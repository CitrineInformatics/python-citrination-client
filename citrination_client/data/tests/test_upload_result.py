from citrination_client.data import UploadResult

def test_indicates_failure():
    """
    Tests that the presence of a single failure
    will make the result report unsuccessful
    """
    ur = UploadResult()
    ur.add_failure("test.jpg", "bad filename")
    assert ur.successful() is False

def test_default_is_success():
    """
    Tests that an empty result is successful
    """
    ur = UploadResult()
    assert ur.successful()

def test_add_success():
    """
    Tests that a success can be added to the upload
    result
    """
    ur = UploadResult()
    ur.add_success("my/path.jpg", 2, "path.jpg")
    assert len(ur.successes) == 1

def test_cant_write_lists():
    """
    Tests that the successes and failures properties
    are not settable
    """
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
