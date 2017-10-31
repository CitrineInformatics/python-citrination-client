from os import environ

from citrination_client import *

class TestPifQuery():

    @classmethod
    def setup_class(cls):
        cls.client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])

    def test_uid_query(self):
        """Testing that a query against a UID only pulls back that record"""
        target_uid = "000496A81BDD616A5BBA1FC4D3B5AC1A"
        query = PifSystemReturningQuery(query=DataQuery(system=PifSystemQuery(uid=Filter(equal=target_uid))))
        result = self.client.pif_search(query)
        assert result.total_num_hits == 1
        assert result.hits[0].system.uid == target_uid

    def test_pif_search(self):
        response = self.client.pif_search(PifSystemReturningQuery(
            size=0,
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal='151278')
                ),
                system=PifSystemQuery(
                    chemical_formula=ChemicalFieldQuery(
                        filter=ChemicalFilter(
                            equal='C22H15NSSi'))))))
        assert 5 == response.total_num_hits