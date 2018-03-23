from citrination_client.data import DatasetFile

def test_can_crud_path():
    """
    Tests that full get/set/delete functionality is
    available for the path property
    """
    path = "path"
    d =  DatasetFile(path)
    assert d.path is path
    d.path = path
    assert d.path is path
    del(d.path)
    assert d.path is None

def test_can_crud_url():
    """
    Tests that full get/set/delete functionality is
    available for the url property
    """
    path = "path"
    d =  DatasetFile(path)
    url = "http://mysite.com"
    assert d.url is None
    d.url = url
    assert d.url is url
    del(d.url)
    assert d.url is None