import unittest
import xmlrunner
import time

from base_e2e import BaseE2E
from azureml.train.estimator import Estimator


class CustomEstimatorE2ETests(unittest.TestCase):
    _WORKSPACE_NAME = "traincore-gated"

    def setUp(self):
        self._workspace = BaseE2E.get_workspace(self._WORKSPACE_NAME)

    # This test fails with: Error copying files to the remote target.
    # Check that you have read, write, and execute permission
    # to /tmp on the target, and that the disk is not full.
    # Disabling to unblock.
    '''
    def test_dsvm_workflow(self):
        project_name = "test_project" + str(int(time.time()))
        try:
            project = BaseE2E.create_project(self._workspace, project_name)
        except Exception as ex:
            BaseE2E.cleanup_project(project)
            raise ex

        dsvm_compute_target = BaseE2E.get_dsvm_target()
        project.attach_legacy_compute_target(dsvm_compute_target)

        BaseE2E.copy_user_script_to_project(project, "svm_mnist_classification.py")

        print("Creating Custom Estimator...")
        estimator = Estimator(project, compute_target=dsvm_compute_target,
                              entry_script="svm_mnist_classification.py",
                              pip_packages=["scipy", "scikit-learn"])

        try:
            script_run = BaseE2E.run_experiment(estimator)
            run_status = script_run.get_status()
            assert run_status["status"] == "Completed"
        finally:
            BaseE2E.cleanup(script_run, project)
    '''

    def test_amlcompute_workflow(self):
        project_name = "test_project" + str(int(time.time()))
        try:
            BaseE2E.create_project(project_name)
        except Exception:
            BaseE2E.cleanup_project(project_name)
            raise

        amlcompute_name = "train-gated-d3"
        amlcompute_target = BaseE2E.get_amlcompute(self._workspace, amlcompute_name)

        BaseE2E.copy_user_script_to_project(project_name, "svm_mnist_classification.py")

        print("Creating Custom Estimator...")
        estimator = Estimator(project_name, compute_target=amlcompute_target,
                              entry_script="svm_mnist_classification.py",
                              pip_packages=["scipy", "scikit-learn"])

        script_run = None
        try:
            script_run = BaseE2E.run_experiment(estimator, self._workspace, "estimator_e2e_test")
            run_status = script_run.get_status()
            assert run_status == "Completed"
        finally:
            BaseE2E.cleanup(script_run, project_name, self._workspace)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner())
