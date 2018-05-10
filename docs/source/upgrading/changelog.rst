Changelog
=========

Data
----

* ``upload`` now returns an ``UploadResult`` instance rather than a dictionary
* ``upload_file`` has been removed, in favor of ``upload``
* ``list_files`` now returns a list of strings rather than a dictionary with a ``files`` key
* ``get_matched_dataset_files`` has been removed
* ``get_dataset_files`` now takes the following parameters:

  * ``glob`` - a pattern to match for the returned files
  * ``is_dir`` - a flag to indicate that the pattern is a leading directory name
  * ``version_number`` - optionally, the version of the dataset to retrieve files from. If left out, the latest version will be used

* ``get_dataset_files`` now returns a list of ``DatasetFile`` objects
* ``get_dataset_file`` now returns a ``DatasetFile`` object
* ``get_pif`` now returns an instance of a ``Pif`` object from the PyPif library
* ``create_data_set`` renamed to ``create_dataset``
* ``update_dataset`` and ``create_dataset`` now let you specify permissions using a boolean value for the ``public`` flag
* ``update_dataset`` and ``create_dataset`` now return instances of the ``Dataset`` class
* ``create_dataset_version`` now returns an instance of ``DatasetVersion``

Models
------

* ``predict_custom`` has been removed
* ``predict`` now returns an instance of ``PredictionResult``
* ``tsne`` now returns an instance of ``Tsne``

Search
------

* ``simple_chemical_search`` has been removed and replaced with ``generate_simple_chemical_query`` which generates a query object which can then be passed in to ``pif_search``
* ``dataset_search`` and ``pif_search`` handle pagination automatically now. The result set you receive will be complete or adhere strictly to your parameterization with the ``size`` and ``from`` attributes