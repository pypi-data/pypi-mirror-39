import unittest
import xmlrunner

from azureml.telemetry import set_diagnostics_collection
from azureml.telemetry.logging_handler import AppInsightsLoggingHandler
from azureml.train._telemetry_logger import _TelemetryLogger


class TelemetryTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TelemetryTests, self).__init__(*args, **kwargs)

    def test_telemetry_logger(self):
        set_diagnostics_collection(send_diagnostics=True)
        logger = _TelemetryLogger.get_telemetry_logger(__name__)
        self.assertEqual(len(logger.handlers), 1)
        self.assertTrue(isinstance(logger.handlers[0], AppInsightsLoggingHandler))
        set_diagnostics_collection(send_diagnostics=False)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner())
