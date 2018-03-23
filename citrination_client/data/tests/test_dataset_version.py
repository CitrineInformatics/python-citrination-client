from citrination_client.data import DatasetVersion

"""
Tests that the setters, getters, and deleters
for the properties on the DatasetVersion class are
functioning correctly
"""
def test_can_crud_number():
    d =  DatasetVersion(1)
    number = 2
    assert d.number is 1
    d.number = number
    assert d.number is number
    del(d.number)
    assert d.number is None