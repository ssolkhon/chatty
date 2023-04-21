import os
import logging

OPENAI_API_TOKEN = os.environ.get("OPENAI_API_TOKEN")
REQUIRED_MODELS = ["whisper-1", "gpt-3.5-turbo-0301"]
LOG_LEVEL = logging.DEBUG
