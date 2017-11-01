from os import environ

from citrination_client import *


class TestDatasetQuery():

    @classmethod
    def setup_class(cls):
        cls.client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])

    def test_full_dataset_query(self):
        """Test a public dataset query with every option on"""
        query = DatasetReturningQuery(
            size=8,
            score_relevance=True,
            count_pifs=True)
        result = self.client.dataset_search(query)

        assert len(result.hits) == 8, "Number of hits didn't match query size"
        assert result.took > 0, "Result shouldn't have been instant"
        assert result.total_num_hits > 10000, "The number of results is too low"
        for hit in result.hits:
            assert len(hit.id) > 0, "Returned empty id"
            assert len(hit.name) > 0, "Returned empty name"
            assert len(hit.email) > 0, "Returned empty email"
            assert hit.num_pifs >= 0, "Dataset had no pifs"
            assert hit.score > 0, "Score not greater than zero"

    def test_dataset_search(self):
        response = self.client.dataset_search(DatasetReturningQuery(
            size=0,
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal='151278')))))
        assert 1 == response.total_num_hits
