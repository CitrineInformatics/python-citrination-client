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

You may execute search queries which return individual records (equivalent to running search from the landing page on Citrination), or datasets by using the ``pif_search`` or ``dataset_search`` methods on the ``SearchClient`` respectively.

.. literalinclude:: /code_samples/search/pif_search.py

.. literalinclude:: /code_samples/search/dataset_search.py

Note that ``dataset_search`` does not return the contents of the datasets, but instead returns the metadata for datasets whose contents match the criteria applied by your search. In other words, if you pass a query to ``dataset_search`` which applies the criteria that matching records must contain a property called "Property Band gap", the resulting hits will be datasets which contain records satisfying that criteria.

Simple Query Generation
-----------------------

The search client provides a method called ``generate_simple_chemical_query`` which simplifies the interface for creating a new query. If you only need to apply a simple set of constraints, this can be a quick way to generate a query.

.. literalinclude:: /code_samples/search/generate_simple_query.py

