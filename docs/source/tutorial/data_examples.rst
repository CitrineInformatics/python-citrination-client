Data Client
===========

The ``DataClient`` is the section of PyCC that allows you to manage your data
on Citrination. To access the data client, instantiate ``CitrinationClient`` and read the ``data`` attribute:

.. literalinclude:: /code_samples/data/instantiation.py

Uploading Files
---------------

The ``DataClient`` class exposes a method, ``.upload`` which allows you to
upload a file or a directory to a dataset on Citrination using the "default"
ingester. This method is useful for uploading JSON files that follow the PIF
schema, as well as files that do not require additional processing with a custom
ingester.

.. attention::
  For files that require additional processing, see the documentation for the
  ``upload_with_ingester`` and ``upload_with_template_csv_ingester`` sections.

This method is parameterized with the following values:

* **dataset_id** - The integer value of the ID of the dataset to which
  you will be uploading
* **source_path** - The path to the file or directory which you want to
  upload
* **dest_path** (optional) - The name of the file or directory as it should
  appear in Citrination.

Uploading a File To Citrination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following Python snippet demonstrates the approach for uploading a file with the relative path ``characterizations/CdTe1.json`` to dataset **1** on Citrination.

.. literalinclude:: /code_samples/data/upload_no_dest.py

In the web UI, this file will appear as ``CdTe1.json`` nested in a ``characterizations`` folder.

Uploading a File To Citrination Under a New Name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can specify the name a file should have once uploaded to Citrination by passing the second parameter to the ``.upload`` method.

.. literalinclude:: /code_samples/data/upload_file_with_dest.py

In the web UI, this file will appear as ``CadTel1.json`` at the top level of the dataset.

Uploading a Directory To Citrination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you pass a directory into the ``upload()`` method, all the files in the
directory will be recursively uploaded to the dataset. Their paths (relative to the directory specified), will remain intact.

.. attention::
   Files uploaded this way will be prefixed with the name of the parent
   directory that you originally specify. In other words, if ``upload()`` is
   called with the source path ``my_folder``, the dataset on Citrination will
   contain files prefixed with ``my_folder/``.

The following code sample uploads the ``characterizations/`` folder to dataset 1 on Citrination.

.. literalinclude:: /code_samples/data/upload_dir_no_dest.py

Uploading a Directory To Citrination Under a New Name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also specify that a folder be renamed when it is uploaded to Citrination. The following code sample uploads the contents of the ``characterizations/`` directory to a directory called ``january_characterizations`` on Citrination.

.. literalinclude:: /code_samples/data/upload_dir_with_dest.py

Selecting a Custom Ingester
---------------------------

Finding an Ingester by ID
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``list_ingesters`` method returns all of the custom ingesters available on
your Citrination deployment. It accepts no parameters, and returns an instance
of :class:`IngesterList`, which itself contains instances of :class:`Ingester`.

The unique field of an ``Ingester`` is its ``id``, so a particular ``Ingester``
can be located via the ``IngesterList#find_by_id`` method.

.. literalinclude:: /code_samples/data/find_ingester_by_id.py

Finding an Ingester by Searching its Attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't know the ``id`` of an ingester, you can also search through an
``IngesterList`` via the ``where`` method, which supports searching through a
variety of attributes that can be found in the ``Ingester.SEARCH_FIELDS`` constant.

.. literalinclude:: /code_samples/data/find_ingester_using_where.py

.. attention::
  Note that the `IngesterList#where` method returns a new instance of `IngesterList`,
  and requires indexing into the `IngesterList#ingesters` attribute to ultimately
  select an ingester.

Viewing an Ingester's Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have an `Ingester`, you can check its optional and required arguments
via the `Ingester#arguments` attribute.

.. literalinclude:: /code_samples/data/ingester_arguments.py

Uploading Data Using a Custom Ingester
--------------------------------------

The ``upload_with_ingester`` method allows for custom ingesters to be used when
uploading a file.

This method is parameterized with the following values:

* **dataset_id** - The integer value of the ID of the dataset to which
  you will be uploading
* **source_path** - The path to the file that you want to upload and for the
  ingester to then process
* **ingester** - The custom ingester you want to use
* **ingester_arguments** (optional) - Any ingester arguments you want to apply
  to the ingester - this should be a list of dicts that contain ``name`` and
  ``value`` keys
