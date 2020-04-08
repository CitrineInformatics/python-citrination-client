import pytest

from citrination_client.views.data_view_builder import DataViewBuilder
from citrination_client.views.descriptors.real_descriptor import RealDescriptor
from citrination_client.client import CitrinationClient
from citrination_client.views.descriptors import FormulationDescriptor
from os import environ


def test_add_descriptor():
    builder = DataViewBuilder()

    bandgap = RealDescriptor("band gap", lower_bound=-1, upper_bound=1)

    builder.add_descriptor(bandgap, "output", True)
    config = builder.build()

    assert config["group_by"] == ["band gap"]
    assert config["descriptors"] == [bandgap.as_dict()]
    assert config["roles"] == {"band gap": "output"}

    # Make sure duplicates raise an error
    with pytest.raises(ValueError) as err:
        builder.add_descriptor(RealDescriptor("band gap", lower_bound=-1, upper_bound=1), "input")


@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://citrination.com",
                    reason="Formulation test only supported on open citrination")
def test_formulation_descriptor():
    client = CitrinationClient(environ["CITRINATION_API_KEY"])

    builder = DataViewBuilder()
    builder.dataset_ids([188718])

    # The new thing..
    builder.add_formulation_descriptor(FormulationDescriptor("Formulation (idealMassPercent)"), client.data_views)
    builder.add_descriptor(RealDescriptor("Property pigment blue", 0, 600))
    builder.add_descriptor(RealDescriptor("Property pigment red", 0, 600))
    builder.add_descriptor(RealDescriptor("Property pigment green", 0, 600))

    builder.add_descriptor(RealDescriptor("Property formulation blue", 0, 600))
    builder.add_descriptor(RealDescriptor("Property formulation red", 0, 600))
    builder.add_descriptor(RealDescriptor("Property formulation green", 0, 600))

    config = builder.build()

    assert config["roles"]["Formulation (idealMassPercent)"] == "input"
    assert config["roles"]["component type"] == "ignore"
    assert config["roles"]["name"] == "ignore"
    assert config["roles"]["% P1 (mass, ideal)"] == "ignore"

    p1_share_present = False
    name_present = False
    pigment_blue_present = False

    print(config["descriptors"])

    for desc in config["descriptors"]:
        if desc["descriptor_key"] == "% P1 (mass, ideal)":
            p1_share_present = True
        if desc["descriptor_key"] == "name":
            name_present = True
        if desc["descriptor_key"] == "Property pigment blue":
            pigment_blue_present = True

    assert p1_share_present
    assert name_present
    assert pigment_blue_present


test_formulation_descriptor()