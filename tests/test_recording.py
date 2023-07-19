import unittest
import tempfile

import speech_recognition
import os

from unittest.mock import patch, MagicMock

import recording


class TestRecording(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.record = recording.Recording(self.test_dir.name)

    def test_recording(self):
        self.assertEqual(type(self.record), recording.Recording)
        self.assertEqual(self.record.log.logger.name, 'recording')

    def test_path_exists(self):
        self.assertEqual(self.test_dir.name, self.record.path)

    @patch('recording.os')
    def test_path_permission_error(self, os_mock):
        os_mock.path.exists.return_value = False
        os_mock.mkdir.side_effect = PermissionError
        with self.assertRaises(PermissionError):
            recording.Recording('/foo')

    @patch('speech_recognition.Microphone')
    @patch('speech_recognition.Recognizer')
    def test_record_microphone(self, recognizer_mock, microphone_mock):
        recognizer_instance = recognizer_mock.return_value
        microphone_instance = microphone_mock.return_value
        audio_mock = MagicMock(spec=speech_recognition.AudioData)

        audio_mock.get_wav_data.return_value = b'sample audio data'
        recognizer_instance.listen.return_value = audio_mock

        # Use the mocked recognizer as the context
        microphone_instance.__enter__.return_value = microphone_instance

        self.record = recording.Recording(self.test_dir.name)
        self.record.record_microphone()

        # Test that we called speech_recognition.Recognizer.listen()
        recognizer_instance.listen.assert_called_once()

        # Test that the wav file was saved
        self.assertTrue(os.path.exists(
            self.test_dir.name + '/microphone_recording.wav'))

    @patch('recording.gTTS')
    def test_record_text(self, mock_gtts):
        mock_gtts_instance = mock_gtts.return_value

        self.record = recording.Recording(self.test_dir.name)
        self.record.record_text('Hello World')

        mock_gtts_instance.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
