

class CronablyException(Exception):

    def __init__(self, msg):
        super(CronablyException, self).__init__(msg)