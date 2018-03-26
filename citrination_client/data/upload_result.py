class UploadResult(object):
    """
    The result of an attempted upload. Keeps track of the failures
    and successes if multiple files were uploaded (for instance,
    if a directory was uploaded).
    """

    def __init__(self):
        """
        Constructor.
        """
        self._failures = []
        self._successes = []

    @property
    def failures(self):
        return self._failures

    @property
    def successes(self):
        return self._successes

    def successful(self):
        """
        Indicates whether or not the entire upload was successful.

        :return: Whether or not the upload was successful
        :rtype: bool
        """
        return len(self._failures) == 0

    def add_failure(self, filepath, reason):
        """
        Registers a file as a failure to upload.

        :param filepath: The path to the file which was to be uploaded.
        :type filepath: str
        :param reason: The reason the file failed to upload
        :type reason: str
        """
        self._failures.append({
                "path": filepath,
                "reason": reason
            })

    def add_success(self, filepath):
        """
        Registers a file as successfully uploaded.

        :param filepath: The path to the successfully uploaded file.
        :type filepath: str
        """
        self._successes.append({
                "path": filepath
            })