class ProcessStatus(object):

    def __init__(self, result, progress, status, messages=None):
        self._status = status
        self._result = result
        self._progress = progress
        self._messages = messages

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        self._uuid = value

    @uuid.deleter
    def uuid(self):
        self._uuid = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    @result.deleter
    def result(self):
        self._result = None

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value

    @progress.deleter
    def progress(self):
        self._progress = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @status.deleter
    def status(self):
        self._status = None

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, value):
        self._messages = value

    @messages.deleter
    def messages(self):
        self._messages = None

    def finished(self):
        return self.status == "Finished"

    def killed(self):
        return self.status == "Killed"

    def accepted(self):
        return self.status == "Accepted"