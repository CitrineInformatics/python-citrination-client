import pytest

from citrination_client.views.data_view_builder import DataViewBuilder
from citrination_client.views.descriptors.real_descriptor import RealDescriptor


def test_add_descriptor():
    builder = DataViewBuilder()

    bandgap = RealDescriptor("band gap", lower_bound=-1, upper_bound=1)

    builder.add_descriptor(bandgap, "output", True)
    config = builder.build()

    assert config["group_by"] == ["band gap"]
    assert config["descriptors"] == [bandgap]
    assert config["roles"] == {"band gap": "output"}

    # Make sure duplicates raise an error
    with pytest.raises(ValueError) as err:
        builder.add_descriptor(RealDescriptor("band gap"), "input")

