Introduction
============

This guide will cover some common PyCC functions their basic use cases.

The biggest structural difference between older versions of PyCC and v4.0.0 is that the client is divided into sub-clients which each handle a specific set of functionality. Specifically, an instance of ``CitrinationClient`` will have as members ``data``, ``models``, and ``search``, which each expose subsets of the functionality.

.. attention::
  While it is recommended that you access methods on the subclients directly (e.g. ``client.data.update_dataset``), those methods are also available on the top level client (e.g. ``client.update_dataset``) to enable simpler backwards compatability. In a future version of the client, those top level methods will be deprecated so, whenever possible, access subclient methods directly.