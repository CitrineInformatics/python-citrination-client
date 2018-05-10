from citrination_client.data import DatasetVersion

def test_can_crud_number():
    """
    Tests that full get/set/delete functionality is
    available for the number property
    """
    d =  DatasetVersion(1)
    number = 2
    assert d.number is 1
    d.number = number
    assert d.number is number
    del(d.number)
    assert d.number is None