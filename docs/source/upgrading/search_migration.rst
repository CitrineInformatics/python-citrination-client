Porting A Search Query
======================

Here is an example of executing a PIF search query against Citrination:

.. code-block:: python

    query_dataset = PifSystemReturningQuery(size=5, 
                                            query=DataQuery(
                                                dataset=DatasetQuery(
                                                    id=Filter(equal=str(my_dataset_id))
                                             )))
    query_result = client.pif_search(query_dataset)

The only difference required in the new version of the client is to use make sure you are calling the ``pif_search`` method on the ``search`` client.

.. code-block:: python

    query_dataset = PifSystemReturningQuery(size=5, 
                                            query=DataQuery(
                                                dataset=DatasetQuery(
                                                    id=Filter(equal=str(my_dataset_id))
                                             )))
    query_result = client.search.pif_search(query_dataset)

.. attention::
  While it is recommended that you access methods on the ``search`` client directly, this is not strictly required in order to enable backwards compatability with existing scripts. This functionality will be deprecated in the future, so please access the client directly whenever possible.