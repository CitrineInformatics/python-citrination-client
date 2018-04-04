Porting Dataset Manipulations
=============================

Retrieving a dataset file
-------------------------

The ``get_dataset_file`` method has the same signature it did, but now it returns an instance of the DatasetFile class rather than a python dictionary.

Also, note that this method is a member of the ``data`` subclient.

In the old version of PyCC, you might get the download URL for a file on Citrination like this:

.. code-block:: python

    file = client.get_dataset_file(1, "my_file.json")
    f["file"]["filename"] # my_file.json
    f["file"]["url"]      # the download URL for the file

Now, there is no need to navigate complex dictionary structures. Return values are all represented as ``DatasetFile`` instances.

.. code-block:: python
    
    # file is an instance of DatasetFile
    file = client.data.get_dataset_file(1, "my_file.json")
    f.filename # my_file.json
    f.url      # the download URL for the file

Creating And Updating Datasets
------------------------------

The main difference in creating and updating datasets is in the return values of those methods.

Additionally, these methods have been moved onto the ``data`` subclient, so make sure all calls to ``create_dataset`` and ``update_dataset`` through that client.

.. code-block:: python
  
  # creates a new dataset which is publicly available
  dataset = client.data.create_dataset(name="My New Dataset", public=True)
  dataset.id # the new dataset's ID
  dataset.name # "My New Dataset"

