Examples
========

Structure
---------

Versions of PyCC greater than ``4.0.0`` are structured hierarchically
such that ``CitrinationClient`` is a container for context specific
subclients. At any point in the client hierarchy, you can see which
methods and subclients are currently available by calling ``.__repr__()`` 
on the current client.

.. literalinclude:: code_samples/general/client_serialization.py

Initialization
--------------

To instantiate ``CitrinationClient``, you will need to provide an
API key and the host URL of the Citrination site you are trying
to interact with.

To avoid saving your API key as plaintext in a file somewhere, store 
it as an environment variable.

.. literalinclude:: code_samples/general/initialization.py

Data Client
-----------

.. literalinclude:: code_samples/data/upload.py