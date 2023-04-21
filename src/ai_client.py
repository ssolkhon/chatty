import logger


class AIClient(object):
    def __init__(self, log=logger.Logger('aiclient')):
        self.log = log
