.. Python Citrination Client documentation master file, created by
   sphinx-quickstart on Tue Mar 13 10:48:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Citrination Client's documentation!
=====================================================


Tutorial
--------

Use the articles in this section to familiarize yourself with the basic usage of the Python Citrination Client.

.. toctree::
   :maxdepth: 2

   tutorial/tutorial

Upgrading
---------

If you are using a version of PyCC older than 6.0.0 and would like to upgrade your scripts to the latest versions, please
note the following:

Changes from 4.x to 5.x
^^^^^^^^^^^^^^^^^^^^^^^
1. When building data views, you now have to specify upper and lower bounds.
2. When making certain prediction/design calls, things previously under
   ``client.data_views`` are now under ``client.models``
3. You have to specify the subclient, e.g. ``client.data.upload()`` not just ``client.upload()``

Changes from 5.x to 6.x
^^^^^^^^^^^^^^^^^^^^^^^
1. New Features

  * **Custom Ingester Support** - allows for the usage of custom ingesters when
    uploading files. See ``DataClient.list_ingesters``, ``DataClient.upload_with_ingester``,
    and ``DataClient.upload_with_template_csv_ingester``, ``Ingester``, and ``IngesterList``
    classes.
  * **Model Reports** - first pass access to ``model settings``, ``feature importances``,
    and ``model performance metrics`` for data views with ML configured. See
    ``ViewsClient.get_model_reports`` and ``ModelReport`` class.
  * Version `6.1.0` adds `pif_version` support on ``DataClient#get_pif``, and a
    new method ``DataClient#get_pif_with_metadata``.
  * Version `6.2.0` adds ``ViewsClient#get_relation_graph`` for retrieving
    relation graphs from data views with ML configured

2. Deprecations

  * The **ModelsClient.get_data_view** method has been deprecated in favor of **ViewsClient.get**.
  * The **DataView** class has been removed - it was previously only used by ``ModelsClient.get_data_view``.

3. Minor Changes

  * Error message propagation for **404** errors - this should give more friendly error
    messages when resources being acted upon are not found. For example instead of
    the generic ``Resource Not Found`` message, one might get a ``Dataset 1234 was not found``
    message.

If you already have ``citrination-client`` installed (either in your virtual environment or your global set of ``pip`` packages), you can upgrade to v6.x like this:

.. code-block:: python

    pip install --upgrade citrination-client

If you do this in an existing project, be sure to update your ``requirements.txt`` file to point to version 6.0.0 or newer.


Module Documentation
--------------------

For detailed method documentation, consult the articles in this section.

.. toctree::
   :maxdepth: 2

   modules/modules
