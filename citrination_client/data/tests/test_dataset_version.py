from citrination_client.data import DatasetVersion

def test_can_cr_number():
    d =  DatasetVersion(1)
    number = 2
    assert d.number is 1
    d.number = number
    assert d.number is number
    del(d.number)
    assert d.number is None