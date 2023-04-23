import speech_recognition
import os

from gtts import gTTS

import logger


class Recording(object):
    def __init__(self, path, log=logger.Logger('recording')):
        self.log = log
        self.path = path
        parent = '/'.join(self.path.split('/')[:-1])
        if not os.path.exists(parent):
            os.mkdir(parent)

    def record_microphone(self):
        r = speech_recognition.Recognizer()
        self.log.debug("Recording")
        with speech_recognition.Microphone() as source:
            print("Please ask Chatty a question...")
            audio = r.listen(source)
        self.log.debug("Recording ended")
        self.log.debug(f"Saving file '{ self.path }")
        with open(self.path, "wb") as f:
            f.write(audio.get_wav_data())

    def record_text(self, text):
        text_to_speech = gTTS(text=text, lang='en')
        text_to_speech.save(self.path)
