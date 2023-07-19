#!/usr/bin/env python3

import sys

from pydub import AudioSegment
from pydub.playback import play

import config
import logger
import openai_client
import recording


def main():
    log = logger.Logger('chatty', config.LOG_LEVEL)

    if not config.OPENAI_API_TOKEN:
        message = "Error: OPENAI_API_TOKEN not set"
        log.error(message)
        print(message)
        sys.exit(1)

    ai = openai_client.OpenAIClient(config.OPENAI_API_TOKEN, log)

    models = ai.list_model_names()
    for model in config.REQUIRED_MODELS:
        if model not in models:
            message = f"Could not find model { model }"
            log.error(message)
            print(message)
            sys.exit(1)

    my_recording = recording.Recording('./recordings', log)

    while True:
        my_recording.record_microphone()
        speech_to_text = ai.speech_to_text(my_recording.path +
                                           '/microphone_recording.wav')

        if "goodbye" in speech_to_text.lower():
            break

        chatgpt_text = ai.chatgpt_response(speech_to_text)
        my_recording.record_text(chatgpt_text)
        sound = AudioSegment.from_file(my_recording.path +
                                       '/text_recording.mp3',
                                       format="mp3")
        play(sound)

    my_recording.record_text("Goodbye")

    sound = AudioSegment.from_file("./recordings/text_recording.mp3",
                                   format="mp3")
    play(sound)


if __name__ == '__main__':
    main()
