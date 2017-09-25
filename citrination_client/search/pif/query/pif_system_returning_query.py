from citrination_client.search.core.query.base_returning_query import BaseReturningQuery


class PifSystemReturningQuery(BaseReturningQuery):
    """
    Query used to return information about PIFs.
    """

    def __init__(self, query=None, extraction_sort=None, from_index=None, size=None, random_results=None,
                 random_seed=None, score_relevance=None, return_max_score=None, return_system=None, add_latex=None,
                 return_extracted_path=None, unwrap_single_value_extractions=None, **kwargs):
        """
        Constructor.

        :param query: One or more :class:`DataQuery` objects with the queries to run.
        :param extraction_sort: A single :class:`ExtractionSort` object for sorting.
        :param from_index: Index of the first hit that should be returned.
        :param size: Total number of hits the should be returned.
        :param random_results: Whether to return a random set of records.
        :param random_seed: The random seed to use.
        :param score_relevance: Whether to use relevance scoring.
        :param return_max_score: Whether to return the maximum score.
        :param return_system: Whether to return the matched PIF systems.
        :param add_latex: Whether to add latex formatting where possible in results.
        :param return_extracted_path: Whether to return the path in PIFs for extracted values.
        :param unwrap_single_value_extractions: Whether to unwrap extracted values when they are lists with one value.
        """
        super(PifSystemReturningQuery, self).__init__(
            query=query, extraction_sort=extraction_sort, from_index=from_index, size=size,
            random_results=random_results, random_seed=random_seed, score_relevance=score_relevance,
            return_max_score=return_max_score, **kwargs)
        self._return_system = None
        self.return_system = return_system
        self._add_latex = None
        self.add_latex = add_latex
        self._return_extracted_path = None
        self.return_extracted_path = return_extracted_path
        self._unwrap_single_value_extractions = None
        self.unwrap_single_value_extractions = unwrap_single_value_extractions

    @property
    def return_system(self):
        return self._return_system

    @return_system.setter
    def return_system(self, return_system):
        self._return_system = return_system

    @return_system.deleter
    def return_system(self):
        self._return_system = None

    @property
    def add_latex(self):
        return self._add_latex

    @add_latex.setter
    def add_latex(self, add_latex):
        self._add_latex = add_latex

    @add_latex.deleter
    def add_latex(self):
        self._add_latex = None

    @property
    def return_extracted_path(self):
        return self._return_extracted_path

    @return_extracted_path.setter
    def return_extracted_path(self, return_extracted_path):
        self._return_extracted_path = return_extracted_path

    @return_extracted_path.deleter
    def return_extracted_path(self):
        self._return_extracted_path = None

    @property
    def unwrap_single_value_extractions(self):
        return self._unwrap_single_value_extractions

    @unwrap_single_value_extractions.setter
    def unwrap_single_value_extractions(self, unwrap_single_value_extractions):
        self._unwrap_single_value_extractions = unwrap_single_value_extractions

    @unwrap_single_value_extractions.deleter
    def unwrap_single_value_extractions(self):
        self._unwrap_single_value_extractions = None
