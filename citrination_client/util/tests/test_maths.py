from citrination_client.util.maths import *

def test_negative_infinity_becomes_string():
    infinity = float("-inf")
    assert "-Infinity" == convert_infinity_to_string(infinity)

def test_positive_infinity_becomes_string():
    infinity = float("+inf")
    assert "Infinity" == convert_infinity_to_string(infinity)

def test_random_number_doesnt_change():
    number = 1
    assert number == convert_infinity_to_string(number)
