import pytest

from citrination_client import CategoricalDescriptor
from citrination_client.views.descriptors import RealDescriptor, IntDescriptor


def test_categorical_descriptor():
    d = CategoricalDescriptor("categorical", ["0", "1"])
    assert d.as_dict() == dict(category="Categorical", descriptor_key="categorical", descriptor_values=["0", "1"])


def test_real_descriptor():
    d = RealDescriptor("band gap", lower_bound=-5, upper_bound=3.0, units="eV")
    assert d.as_dict() == dict(category="Real", units="eV", descriptor_key="band gap", lower_bound=-5, upper_bound=3.0)

    with pytest.raises(ValueError) as err:
        RealDescriptor("bg", 5, -5).as_dict()


def test_int_descriptor():
    descriptor_key = "Ingredient count"
    lower_bound = 0
    upper_bound = 10
    units = ""
    d = IntDescriptor(descriptor_key, lower_bound=lower_bound, upper_bound=upper_bound, units=units)

    expected = dict(
        category="Integer",
        descriptor_key=descriptor_key,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        units=units
    )
    assert d.as_dict() == expected

    with pytest.raises(ValueError) as err:
        IntDescriptor("", 5, -5).as_dict()
