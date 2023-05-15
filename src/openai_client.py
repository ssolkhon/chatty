import sys

import requests

from ai_client import AIClient

BASE_URL = "https://api.openai.com/v1"


class OpenAIClient(AIClient):

    def __init__(self, api_token, log=None):
        if log:
            super().__init__(log)
        else:
            super().__init__()
        self.api_token = api_token
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def list_model_names(self):
        self.log.debug("Listing models from OpenAI API")
        url = f"{BASE_URL}/models"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            self.log.error(f"Error listing models '{ response.text }'")
            print(response.text)
            sys.exit(1)

        result = [model['id'] for model in response.json()['data']]
        self.log.debug(f"Models available are '{ result }")
        return result

    def speech_to_text(self, file):
        self.log.debug(f"Converting speech in { file } to text using OpenAI "
                       f"API")

        url = f"{BASE_URL}/audio/transcriptions"

        data = {
            "model": "whisper-1",
            "file": file,
        }
        files = {
            "file": open(file, "rb")
        }

        response = requests.post(url, files=files, data=data,
                                 headers=self.headers)

        if response.status_code != 200:
            self.log.error(f"Error converting speech to text "
                           f"'{ response.text }'")
            print(response.text)
            sys.exit(1)

        result = response.json()["text"]

        self.log.info(f"Converted speech result is '{ result }'")
        return result

    def chatgpt_response(self, text):
        self.log.info(f"Asking ChatGPT '{ text }'")
        url = f"{BASE_URL}/chat/completions"

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ]
        }

        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code != 200:
            self.log.error(f"Error getting response from ChatGPT "
                           f"'{ response.text }'")
            print(response.text)
            sys.exit(1)

        result = response.json()["choices"][0]["message"]["content"]

        self.log.info(f"Response from ChatGPT is '{ result }'")
        return result
