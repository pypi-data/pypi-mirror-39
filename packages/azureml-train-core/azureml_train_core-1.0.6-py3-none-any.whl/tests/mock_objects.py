# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

from unittest.mock import Mock
from azureml.core import Experiment
from azureml.core.authentication import ArmTokenAuthentication
from azureml.core.workspace import Workspace
from azureml.core.compute_target import _BatchAITarget, LocalTarget
from azureml.core.compute import AmlCompute
from azureml.core.runconfig import AzureContainerRegistry, RunConfiguration
from azureml.core.run import Run
from azureml._base_sdk_common.utils import convert_dict_to_list

from azureml.train.estimator import MMLBaseEstimator, MMLBaseEstimatorRunConfig


class MockObjects:

    # These could be @classmethod, where cls is the first param and MockObjects. turns into cls.
    @staticmethod
    def get_image_repo():
        mock_repo = AzureContainerRegistry()
        mock_repo.address = "image.repository.address"
        mock_repo.username = "imageusername"
        mock_repo.password = "imagepassword"
        return mock_repo

    @staticmethod
    def get_run_config(arguments=None):
        mock_config = RunConfiguration(script="testscript.py",
                                       arguments=arguments if arguments else [])
        mock_config.target = "batchai"
        mock_config.framework = "CNTK"
        return mock_config

    @staticmethod
    def get_run_config_amlcompute():
        mock_config = RunConfiguration(script="testscript.py")
        mock_config.amlcompute.vm_size = "STANDARD_D1_V2"
        mock_config.target = "amlcompute"
        return mock_config

    @staticmethod
    def get_workspace():
        mock_workspace = Mock(spec_set=Workspace)
        workspace_attrs = {
            "subscription_id": "test_subscription_123",
            "name": "test_ws",
            "resource_group": "test_rg",
            "_auth_object": ArmTokenAuthentication("test_arm_token")
        }
        mock_workspace.configure_mock(**workspace_attrs)
        return mock_workspace

    @staticmethod
    def get_experiment():
        mock_experiment = Mock(spec_set=Experiment)
        experiment_attrs = {"name": "test_project", "workspace": MockObjects.get_workspace()}
        mock_experiment.configure_mock(**experiment_attrs)
        return mock_experiment

    @staticmethod
    def get_project_folder():
        return "."

    @staticmethod
    def get_estimator(script_params=None):
        mock_estimator = Mock(spec_set=MMLBaseEstimator)
        estimator_attrs = {
            "source_directory": MockObjects.get_project_folder(),
            "_estimator_config": MockObjects.get_mock_estimator_config(script_params),
            "run_config": MockObjects.get_run_config(convert_dict_to_list(script_params)),
            "_compute_target": MockObjects.get_compute_target_batchai()
        }
        mock_estimator.configure_mock(**estimator_attrs)
        return mock_estimator

    @staticmethod
    def get_mock_estimator_config(script_params=None):
        mock_config = Mock(spec_set=MMLBaseEstimatorRunConfig)
        config_attrs = {
            "_script_params": script_params
        }
        mock_config.configure_mock(**config_attrs)
        return mock_config

    @staticmethod
    def get_estimator_with_conda_dependencies():
        mock_estimator = Mock(spec_set=MMLBaseEstimator)
        estimator_attrs = {
            "source_directory": MockObjects.get_project_folder(),
            "_estimator_config": MockObjects.get_mock_estimator_config(),
            "run_config": MockObjects.get_run_config()
        }
        mock_estimator.configure_mock(**estimator_attrs)
        return mock_estimator

    @staticmethod
    def get_estimator_auto_create_cluster():
        mock_estimator = Mock(spec_set=MMLBaseEstimator)
        estimator_attrs = {
            "source_directory": MockObjects.get_project_folder(),
            "_estimator_config": MockObjects.get_mock_estimator_config(),
            "run_config": MockObjects.get_run_config_amlcompute()
        }
        mock_estimator.configure_mock(**estimator_attrs)
        return mock_estimator

    @staticmethod
    def get_compute_target_batchai(name='batchaitarget'):
        mock_compute_target = Mock(spec_set=_BatchAITarget)
        target_attrs = {
            "name": name,
            "cluster_name": "test_cluster",
            "subscription_id": "test_subscription_123",
            "resource_group_name": "test_rg",
            "type": "batchai"
        }
        mock_compute_target.configure_mock(**target_attrs)
        mock_compute_target._serialize_to_dict.return_value = {
            "cluster_name": "test_cluster",
            "subscription_id": "test_subscription_123",
            "resource_group_name": "test_rg",
            "type": "batchai"
        }
        return mock_compute_target

    @staticmethod
    def get_compute_target_local(name='local'):
        mock_compute_target = Mock(spec_set=LocalTarget)
        target_attrs = {
            "name": name,
            "type": "local"
        }
        mock_compute_target.configure_mock(**target_attrs)
        mock_compute_target._serialize_to_dict.return_value = {
            "name": name,
            "type": "local"
        }
        return mock_compute_target

    @staticmethod
    def get_compute_target_cloud_amlcompute():
        mock_compute_target = Mock(spec_set=AmlCompute)
        return mock_compute_target

    @staticmethod
    def get_run(run_id, metrics):
        mock_run = Mock(spec_set=Run)
        run_attrs = {
            "experiment": MockObjects.get_experiment(),
            "id": run_id
        }
        mock_run.configure_mock(**run_attrs)
        mock_run.get_metrics.return_value = metrics
        mock_run.get_status.return_value = "Completed"
        mock_run.get_children.return_value = None
        return mock_run
