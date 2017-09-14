from citrination_client import CitrinationClient
from citrination_client import PifQuery, SystemQuery, FieldQuery, Filter

from os import environ
from pypif.pif import dumps


def test_uid_query():
    """Testing that a query against a UID only pulls back that record"""
    target_uid = "000496A81BDD616A5BBA1FC4D3B5AC1A"
    query = PifQuery(system=SystemQuery(uid=FieldQuery(filter=Filter(equal=target_uid))))
    
    client = CitrinationClient(environ["CITRINATION_API_KEY"])
    result = client.pif_search(query)
    assert result.total_num_hits == 1
    assert result.hits[0].system.uid == target_uid
