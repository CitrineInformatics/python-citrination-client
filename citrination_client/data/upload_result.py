class UploadResult(object):

    def __init__(self):
        self._failures = []
        self._successes = []

    @property
    def failures(self):
        return self._failures

    @property
    def successes(self):
        return self._successes

    def successful(self):
        return len(self._failures) == 0

    def add_failure(self, filepath, reason):
        self._failures.append({
                "path": filepath,
                "reason": reason
            })

    def add_success(self, filepath):
        self._successes.append({
                "path": filepath
            })