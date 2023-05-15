import unittest
import logging
import tempfile

from unittest.mock import patch, MagicMock
from requests import ConnectionError

import openai_client
import logger


class TestOpenAIClient(unittest.TestCase):

    def setUp(self):
        token = "285A31B2-61BD-4B0B-A553-48077A49AB43"
        self.client = openai_client.OpenAIClient(token)

    @patch('openai_client.requests')
    def test_list_model_names(self, requests_mock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data':  [{'id': 'text-curie:001', 'object': 'model'},
                      {'id': 'text-babbage:001', 'object': 'model'}]
        }

        requests_mock.get.return_value = mock_response
        models = self.client.list_model_names()
        assert type(models), list
        assert len(models) == 2

    @patch('openai_client.requests')
    def test_list_model_names_500(self, requests_mock):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        requests_mock.get.return_value = mock_response
        with self.assertRaises(SystemExit) as cm:
            self.client.list_model_names()

        self.assertEqual(cm.exception.code, 1)

    @patch('openai_client.requests')
    def test_list_model_names_connection_error(self, requests_mock):
        requests_mock.get.side_effect = ConnectionError
        with self.assertRaises(ConnectionError):
            self.client.list_model_names()

    @patch('openai_client.requests')
    def test_speech_to_text(self, requests_mock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'text':  "Hello from ChatGPT"
        }

        requests_mock.post.return_value = mock_response
        with tempfile.NamedTemporaryFile(suffix='.wav') as file:
            result = self.client.speech_to_text(file.name)
        assert type(result), str
        assert result, "Hello from ChatGPT"

    @patch('openai_client.requests')
    def test_speech_to_text_500(self, requests_mock):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        requests_mock.post.return_value = mock_response
        with self.assertRaises(SystemExit) as cm:
            with tempfile.NamedTemporaryFile(suffix='.wav') as file:
                self.client.speech_to_text(file.name)

        self.assertEqual(cm.exception.code, 1)

    @patch('openai_client.requests')
    def test_speech_to_text_connection_error(self, requests_mock):
        requests_mock.post.side_effect = ConnectionError
        with self.assertRaises(ConnectionError):
            with tempfile.NamedTemporaryFile(suffix='.wav') as file:
                self.client.speech_to_text(file.name)

    @patch('openai_client.requests')
    def test_chatgpt_response(self, requests_mock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Pong"}},
                        {"message": {"content": "Pongs"}},
                        {"message": {"content": "Songs"}}]
        }

        requests_mock.post.return_value = mock_response
        result = self.client.chatgpt_response("Ping")
        assert type(result), str
        assert result, "Pong"

    @patch('openai_client.requests')
    def test_chatgpt_response_500(self, requests_mock):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        requests_mock.post.return_value = mock_response
        with self.assertRaises(SystemExit) as cm:
            self.client.chatgpt_response("Ping")

        self.assertEqual(cm.exception.code, 1)

    @patch('openai_client.requests')
    def test_chatgpt_response_connection_error(self, requests_mock):
        requests_mock.post.side_effect = ConnectionError
        with self.assertRaises(ConnectionError):
            self.client.chatgpt_response("Ping")


if __name__ == '__main__':
    unittest.main()
