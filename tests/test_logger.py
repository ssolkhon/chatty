import logging
import unittest
import tempfile
import os

from logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log_file = tempfile.NamedTemporaryFile(suffix='.log',
                                                    delete=False)
        self.log = Logger(name='test', level=logging.DEBUG,
                          filename=self.log_file.name)

    def tearDown(self):
        self.log_file.close()
        os.unlink(self.log_file.name)

    def test_logger_name(self):
        self.assertEqual(self.log.logger.name, 'test')

    def test_logger_level(self):
        self.assertEqual(self.log.logger.level, logging.DEBUG)

    def test_logger_info(self):
        with self.assertLogs(self.log.logger, level='INFO') as cm:
            self.log.info('Test info message')
        self.assertEqual(cm.output, ['INFO:test:Test info message'])

    def test_logger_debug(self):
        with self.assertLogs(self.log.logger, level='DEBUG') as cm:
            self.log.debug('Test debug message')
        self.assertEqual(cm.output, ['DEBUG:test:Test debug message'])

    def test_logger_warning(self):
        with self.assertLogs(self.log.logger, level='WARNING') as cm:
            self.log.warning('Test warning message')
        self.assertEqual(cm.output, ['WARNING:test:Test warning message'])

    def test_logger_error(self):
        with self.assertLogs(self.log.logger, level='ERROR') as cm:
            self.log.error('Test error message')
        self.assertEqual(cm.output, ['ERROR:test:Test error message'])

    def test_logger_critical(self):
        with self.assertLogs(self.log.logger, level='CRITICAL') as cm:
            self.log.critical('Test critical message')
        self.assertEqual(cm.output, ['CRITICAL:test:Test critical message'])

    def test_log_file_exists(self):
        self.log.info("Hello, World!")
        with open(self.log_file.name, 'r') as f:
            data = f.read()
        assert "Hello, World!" in data


if __name__ == '__main__':
    unittest.main()
