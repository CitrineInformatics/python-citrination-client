Models Client Examples
======================

The ``ModelsClient`` class encapsulates interactions with
trained models on Citrination.

Predict
-------

The ``.predict()`` method allows you to make a prediction with
a model by referencing the ID of a Data View.

The predict method takes a list of candidates, each of which is a dictionary of the inputs required for that data view. You may also specify the prediction method (either ``from_distribution`` or ``scalar``).

.. literalinclude:: /code_samples/models/predict.py

t-SNE
-----

You can retrieve the t-SNE analysis for a model by calling the
``.tsne()`` method with the ID of a data view with trained models.

The result of this call will be a ``Tsne`` instance which contains
projections for each of the the outputs for the models trained on the data view.

.. literalinclude:: /code_samples/models/tsne.py


Design
------

The ``.submit_design_run()`` method allows you to start a design run.

.. literalinclude:: /code_samples/models/design.py
