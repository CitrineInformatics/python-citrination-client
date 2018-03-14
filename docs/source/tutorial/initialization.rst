Initialization
==============

To instantiate ``CitrinationClient``, you will need to provide an
API key and the host URL of the Citrination site you are trying
to interact with.

You can find your API key by navigation to ``https://citrination.com``,
or your private Citrination deployment, logging in, and using the menu
in the top right to visit your ``Account Settings`` page.

.. attention::
  Your API allows you (and anyone who knows it) to access your account.
  To avoid saving your API key as plaintext in a file somewhere, store 
  it as an environment variable.

.. literalinclude:: code_samples/general/initialization.py