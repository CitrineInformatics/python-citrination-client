from citrination_client.models import Event
from citrination_client.base.errors import CitrinationClientError

class ServiceStatus(object):
    """
    The status of a service for a given model on Citrination. The status of a
    service is summarized by the ready value indicating whether or not the service
    is in a state where it can be utilized. It also includes more detailed
    information about the current state of the service in the form of a descriptive
    sentence, a context string and an event object.
    """

    @staticmethod
    def from_response_dict(response_dict):

        if "event" in response_dict:
            event_dict = response_dict["event"]
            event = Event(
                title = event_dict["title"],
                normalized_progress = event_dict["normalizedProgress"]
            )

            if "subtitle" in response_dict["event"]:
                event.subtitle = event_dict["subtitle"]

            if "subevent" in response_dict["event"]:
                subevent_dict = response_dict["event"]["subevent"]
                subevent = Event(
                    title = subevent_dict["title"],
                    subtitle = subevent_dict["subtitle"],
                    normalized_progress = subevent_dict["normalizedProgress"]
                )
                event.subevent = subevent
        else:
            event = None

        return ServiceStatus(
            ready = response_dict["ready"],
            reason = response_dict["reason"],
            context = response_dict["context"],
            event = event
        )

    def __init__(self, ready, context, reason, event):
        """
        Constructor.

        :param ready: Boolean indicating whether or not the service can be used
        :type ready: bool
        :param context: A contextual description of the current status: "notice",
            "success", "error"
        :type context: str
        :param reason: A full sentence explanation of the service's status
        :type reason: str
        :param event: An event object describing the current state of the service's
            progress toward readiness
        :type event: Event
        """
        self._ready   = ready
        self._context = context
        self._event   = event
        self._reason  = reason

    @property
    def ready(self):
        return self._ready

    @ready.setter
    def ready(self, value):
        self._ready = value

    @ready.deleter
    def ready(self):
        self._ready = None

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @context.deleter
    def context(self):
        self._context = None

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, value):
        self._event = value

    @event.deleter
    def event(self):
        self._event = None

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, value):
        self._reason = value

    @reason.deleter
    def reason(self):
        self._reason = None

    def is_ready(self):
        """
        Indicates whether or not the service is ready to be used.

        :return: A boolean
        :rtype: bool
        """
        return self.ready == True

