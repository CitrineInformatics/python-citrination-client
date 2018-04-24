Introduction
============

This guide will cover some common PyCC functions and how to migrate the use of those functions on old version of the client to the new version of the client.

The biggest structural difference between older versions of PyCC and v4.0.0 is that the client is divided into sub-clients which each handle a specific set of functionality. Specifically, an instance of ``CitrinationClient`` will have as members ``data``, ``models``, and ``search``, which each expose subsets of the functionality.

.. attention::
  While it is recommended that you access methods on the subclients directly (e.g. ``client.data.update_dataset``), those methods are also available on the top level client (e.g. ``client.update_dataset``) to enable simpler backwards compatability.