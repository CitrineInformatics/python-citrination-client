import json

import pytest

from citrination_client import CategoricalDescriptor
from citrination_client.views.descriptors.real_descriptor import RealDescriptor


def test_categorical_descriptor():
    d = CategoricalDescriptor("categorical", ["0", "1"])
    assert d.as_dict() == dict(category="Categorical", descriptor_key="categorical", descriptorValues=["0", "1"])


def test_real_descriptor():
    d = RealDescriptor("band gap", lower_bound=-5, upper_bound=3.0, units="eV")
    assert d.as_dict() == dict(category="Real", units="eV", descriptor_key="band gap", lower_bound=-5, upper_bound=3.0)

    with pytest.raises(ValueError) as err:
        RealDescriptor("bg", 5, -5).as_dict()
