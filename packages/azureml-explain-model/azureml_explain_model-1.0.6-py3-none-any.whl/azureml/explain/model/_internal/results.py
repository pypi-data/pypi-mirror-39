# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines a set of functions for retrieving model explanation result data from run history."""

import os
import json

from azureml._async import TaskQueue, WorkerPool
from .constants import MODEL_TYPE, CLASSIFICATION_TYPE
try:
    from azureml._restclient.assets_client import AssetsClient
except ImportError:
    print("Could not import azureml.core, required if using run history")
from .common import NUM_FEATURES, NUM_BLOCKS, module_logger, _sort_feature_list_single, \
    _sort_feature_list_multiclass, _two_dimensional_slice

EXPLANATION_ASSET = 'explanation_asset'


def _create_download_dir():
    # create the downloads folder
    download_dir = './download_explanation/'
    os.makedirs(download_dir, exist_ok=True)
    return download_dir


def _download_artifact(run, download_dir, artifact_name):
    file_name = '{}{}.json'.format('explanation/', artifact_name)
    path = os.path.join(download_dir, file_name)
    run.download_file(file_name, path)
    with open(path, 'rb') as f:
        json_string = f.read()
        values = json.loads(json_string.decode('utf-8'))
    return values


def _download_model_summary(run, download_dir, summary_name, top_k=None):
    explanation_asset = None
    storage_metadata = None
    asset_found = False
    assets_client = AssetsClient.create(run.experiment.workspace)
    explanation_assets = assets_client.get_assets_by_run_id_and_name(run.id, EXPLANATION_ASSET)
    if len(explanation_assets) > 0:
        explanation_asset = explanation_assets[0]
        storage_metadata = explanation_asset.meta
        meta_keys = storage_metadata.keys()
        for key in meta_keys:
            if summary_name in key:
                asset_found = True
                break
    if not asset_found:
        return _download_artifact(run, download_dir, summary_name)
    else:
        num_columns_to_return = int(storage_metadata[NUM_FEATURES + '_' + summary_name])
        num_blocks = int(storage_metadata[NUM_BLOCKS + '_' + summary_name])
        if top_k is not None:
            num_columns_to_return = min(top_k, num_columns_to_return)
        summary = None
        # Get the blocks
        for idx in range(num_blocks):
            block_name = '{}_{}'.format(summary_name, str(idx))
            block = _download_artifact(run, download_dir, block_name)
            if not isinstance(block, list):
                raise ValueError('Cannot process scalar blocks')
            # in both of these cases, we have to deal with possible multidimensionality
            if summary is None:
                summary = block
                if not isinstance(block[0], list):
                    num_columns_read = len(summary)
                elif not isinstance(block[0][0], list):
                    num_columns_read = len(summary[0])
                elif not isinstance(block[0][0][0], list):
                    num_columns_read = len(summary[0][0])
            else:
                if not isinstance(block[0], list):
                    summary += block
                    num_columns_read = len(summary)
                elif not isinstance(block[0][0], list):
                    for i in range(len(summary)):
                        summary[i] += block[i]
                    num_columns_read = len(summary[0])
                elif not isinstance(block[0][0][0], list):
                    for i in range(len(summary)):
                        for j in range(len(summary[i])):
                            summary[i][j] += block[i][j]
                    num_columns_read = len(summary[0][0])

            if num_columns_read >= num_columns_to_return:
                break
        if not isinstance(summary[0], list):
            return summary[:num_columns_to_return]
        else:
            # currently assuming there's no need to slice anything more than 2 dimensional
            return _two_dimensional_slice(summary, num_columns_to_return)


def get_model_explanation(run):
    """Return the feature importance values.
    :param run: An object that represents a model explanation run.
    :type run: azureml.core.run.Run
    :rtype: (Union[numpy.ndarray, list[numpy.ndarray]], numpy.ndarray)
    :return: tuple(feature_importance_values, expected_values) where
        - feature_importance_values = For a model with a single output such as regression, this returns
        a matrix of feature importance values. For models with vector outputs this function returns a
        list of such matrices, one for each output. The dimension of this matrix is (# examples x # features).
        - expected_values = The expected value of the model applied to the set of initialization examples.
        For SHAP values, when a version older than 0.20.0 is used, this value is None. The expected
        values are in the last columns of the matrices in feature_importance_values. In this case, the
        dimension of those matrix is (# examples x (# features + 1)). This causes each row to sum to
        the model output for that example.
    """
    download_dir = _create_download_dir()
    shap_values = _download_artifact(run, download_dir, 'shap_values')
    expected_values = None
    try:
        expected_values = _download_artifact(run, download_dir, 'expected_values')
    except Exception:
        module_logger.warning(
            "expected_values is not found in Artifact service")
    return shap_values, expected_values


def get_model_explanation_from_run_id(workspace, experiment_name, run_id):
    """Return the feature importance values.

    :param workspace: An object that represents a workspace.
    :type workspace: azureml.core.workspace.Workspace
    :param experiment_name: The name of the experiment.
    :type experiment_name: str
    :param run_id: A GUID that represents a run.
    :type run_id: str
    :rtype: (Union[numpy.ndarray, list[numpy.ndarray]], numpy.ndarray)
    :return: tuple(feature_importance_values, expected_values) where
        - feature_importance_values = For a model with a single output such as regression, this
        returns a matrix of feature importance values. For models with vector outputs this function
        returns a list of such matrices, one for each output. The dimension of this matrix
        is (# examples x # features).
        - expected_values = The expected value of the model applied to the set of initialization examples.
        For SHAP values, when a version older than 0.20.0 is used, this value is None. The expected
        values are in the last columns of the matrices in feature_importance_values. In this case, the
        dimension of those matrix is (# examples x (# features + 1)). This causes each row to sum to
        the model output for that example.
    """
    try:
        from azureml.core import Experiment, Run
    except ImportError as exp:
        module_logger.error("Could not import azureml.core.run")
        raise exp
    experiment = Experiment(workspace, experiment_name)
    run = Run(experiment, run_id=run_id)
    shap_values, expected_values = get_model_explanation(run)
    return shap_values, expected_values


