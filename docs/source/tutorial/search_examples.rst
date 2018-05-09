.. attention::
   The search interface for Citrination is powerful but complex. This guide is still a work in progress.

Search Client Examples
======================

The ``SearchClient`` class allows you to run search queries against
Citrination. The search client utilizes a deeply recursive query structure
that enables complex sets of criteria to be applied.

For more detailed information about the structure of search queries, consult the documentation found here: (https://citrineinformatics.github.io/api-documentation/#tag/search

Basic Usage
-----------

To execute a search against Citrination, build a search query and pass it to either ``pif_search`` or ``dataset_search`` on the ``SearchClient``.

.. literalinclude:: /code_samples/search/basic_usage.py


Record vs Dataset Search
---------------------

You may execute search queries which return individual records (equivalent to running search from the landing page on Citrination), or datasets by using the ``pif_search`` or ``dataset_search`` methods on the ``SearchClient`` respectively. Note that ``dataset_search`` does not return the contents of the datasets, but instead returns the metadata for datasets whose contents match the criteria applied by your search. In other words, if you pass a query to ``dataset_search`` which applies the criteria that matching records must contain a property called "Property Band gap", the resulting hits will be datasets which contain records satisfying that criteria. Additionally, in order to search for records, you will need to use ``PifSystemReturningQuery`` whereas to return datasets, you will need to use ``DatasetReturningQuery``.