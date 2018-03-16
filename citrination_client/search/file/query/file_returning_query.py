from citrination_client.search.core.query.base_returning_query import BaseReturningQuery


class FileReturningQuery(BaseReturningQuery):
    """
    Query used to return information about files.
    """

    def __init__(self, query=None, from_index=None, size=None, random_results=None, random_seed=None,
                 score_relevance=None, return_max_score=None, timeout=None, max_content_highlights=None,
                 highlight_pre_tag=None, highlight_post_tag=None, **kwargs):
        """
        Constructor.

        :param query: One or more :class:`DataQuery` objects with the queries to run.
        :param from_index: Index of the first hit that should be returned.
        :param size: Total number of hits the should be returned.
        :param random_results: Whether to return a random set of records.
        :param random_seed: The random seed to use.
        :param score_relevance: Whether to use relevance scoring.
        :param return_max_score: Whether to return the maximum score.
        :param timeout: The number of milliseconds to wait for the query to execute.
        :param max_content_highlights: The maximum number of highlighted results to return.
        :param highlight_pre_tag: The tag to use at the beginning of a highlight.
        :param highlight_post_tag: The tag to use at the end of a highlight.
        """
        super(FileReturningQuery, self).__init__(
            query=query, from_index=from_index, size=size, random_results=random_results, random_seed=random_seed,
            score_relevance=score_relevance, return_max_score=return_max_score, timeout=timeout, **kwargs)
        self._max_content_highlights = None
        self.max_content_highlights = max_content_highlights
        self._highlight_pre_tag = None
        self.highlight_pre_tag = highlight_pre_tag
        self._highlight_post_tag = None
        self.highlight_post_tag = highlight_post_tag

    @property
    def max_content_highlights(self):
        return self._max_content_highlights

    @max_content_highlights.setter
    def max_content_highlights(self, max_content_highlights):
        self._max_content_highlights = max_content_highlights

    @max_content_highlights.deleter
    def max_content_highlights(self):
        self._max_content_highlights = None

    @property
    def highlight_pre_tag(self):
        return self._highlight_pre_tag

    @highlight_pre_tag.setter
    def highlight_pre_tag(self, highlight_pre_tag):
        self._highlight_pre_tag = highlight_pre_tag

    @highlight_pre_tag.deleter
    def highlight_pre_tag(self):
        self._highlight_pre_tag = None

    @property
    def highlight_post_tag(self):
        return self._highlight_post_tag

    @highlight_post_tag.setter
    def highlight_post_tag(self, highlight_post_tag):
        self._highlight_post_tag = highlight_post_tag

    @highlight_post_tag.deleter
    def highlight_post_tag(self):
        self._highlight_post_tag = None
