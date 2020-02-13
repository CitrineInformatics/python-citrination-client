Data Views Client
=================

The ``DataViewsClient`` is the section of PyCC that allows you to manage your
data views on Citrination. To access the data views client, instantiate
``CitrinationClient`` and read the ``data_views`` attribute, or just import
the ``DataViewsClient`` and instantiate it directly:

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

The ``DataViewsClient`` allows you to create a machine learning configuration which in turn can be used
to make a data view via the API.  A builder is provided to simplify creating ML configurations.

Once you have a data view id, you can use that id in the ``ModelsClient`` to run predictions or design.

Creating Model Configuration for Your Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The ``DataViewsClient#create_ml_configuration_from_datasets`` method will create
a configuration object for you, suitable for passing into the ``create`` or
``update`` methods. While the configuration object returned might contain more
descriptors than you want, it's a great starting point, and can easily be modified
to suit your needs.

By passing in the dataset ids that you're interested in, Citrination will determine
(within limitations) which ``descriptor keys`` (``properties``, ``conditions``,
``process steps``, and ``process step details``) are present in those datasets.

It will then do some analysis of that data, and suggest ``descriptor`` and
``role`` configurations for each of those ``descriptor keys``, returning back to
you a dictionary that can be used to create or update a view.

.. literalinclude:: /code_samples/views/fetching_ml_config_defaults_1.py

At this point, we have a configuration object with all of the descriptors that
could be created from the datasets we selected. Suppose we are only interested in
``formula``, ``band gap``, ``color``, and some related ``temperature`` conditions.
We can modify the existing configuration object to filter it down to those
``descriptors`` and ``roles``.

.. literalinclude:: /code_samples/views/fetching_ml_config_defaults_2.py

This dictionary has now been paired down to only the descriptors we are interested
in. It can now be modified further, or used to create/update a view.

.. literalinclude:: /code_samples/views/fetching_ml_config_defaults_3.py

Using the DataViewBuilder
^^^^^^^^^^^^^^^^^^^^^^^^^

Under the hood, the ``DataViewsClient#create_ml_configuration_from_datasets`` method
leverages the ``DataViewBuilder`` to create a configuration object. This class
can also be used to build your own configuration object from scratch, by providing
``dataset ids`` and ``descriptors``.

This path can be quicker than using the ``DataViewsClient#create_ml_configuration_from_datasets``
method in an automated workflow if you already know the descriptors that you want to use.

When building data views through the UI, or using the configuration object returned
from the ``DataViewBuilder``, the ``roles`` of each of those descriptors are
interpreted by Citrination, and the machine learning libraries determine how
many models to generate, and how to apply your inputs, outputs, and latent variables.

.. literalinclude:: /code_samples/views/data_view_builder.py

The following relation graph was generated from the sample code above:

.. image:: /code_samples/views/data_view_builder_relation_graph.png
  :width: 600
  :alt: Relation graph visualization using dagre_py

Using the AdvancedDataViewBuilder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the data view generated in the ``DataViewBuilder`` example above, specifying:

* `formula`, `Temperature (Property Band gap)`, and `Temperature (Property Color)` as ``inputs``,
* `Property Band gap` as a ``latentVariable``, and
* `Property Color` as an ``output``,

resulted in 3 models being generated, represented by the following relations:

.. literalinclude:: /code_samples/views/data_view_builder_relations.py

The ``AdvancedDataViewBuilder`` gives you the freedom to specify the ``relations``
between all of your descriptors. Building on the ``DataViewBuilder`` example,
say we want to have the following relations build a system of 5 models for our
data view, instead of the 3 models that were created when we used the ``DataViewBuilder``:

.. literalinclude:: /code_samples/views/advanced_data_view_builder_relations.py

In this case, the ``role`` of each descriptor is essentially the same as before,
but applied in a different model configuration.

Similar to the ``DataViewBuilder``, the ``AdvancedDataViewBuilder`` requires
``descriptors``. In this example, we'll select the descriptor dictionaries that
we are interested in from an auto-generated config object, similar to what is
shown in the ``Creating Model Configuration for Your Data`` section.

.. literalinclude:: /code_samples/views/advanced_data_view_builder_1.py

Next, we initialize the ``AdvancedDataViewBuilder``, add the descriptors via
the ``#add_raw_descriptor`` method, and then add relations via the
``#add_relation`` method.

.. literalinclude:: /code_samples/views/advanced_data_view_builder_2.py

At this point, the advanced data view builder object is ready to be used to
create or update a data view.

.. literalinclude:: /code_samples/views/advanced_data_view_builder_3.py

Checking out the resulting relation graph, we can see that 5 models have been
generated.

.. image:: /code_samples/views/advanced_data_view_builder_relation_graph.png
  :width: 600
  :alt: Relation graph visualization using dagre_py

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
