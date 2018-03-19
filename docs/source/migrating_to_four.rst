Migrating To PyCC v4.0.0
========================

Client Structure
----------------

Versions of PyCC greater than ``4.0.0`` are structured hierarchically
such that ``CitrinationClient`` is a container for context specific
subclients. At any point in the client hierarchy, you can see which
methods and subclients are currently available by calling ``.__repr__()`` 
on the current client.

.. literalinclude:: code_samples/general/client_serialization.py

The consequence of this is that all method invocations on the client must be directed to the appropriate subclient. In other words, rather than calling ``upload`` on the ``CitrinationClient`` instance, you must call it on the ``DataClient`` accessed by calling ``.data`` on the ``CitrinationClient``.

Error Handling
--------------

In previous version of PyCC, errors which occurred during interactions with Citrination were bubbled directly up with no intermediate error handling. In version ``4.0.0`` and above, interaction errors are represented by exceptions which extend ``CitrinationClientError``.

* ``APIVersionMismatchException`` - An error indicating that the Citrination API has been upgraded. If this error is thrown, check for new versions of PyCC. If none is available, contact Citrine for assistance.
* ``FeatureUnavailableException`` - Indicates that the requested feature is not enabled on the Citrination deployment you are using.
* ``UnauthorizedAccessException`` - Indicates that you attempted to access a resource (usually a data view or dataset) to which you do not have authorized access. Ensure you are using the correct resource ID, or contact the owner of the resource to be given access to the resource.
* ``CitrinationServerErrorException`` - Indicates that there was a problem on Citrination processing your request. The best solution here is to check the parameterization of your PyCC method invocation for correctness and try again at a later time.

Response Signatures
-------------------

In version ``4.0.0``, PyCC methods all return primitives or instances of classes representative of the Citrination resources it interacts with. In prior versions of PyCC, method return values depended largely on the method being invoked and were not consistent.

Method Removals
---------------

The following methods which were present on the old ``CitrinationClient`` class have been removed:

* ``upload_file`` - Redundant with ``upload`` on the ``DataClient``
* ``search`` - Redundant with ``pif_search`` on the ``SearchClient``
* ``get_matched_dataset_files`` - Redundant with ``get_dataset_files`` on the ``DataClient``
