from citrination_client.data import UploadResult

def test_indicates_failure():
    ur = UploadResult()
    ur.add_failure("test.jpg", "bad filename")
    assert ur.successful() is False

def test_default_is_success():
    ur = UploadResult()
    assert ur.successful()

def test_add_success():
    ur = UploadResult()
    ur.add_success("my/path.jpg")
    assert len(ur.successes) == 1

def test_cant_write_lists():
    ur = UploadResult()

    try:
        ur.successes = "asdf"
        assert False
    except AttributeError:
        assert True

    try:
        ur.failures = "asdf"
        assert False
    except AttributeError:
        assert True