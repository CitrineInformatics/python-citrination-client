Porting A Prediction
====================

Here is an example of a prediction made with an older version of PyCC:

.. code-block:: python

    inputs = [{"Chemical formula": "AlCu"},]
    resp = client.predict("27", inputs)
    prediction = resp['candidates'][0]['Density']

In v4.0.0, predictions are submitted the same way, but using the ``models`` client.

The main differences in this case are in the result returned by the predict call. Rather than returning a plain Python dictionary, the result is represented as an instance of the ``PredictionResult`` class:

.. code-block:: python

    inputs = [{"Chemical formula": "AlCu"},]
    result = client.models.predict("27", inputs)

    # now result is an instance of PredictionResult
    prediction = result.get_value("Density")
    
    # and it allows you to access predicted properties
    # which each each have value and loss attributes
    prediction.value # 6.01721779167
    prediction.loss  # 0.69396638928