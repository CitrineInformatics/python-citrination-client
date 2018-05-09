Running v3.x.x and 4.0.0 in Parallel
====================================

If you are not ready to migrate all of your existing scripts to v4.0.0 of Python Citrination Client, you can take advantage of `virtual environments <http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv>`_ to only use v4.0.0 for new projects.

In a new project directory, create and activate a new virtual environment:

.. literalinclude:: /code_samples/migrating/activate_venv

Then install using ``pip`` the version of PyCC you would like to use for this project:

.. literalinclude:: /code_samples/migrating/pip_install

When you are done working with the new project, deactivate your virtual environment:

.. literalinclude:: /code_samples/migrating/deactivate

This will ensure that python scripts you run will only use ``4.0.0`` when you have a virtual environment activated that contains that version of PyCC.

Similarly, ensure that your older projects do not use the new version by specifying your preferred older version in the ``requirements.txt`` file.

