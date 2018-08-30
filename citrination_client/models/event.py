class Event(object):
    """
    The representation of an in progress process. Described by a title, subtitle and subevent.
    """

    def __init__(self, title, normalized_progress, subtitle=None, subevent=None):
        """
        Constructor.

        :param title: The title of the event
        :type title: str
        :param subtitle: More detail about the event
        :type subtitle: str
        :param subevent: An event object describing the current state of the service's
            progress toward readiness
        :type subevent: Event
        :param normalized_progress: The fractional representation of the status of the event
        :type normalized_progress: float
        """
        self._title = title
        self._subtitle = subtitle
        self._subevent = subevent
        self._normalized_progress = normalized_progress

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @title.deleter
    def title(self):
        self._title = None

    @property
    def subtitle(self):
        return self._subtitle

    @subtitle.setter
    def subtitle(self, value):
        self._subtitle = value

    @subtitle.deleter
    def subtitle(self):
        self._subtitle = None

    @property
    def subevent(self):
        return self._subevent

    @subevent.setter
    def subevent(self, value):
        self._subevent = value

    @subevent.deleter
    def subevent(self):
        self._subevent = None

    @property
    def normalized_progress(self):
        return self._normalized_progress

    @normalized_progress.setter
    def normalized_progress(self, value):
        self._normalized_progress = value

    @normalized_progress.deleter
    def normalized_progress(self):
        self._normalized_progress = None
