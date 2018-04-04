Porting A File Upload
=====================

Here is an example of uploading a file using an older version of PyCC:

.. code-block:: python

    client.upload_file("example_data/instron.json", dataset_id)

The ``upload_file`` method has been deprecated in the new version of the client in favor of the ``upload`` method on the ``data`` client.

This method lets you specify the path of the file to upload, and optionally, the name that it should have on Citrination.

In other words, the following example uploads the same file as in the previous example, but tells Citrination to call it ``instron_example.json``, without the leading directory name:

.. code-block:: python

    client.data.upload(dataset_id, "example_data/instron.json", "instron_example.json")

If you do not specify the third argument to ``upload``, the original path will be used. The following snippet is equivalent to the first example:

.. code-block:: python

    client.data.upload(dataset_id, "example_data/instron.json")
