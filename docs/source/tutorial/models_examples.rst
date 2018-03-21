Models Client Examples
======================

The ``ModelsClient`` class encapsulates interactions with
trained models on Citrination.

Predict
-------

The ``.predict()`` method allows you to make a prediction with
a model by referencing the ID of a Data View.

Custom Predict
--------------

The ``.predict_custom()`` method allows you to make a prediction
with a custom model, referenced by its name.

t-SNE
-----

You can retrieve the t-SNE analysis for a model by calling the
``.tsne()`` method with the ID of a data view with trained models.