class SimpleSearchTemplateBuilder(object):
    """
    A simple interface for building a search template
    """

    def __init__(self):
        pass

    def build(self, columns, dataset_ids):
        search_template = self.__generate_search_template(dataset_ids)
        return self.__prune_search_template(search_template,columns)


