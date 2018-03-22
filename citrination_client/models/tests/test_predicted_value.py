from citrination_client.models import PredictedValue

def test_can_crud_value():
    original_key = "my_key"
    original_value = 2
    original_loss = 0.3
    pv =  PredictedValue(original_key, original_value, loss=original_loss)
    key = "other_key"
    assert pv.key is original_key
    pv.key = key
    assert pv.key is key
    del(pv.key)
    assert pv.key is None

def test_can_crud_key():
    original_key = "my_key"
    original_value = 2
    original_loss = 0.3
    pv =  PredictedValue(original_key, original_value, loss=original_loss)
    value = 3
    assert pv.value is original_value
    pv.value = value
    assert pv.value is value
    del(pv.value)
    assert pv.value is None

def test_can_crud_loss():
    original_key = "my_key"
    original_value = 2
    original_loss = 0.3
    pv =  PredictedValue(original_key, original_value, loss=original_loss)
    loss = 3
    assert pv.loss is original_loss
    pv.loss = loss
    assert pv.loss is loss
    del(pv.loss)
    assert pv.loss is None