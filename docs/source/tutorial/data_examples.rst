Data Client
===========

The ``DataClient`` is the section of PyCC that allows you to manage your data
on Citrination. To access the data client, instantiate ``CitrinationClient`` and read the ``data`` attribute:

.. literalinclude:: /code_samples/data/instantiation.py

Uploading Files
---------------

The ``DataClient`` class exposes a method, ``.upload`` which
allows you to upload a file or a directory to a dataset on
Citrination.

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
