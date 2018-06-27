import math

def convert_infinity_to_string(number):
    if math.isinf(number):
        if number < 0:
            return "-Infinity"
        if number > 0:
            return "Infinity"
    return number
