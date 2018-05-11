from citrination_client.models import Event


def test_can_initialize_event_without_subevent():
    title = "test"
    subtitle = "test2"
    progress = 0.5

    e = Event(
        title = title,
        subtitle = subtitle,
        normalized_progress = progress
    )

    assert e.title == title
    assert e.subtitle == subtitle
    assert e.normalized_progress == progress
