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

    def test_pif_simple_search(self):
        response = self.client.pif_search(PifSystemReturningQuery(
            size=0,
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal='151278')
                ),
                simple='C22H15NSSi')))
        assert 5 == response.total_num_hits

    def test_extracted(self):
        response = self.client.pif_search(PifSystemReturningQuery(
            size=0,
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal='151278')
                ),
                system=PifSystemQuery(
                    chemical_formula=ChemicalFieldQuery(
                        extract_as='Chemical formula',
                        filter=ChemicalFilter(
                            equal='C22H15NSSi'))))))
        assert response.hits[0].extracted['Chemical formula'] == 'C22H15NSSi'
        assert response.hits[0].extracted_path['Chemical formula'] == '/chemicalFormula'

    def test_updated_at(self):
        all_response = self.client.pif_search(PifSystemReturningQuery(size=1))
        subset_response = self.client.pif_search(PifSystemReturningQuery(
            size=0,
            query=DataQuery(
                system=PifSystemQuery(
                    updated_at=Filter(
                        max='20171001T00:00:00Z')))))
        assert all_response.hits[0].updated_at is not None
        assert all_response.total_num_hits != subset_response.total_num_hits
