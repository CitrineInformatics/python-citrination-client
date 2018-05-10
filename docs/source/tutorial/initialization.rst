Initialization
==============

To instantiate ``CitrinationClient``, you will need to provide an
API key and the host URL of the Citrination site you are trying
to interact with.

API Key
-------

You can find your API key by navigation to ``https://citrination.com``,
or your private Citrination deployment, logging in, and using the menu
in the top right to visit your ``Account Settings`` page.

.. attention::
  Your API key allows you (and anyone who knows it) to access your account and your data. Use caution when storing it on your filesystem.

Host URL
--------

The second parameter to ``CitrinationClient`` instantiation is the URL of the Citrination site you are trying to interact with. By default it is ``https://citrination.com``, but you can pass in any Citrination site.

API Key From Environment
------------------------

Set the following values and ``CitrinationClient`` will pull in your authentication values from the environment:

* ``CITRINATION_API_KEY``
* ``CITRINATION_SITE``

API Key From .citrination Folder
--------------------------------

If you use PyCC to interact with multiple Citrination sites, or simply don't want to use your environment to specify authentication information for ``CitrinationClient``, you may use a credentials file to keep track of your Citrination API key.

#. Create a directory in your home folder called ``.citrination``
#. Create a file in the ``.citrination`` folder called ``credentials``

Use the following format to store credential information::

  default:
    api_key: my_default_profile_key
    site: my_default_profile_site
  my_site:
    api_key: my_test_profile_key
    site: https://mysite.citrination.com


In the absence of any other configuration, when you initialize ``CitrinationClient`` with no parameters, the credentials from the ``default`` stanza will be used.

To specify which credentials set will be used, set the environment variable ``CITRINATION_PROFILE`` to be equal to the name of the desired credentials stanza.


API Key In Direct Initialization
--------------------------------

You may also pass your API key in directly as a constructor argument to the client class (along with the Citrination site you prefer).

.. literalinclude:: /code_samples/general/initialization.py

.. attention::
  Remember to be careful not to share your API key accidentally by including it in a shared script!

Inititialization Mode Priority
------------------------------

The three methods of initialization outlined above are prioritized in the following order:

#. API Key In Direct Initialization
#. API Key From Environment
#. API Key From .citrination Folder

In other words, if you pass in an API key directly on instantiation, but also have it defined in the `.citrination/credentials` file, the API key you passed in directly will be used.