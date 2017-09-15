from os import environ

from citrination_client import CitrinationClient
from citrination_client import PifSystemReturningQuery, DataQuery, PifSystemQuery, Filter


def test_uid_query():
    """Testing that a query against a UID only pulls back that record"""
    target_uid = "000496A81BDD616A5BBA1FC4D3B5AC1A"
    query = PifSystemReturningQuery(query=DataQuery(system=PifSystemQuery(uid=Filter(equal=target_uid))))
    
    client = CitrinationClient(environ["CITRINATION_API_KEY"])
    result = client.pif_search(query)
    assert result.total_num_hits == 1
    assert result.hits[0].system.uid == target_uid
