from citrination_client.models import ServiceStatus
from citrination_client.base.errors import CitrinationClientError
import pytest

example_status_response_dict = {
  "reason": "Please wait for machine learning features to become available",
  "ready": True,
  "context": "notice",
  "event": {
    "title": "Initializing machine learning services",
    "subtitle": "Doin some other stuff",
    "normalizedProgress": 1.0,
    "subevent": {
      "title": "A slightly more granular description of what were doing",
      "subtitle": "An even more granular description of what were doing",
      "normalizedProgress": 1.0
    }
  }
}

def test_can_initialize_from_response_dict():

    status = ServiceStatus.from_response_dict(example_status_response_dict)

    assert status.is_ready()
    assert status.reason  == example_status_response_dict["reason"]
    assert status.context == example_status_response_dict["context"]

    event = status.event

    assert event.title == example_status_response_dict["event"]["title"]
    assert event.subtitle == example_status_response_dict["event"]["subtitle"]
    assert event.normalized_progress == example_status_response_dict["event"]["normalizedProgress"]

    subevent = event.subevent

    assert subevent.title == example_status_response_dict["event"]["subevent"]["title"]
    assert subevent.subtitle == example_status_response_dict["event"]["subevent"]["subtitle"]
    assert subevent.normalized_progress == example_status_response_dict["event"]["subevent"]["normalizedProgress"]

example_status_response_dict_without_event = {
  "reason": "Please wait for machine learning features to become available",
  "ready": True,
  "context": "notice"
}

def test_can_initialize_from_response_dict_without_event():

    status = ServiceStatus.from_response_dict(example_status_response_dict_without_event)

    assert status.is_ready()
    assert status.reason  == example_status_response_dict_without_event["reason"]
    assert status.context == example_status_response_dict_without_event["context"]
    assert status.event is None

example_status_response_dict_without_subevent = {
  "reason": "Please wait for machine learning features to become available",
  "ready": True,
  "context": "notice",
  "event": {
    "title": "Initializing machine learning services",
    "subtitle": "Doin some other stuff",
    "normalizedProgress": 1.0
  }
}

def test_can_initialize_from_response_dict_without_subevent():

    status = ServiceStatus.from_response_dict(example_status_response_dict_without_subevent)

    assert status.is_ready()
    assert status.reason  == example_status_response_dict_without_subevent["reason"]
    assert status.context == example_status_response_dict_without_subevent["context"]

    event = status.event

    assert event.title == example_status_response_dict_without_subevent["event"]["title"]
    assert event.subtitle == example_status_response_dict_without_subevent["event"]["subtitle"]
    assert event.normalized_progress == example_status_response_dict_without_subevent["event"]["normalizedProgress"]
    assert event.subevent is None

example_status_response_dict_not_ready = {
  "reason": "Please wait for machine learning features to become available",
  "ready": False,
  "context": "notice",
  "event": {
    "title": "Initializing machine learning services",
    "subtitle": "Doin some other stuff",
    "normalizedProgress": 0.33
  }
}

def test_can_initialize_from_response_dict_not_ready():

    status = ServiceStatus.from_response_dict(example_status_response_dict_not_ready)

    assert not status.is_ready()
    assert status.reason  == example_status_response_dict_not_ready["reason"]
    assert status.context == example_status_response_dict_not_ready["context"]

    event = status.event

    assert event.title == example_status_response_dict_not_ready["event"]["title"]
    assert event.subtitle == example_status_response_dict_not_ready["event"]["subtitle"]
    assert event.normalized_progress == example_status_response_dict_not_ready["event"]["normalizedProgress"]
    assert event.subevent is None

example_status_response_dict_nonsense = {
  "reason": "Please wait for machine learning features to become available",
  "ready": True,
  "context": "notice",
  "event": {
    "title": "Initializing machine learning services",
    "subtitle": "Doin some other stuff",
    "normalizedProgress": 0.33
  }
}

def test_only_ready_when_progress_one():

    with pytest.raises(CitrinationClientError):
        ServiceStatus.from_response_dict(example_status_response_dict_nonsense)
