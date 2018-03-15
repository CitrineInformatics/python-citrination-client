from os import environ

from citrination_client import *

class TestPifQuery():

    @classmethod
    def setup_class(cls):
        cls.client = CitrinationClient().search

    def test_uid_query(self):
        """Testing that a query against a UID only pulls back that record"""
        target_uid = "000496A81BDD616A5BBA1FC4D3B5AC1A"
        query = PifSystemReturningQuery(query=DataQuery(system=PifSystemQuery(uid=Filter(equal=target_uid))))
        result = self.client.pif_search(query)
        assert result.total_num_hits == 1
        assert result.hits[0].system.uid == target_uid

    def test_pagination_overflow(self):
        query = PifSystemReturningQuery(size=0,
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal='1160'))))
        response = self.client.pif_search(query)
        total = response.total_num_hits
        from_index = total - 20

        query = PifSystemReturningQuery(size=45,
            from_index=from_index,
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal='1160'))))
        response = self.client.pif_search(query)
        assert 20 == len(response.hits)

    def test_pagination_from_start(self):
        query = PifSystemReturningQuery(size=200)
        response = self.client.pif_search(query)
        assert 200 == len(response.hits)

    def test_pagination_with_from_index(self):
        query = PifSystemReturningQuery(size=200, from_index=1000)
        response = self.client.pif_search(query)
        assert 200 == len(response.hits)

    def test_auto_pagination(self):
        query = PifSystemReturningQuery(
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal='150670'))))
        response = self.client.pif_search(query)
        assert response.total_num_hits == len(response.hits)

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
            size=1,
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal='151278')
                ),
                system=PifSystemQuery(
                    chemical_formula=ChemicalFieldQuery(
                        extract_as='Chemical formula',
                        filter=ChemicalFilter(
                            equal='C22H15NSSi'))))))
        assert response.hits[0].extracted['Chemical formula'] == '$\\rm$C$_{22}$$\\rm$H$_{15}$$\\rm$N$\\rm$S$\\rm$Si'
        assert response.hits[0].extracted_path['Chemical formula'] == '/chemicalFormula'

    def test_updated_at(self):
        all_response = self.client.pif_search(PifSystemReturningQuery(size=1))
        subset_response = self.client.pif_search(PifSystemReturningQuery(
            size=0,
            query=DataQuery(
                system=PifSystemQuery(
                    updated_at=Filter(
                        max='2017-10-01T00:00:00.000Z')))))
        assert all_response.hits[0].updated_at is not None
        assert all_response.total_num_hits != subset_response.total_num_hits

    def test_search_weight(self):

        # Run a query to get a record with a name
        reference_hit = self.client.pif_search(PifSystemReturningQuery(
            size=1,
            return_system=False,
            query=DataQuery(
                system=PifSystemQuery(
                    names=FieldQuery(
                        filter=Filter(exists=True)))))
        ).hits[0]
        uid = reference_hit.id.split('/')[2]

        # Run two queries where everything is the same except the weight on the name query
        search_result = self.client.pif_multi_search(MultiQuery(
            queries=[
                PifSystemReturningQuery(
                    return_system=False,
                    score_relevance=True,
                    query=DataQuery(
                        system=PifSystemQuery(
                            uid=Filter(equal=uid),
                            names=FieldQuery(
                                filter=Filter(exists=True))))),
                PifSystemReturningQuery(
                    return_system=False,
                    score_relevance=True,
                    query=DataQuery(
                        system=PifSystemQuery(
                            uid=Filter(equal=uid),
                            names=FieldQuery(
                                weight=2.0,
                                filter=Filter(exists=True)))))
            ]))

        # Make sure that the two weights are off by the correct amount
        unweighted_score = search_result.results[0].result.hits[0].score
        weighted_score = search_result.results[1].result.hits[0].score
        assert abs(weighted_score - unweighted_score) > 0.01

    def test_simple_search_weight(self):

        # Run a query to get a record with a name
        reference_hit = self.client.pif_search(PifSystemReturningQuery(
            size=1,
            return_system=True,
            query=DataQuery(
                system=PifSystemQuery(
                    names=FieldQuery(
                        filter=Filter(exists=True)))))
        ).hits[0]
        uid = reference_hit.id.split('/')[2]

        # Run two queries where everything is the same except the weight on the name query
        search_result = self.client.pif_multi_search(MultiQuery(
            queries=[
                PifSystemReturningQuery(
                    return_system=False,
                    score_relevance=True,
                    query=DataQuery(
                        system=PifSystemQuery(
                            uid=Filter(equal=uid)),
                        simple=reference_hit.system.names[0])),
                PifSystemReturningQuery(
                    return_system=False,
                    score_relevance=True,
                    query=DataQuery(
                        system=PifSystemQuery(
                            uid=Filter(equal=uid)),
                        simple=reference_hit.system.names[0],
                        simple_weight={'system.names': 2.0}))
            ]))

        # Make sure that the two weights are off by the correct amount
        unweighted_score = search_result.results[0].result.hits[0].score
        weighted_score = search_result.results[1].result.hits[0].score
        assert abs(weighted_score - unweighted_score) > 0.01
