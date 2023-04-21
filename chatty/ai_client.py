import logger


class AIClient(object):
    def __init__(self, log=None):
        if log:
            self.log = log
        else:
            self.log = logger.Logger('aiclient')