* **dest_path** (optional) - The name of the file or directory as it should
  appear in Citrination.

Ingesting Without Ingester Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following Python snippet demonstrates 2 approaches for uploading a file with
the relative path ``data/formulation.csv`` to dataset **1** on Citrination, one
with a specified destination path and one without (similar to how the ``upload``
method works). Both approaches utilize the ``Formulation CSV`` ingester with
``no ingester arguments``.

.. literalinclude:: /code_samples/data/custom_ingest_without_arguments.py

In the web UI, this file will appear as either ``formulation.csv`` nested in a
``data`` folder, or ``formulation.csv`` in the top level of the dataset
depending on whether or not the destination path was provided.

Ingesting With Ingester Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following Python snippet demonstrates 2 approaches for uploading a file with
the relative path ``experiments/data.xrdml`` to dataset **1** on Citrination, one
with a specified destination path and one without (similar to how the ``upload``
method works). Both approaches utilize the ``Citrine: XRD .xrdml`` ingester with
``a set of arguments provided``.

.. literalinclude:: /code_samples/data/custom_ingest_with_arguments.py

In the web UI, this file will appear as either ``data.xrdml`` nested in a
``experiments`` folder, or ``data.xrdml`` in the top level of the dataset
depending on whether or not the destination path was provided.

Uploading Using the Template CSV Ingester
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``upload_with_template_csv_ingester`` method abstracts away the logic of
finding the Template CSV ingester, since it is one of the more commonly used
ingesters. The same work can be accomplished by by finding the Template CSV
ingester and using the ``upload_with_ingester`` method.

This method is parameterized with the following values:

* **dataset_id** - The integer value of the ID of the dataset to which
  you will be uploading
* **source_path** - The path to the file that you want to upload and for the
  Template CSV to then process
* **dest_path** (optional) - The name of the file or directory as it should
  appear in Citrination.

The following Python snippet demonstrates 2 approaches for uploading a file with
the relative path ``experiments/data.csv`` to dataset **1** on Citrination, one
with a specified destination path and one without (similar to how the ``upload``
method works). Both approaches utilize the ``Citrine: XRD .xrdml`` ingester with
``a set of arguments provided``.

.. literalinclude:: /code_samples/data/upload_with_template_csv_ingester.py

In the web UI, this file will appear as either ``data.csv`` nested in a
``experiments`` folder, or ``data.csv`` in the top level of the dataset
depending on whether or not the destination path was provided.

Checking the Ingest Status of a Dataset
---------------------------------------

The ``get_ingest_status`` method can be used to check the ingestion status of
a dataset. It returns the string ``Processing`` when data is being ingested
or indexed, and returns the string ``Finished`` when no data is being processed.

.. literalinclude:: /code_samples/data/get_ingest_status.py

.. attention::
  Note that this method does not distinguish between successful and failed data
  ingestions - it is simply whether or not data is currently being processed
  for the dataset.

Retrieving Files
-----------------

There are two mechanisms for retrieving data from datasets on Citrination:

#. Request download URLs for previously uploaded files
#. Request the contents of a single record in PIF JSON format

File Download URLs
^^^^^^^^^^^^^^^^^^

The ``DataClient`` class provides several methods for retrieving files
from a dataset:

* ``get_dataset_files()``
* ``get_dataset_file()``

These two methods will each return URLs which can be used to download
one or more files in a dataset.

.. literalinclude:: /code_samples/data/file_urls.py

PIF Retrieval
^^^^^^^^^^^^^

A PIF record on Citrination can be retrieved using the `get_pif()` method.
The record will be returned as a PyPif Pif object.

.. literalinclude:: /code_samples/data/get_pif.py

Dataset Manipulation
--------------------

The ``DataClient`` class allows you to create datasets, update their names, descriptions, and permissions, and create new versions of them.

Creating a new version of a dataset bumps the version number on Citrination.
All files uploaded after this point will be uploaded to the new version.

The example below demonstrates how a files in old version of a dataset are not
included in the file count mechanism.

.. literalinclude:: /code_samples/data/version.py

It is also possible to toggle a dataset between being publicly accessible and private to your own user:

.. literalinclude:: /code_samples/data/permissions.py
