Data Views Client
=================

The ``DataViewClient`` is the section of PyCC that allows you to manage your data views
on Citrination. To access the data views client, instantiate ``CitrinationClient`` and read the ``data_views`` attribute:

.. literalinclude:: /code_samples/views/instantiation.py

Descriptor Keys
---------------

If you know the dataset identifier, but do not know the descriptor names, you can use the
``SearchTemplateClient#get_available_columns`` to get the descriptor keys.

Alternatively, you can use the ``DataViewsClient``, as an instance of the
``SearchTemplateClient`` is present on the ``DataViewsClient`` via ``client.search_template``.

.. literalinclude:: /code_samples/views/descriptor_keys.py

Creating a View
---------------

The ``DataViewClient`` allows you to create a machine learning configuration which in turn can be used
to make a data view via the API.  A builder is provided to simplify creating ML configurations.

.. literalinclude:: /code_samples/views/create_view.py

Once you have a data view id, you can use that id in the models client to run predictions or design.

Retrieving Model Reports
------------------------
The ``get_model_reports`` method allows you to fetch a subset of the model reports
data as JSON that one would normally see through the UI.

The following code snippet is using model reports from https://citrination.com/data_views/524/data_summary

.. literalinclude:: /code_samples/views/model_reports.py

Retrieving Relation Graphs
--------------------------
A relation graph shows you how your inputs, outputs, and latent variables are linked
by Citrination's machine learning models.

The ``get_relation_graph`` method returns a dict containing `nodes` and `edges`
intended to be passed to the ``plot`` function from the ``dagre_py.core`` module.

.. literalinclude:: /code_samples/views/relation_graphs.py

.. image:: /code_samples/views/relation_graph.png
  :width: 400
  :alt: Relation graph visualization using dagre_py
