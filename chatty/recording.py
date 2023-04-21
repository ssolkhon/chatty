import speech_recognition

from pathlib import Path

import logger


class Recording(object):
    def __init__(self, path, log=None):
        if log:
            self.log = log
        else:
            self.log = logger.Logger('recording')
        self.path = Path(path)
        self.filename = f"{ self.path }/audio.wav"
        if not self.path.exists():
            self.path.mkdir()

    def _save_wav(self, audio):
        self.log.debug(f"Saving file '{ self.filename }")
        with open(self.filename, "wb") as f:
            print(f"Saving audio to {self.filename}")
            f.write(audio.get_wav_data())

    def record(self):
        r = speech_recognition.Recognizer()
        self.log.debug("Recording")
        with speech_recognition.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        self.log.debug("Recording ended")
        self._save_wav(audio)