def get_model_summary_from_run_id(workspace, experiment_name, run_id, overall_summary_only=False, top_k=None):
    """Return the feature importance values.

    :param workspace: An object that represents a workspace.
    :type workspace: azureml.core.workspace.Workspace
    :param experiment_name: The name of an experiment_name.
    :type experiment_name: str
    :param run_id: A GUID that represents a run.
    :type run_id: str
    :param overall_summary_only: A flag that indicates whether to return per class summary.
    :type overall_summary_only: bool
    :param top_k: An integer that indicates the number of the most important features to return.
    :type top_k: int
    :rtype: (list, list, list, list)
    :return: tuple(overall_feature_importance_values, overall_important_features,
        per_class_feature_importance_values, per_class_important_features) where
        - overall_feature_importance_values = The model level feature importance values sorted
        in descending order.
        - overall_important_features = The feature names sorted in the same order as in
        overall_summary or the indexes that would sort overall_summary.
        - per_class_feature_importance_values = The class level feature importance values
        sorted in descending order where a binary classification (this class or not) is
        evaluated. Only available for the classification case.
        - per_class_important_features = The feature names sorted in the same order as
        in per_class_summary or the indexes that would sort per_class_summary. Only
        available for the classification case.
    """
    try:
        from azureml.core import Experiment, Run
    except ImportError as exp:
        module_logger.error("Could not import azureml.core.run")
        raise exp
    experiment = Experiment(workspace, experiment_name)
    run = Run(experiment, run_id=run_id)
    return get_model_summary(run, overall_summary_only, top_k)


def get_model_summary(run, overall_summary_only=False, top_k=None):
    """Return the feature importance values.

    :param run: An object that represents a model explanation run.
    :type run: azureml.core.run.Run
    :param overall_summary_only: A flag that indicates whether to return per class summary.
    :type overall_summary_only: bool
    :param top_k: An integer that indicates the number of the most important features to return.
    :type top_k: int
    :rtype: (list, list, list, list)
    :return: tuple(overall_feature_importance_values, overall_important_features
        per_class_feature_importance_values, per_class_important_features) where
        - overall_feature_importance_values = The model level feature importance values sorted in
        descending order.
        - overall_important_features = The feature names sorted in the same order as in
        overall_summary or the indexes that would sort overall_summary.
        - per_class_feature_importance_values = The class level feature importance values
        sorted in descending order where a binary classification (this class or not) is evaluated.
        Only available for the classification case.
        - per_class_important_features = The feature names sorted in the same order as in
        per_class_summary or the indexes that would sort per_class_summary. Only available for
        the classification case.
    """
    download_dir = _create_download_dir()
    feature_names = None
    try:
        feature_names = _download_artifact(run, download_dir, 'feature_names')
    except Exception:
        module_logger.info(
            "feature_names is not found in Artifact service")

    pool = WorkerPool(_parent_logger=module_logger)
    with TaskQueue(worker_pool=pool,
                   _ident="DownloadExplanationSummaries",
                   _parent_logger=module_logger) as task_queue:
        try:
            model_type = run.get_properties()[MODEL_TYPE]
        except Exception:
            module_logger.info("failed to retrieve model_type from properties, retrieving from metrics instead")
            model_type = run.get_metrics()[MODEL_TYPE]
        if model_type == CLASSIFICATION_TYPE and not overall_summary_only:
            summaries = [
                'overall_summary',
                'overall_importance_order',
                'per_class_summary',
                'per_class_importance_order'
            ]
            results = []
            for summary_name in summaries:
                task = task_queue.add(_download_model_summary, run, download_dir, summary_name, top_k)
                results.append(task)
            results = list(map(lambda task: task.wait(), results))
            overall_summary, overall_importance_order, per_class_summary, per_class_importance_order = results
            overall_importance = overall_importance_order
            per_class_importance = per_class_importance_order
            if feature_names is not None:
                overall_importance = _sort_feature_list_single(feature_names, overall_importance_order)
                per_class_importance = _sort_feature_list_multiclass(feature_names, per_class_importance_order)
            return overall_summary, overall_importance, per_class_summary, per_class_importance
        else:
            overall_summaries = [
                'overall_summary',
                'overall_importance_order'
            ]
            overall_results = []
            for summary_name in overall_summaries:
                task = task_queue.add(_download_model_summary, run, download_dir, summary_name, top_k)
                overall_results.append(task)
            overall_results = list(map(lambda task: task.wait(), overall_results))

            overall_summary, overall_importance_order = overall_results
            overall_importance = overall_importance_order
            if feature_names is not None:
                overall_importance = _sort_feature_list_single(feature_names, overall_importance_order)
            return overall_summary, overall_importance


def get_classes(run):
    """Return the class names or None if not found in Artifact service.

    :param run: An object that represents a model explanation run.
    :type run: azureml.core.run.Run
    :rtype: numpy.ndarray
    :return: The class names passed to explain_model. The order of the class names matches the model output.
    """
    download_dir = _create_download_dir()
    classes = None
    try:
        classes = _download_artifact(run, download_dir, 'classes')
    except Exception:
        module_logger.warning(
            "classes is not found in Artifact service")
    return classes
