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

If you are using a version of PyCC older than 5.0.0 and would like to upgrade your scripts to the latest versions, please
note the following:

1. When building data views, you now have to specify upper and lower bounds.
2. When making certain prediction/design calls, things previously under `client.data_views` are now under `client.models`
3. You have to specify the subclient, e.g. `client.data.upload()` not just `client.upload()`


If you already have ``citrination-client`` installed (either in your virtual environment or your global set of ``pip`` packages), you can upgrade to v5.x like this:

.. code-block:: python

    pip install --upgrade citrination-client

If you do this in an existing project, be sure to update your ``requirements.txt`` file to point to version 5.1.1 or newer.


Module Documentation
--------------------

For detailed method documentation, consult the articles in this section.

.. toctree::
   :maxdepth: 2

   modules/modules