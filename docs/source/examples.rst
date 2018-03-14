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


Data Client
-----------


Models Client
-------------


