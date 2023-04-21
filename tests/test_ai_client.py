import unittest

import ai_client
import logger


class TestAIClient(unittest.TestCase):
    def test_ai_client(self):
        client = ai_client.AIClient()
        assert type(client), ai_client.AIClient
        assert client.log.logger.name == 'aiclient'

    def test_ai_client_custom_logger(self):
        log = logger.Logger('test')
        client = ai_client.AIClient(log)
        assert type(client), ai_client.AIClient
        assert client.log.logger.name == 'test'


if __name__ == '__main__':
    unittest.main()
