#!/usr/bin/env python3

import sys
import subprocess

from openai_client import OpenAIClient
from recording import Recording

import config
import logger


def main():
    log = logger.Logger('chatty', config.LOG_LEVEL)

    if not config.OPENAI_API_TOKEN:
        message = "Error: OPENAI_API_TOKEN not set"
        log.error(message)
        print(message)
        sys.exit(1)

    ai = OpenAIClient(config.OPENAI_API_TOKEN, log)

    models = ai.list_model_names()
    for model in config.REQUIRED_MODELS:
        if model not in models:
            message = f"Could not find model { model }"
            log.error(message)
            print(message)
            sys.exit(1)

    recording = Recording('./recordings')

    while True:
        recording.record()

        speech_to_text = ai.speech_to_text(recording.filename)

        if "goodbye" in speech_to_text.lower():
            break

        chatgpt_text = ai.chatgpt_response(speech_to_text)
        subprocess.call(["say", chatgpt_text])

    subprocess.call(["say", "goodbye"])


if __name__ == '__main__':
    main()
