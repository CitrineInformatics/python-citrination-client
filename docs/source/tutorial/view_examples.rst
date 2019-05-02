Data Views Client
=================

The ``DataViewClient`` is the section of PyCC that allows you to manage your data views
on Citrination. To access the data views client, instantiate ``CitrinationClient`` and read the ``data_views`` attribute:

.. literalinclude:: /code_samples/views/instantiation.py

Descriptor Keys
---------------

If you know the dataset identifier, but do not know the descriptor names, you can use the
SearchTemplateClient to get the descriptor keys.

.. literalinclude:: /code_samples/views/descriptor_keys.py

Creating a view
---------------

The ``DataViewClient`` allows you to create a machine learning configuration which in turn can be used
to make a data view via the API.  A builder is provided to simplify creating ML configurations.

.. literalinclude:: /code_samples/views/create_view.py

Once you have a data view id, you can use that id in the models client to run predictions or design.
