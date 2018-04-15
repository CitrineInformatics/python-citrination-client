from citrination_client.design.constraints import *
from citrination_client.errors import *

def test_real_value_constraint():
    """
    Tests that a real constraint will only serialize
    with min and max OR value but not both

    Also tests that the constraint 
    """

    c_value = RealValueConstraint(descriptor="Property",value=3)
    mapped_c_value = c_value.to_dict()

    assert mapped_c_value["name"] == "Property"
    assert mapped_c_value["type"] == "real"
    assert mapped_c_value["options"]["value"] == 3

def test_real_range_constraint():

    c = RealRangeConstraint(descriptor="Property",minimum=1,maximum=2)
    mapped_c_range = c.to_dict()

    assert mapped_c_range["name"] == "Property"
    assert mapped_c_range["type"] == "real"
    assert mapped_c_range["options"].get("min") is 1
    assert mapped_c_range["options"].get("max") is 2

def test_categorical_constraint():
    """
    Tests that a categorical constraint converts to a map
    properly: type is correct, name is correct, and the categories
    array is preserved
    """
    categories = ["A", "B", "C"]
    c = CategoricalConstraint(descriptor="Property 1", categories=categories)

    mapped_c = c.to_dict()

    assert mapped_c["type"] is "categorical"
    assert mapped_c["name"] is "Property 1"
    assert mapped_c["options"]["categories"] is categories

def test_number_of_elements_constraint():
    """
    Tests that the number of elements constraint converts
    correctly to a map with the min and max properties preserved
    """
    descriptor = "Property B"
    minimum = 1
    maximum = 2

    c = NumberOfElementsConstraint(descriptor=descriptor,
                                   minimum=minimum,
                                   maximum=maximum)

    mapped_c = c.to_dict()

    assert mapped_c["type"] is "numberOfElementsConstraint"
    assert mapped_c["name"] is descriptor
    assert mapped_c["options"]["min"] is minimum
    assert mapped_c["options"]["max"] is maximum

def test_elemental_composition_constraint():
    """
    Tests that the elemental composition constraint is correctly
    converted to a map with min, max, and elements preserved
    """
    descriptor = "Property B"
    minimum = 1
    maximum = 2
    elements = ["Mg", "C"]

    c = ElementalCompositionConstraint(descriptor=descriptor,
                                       elements=elements,
                                       minimum=minimum,
                                       maximum=maximum)

    mapped_c = c.to_dict()

    assert mapped_c["type"] is "elementalCompositionConstraint"
    assert mapped_c["name"] is descriptor
    assert mapped_c["options"]["min"] is minimum
    assert mapped_c["options"]["max"] is maximum
    assert mapped_c["options"]["elements"] is elements    

def test_elemental_inclusion_constraint():
    """
    Tests that the elemental inclusion constraint is correctly
    converted to a map with elements and logic preserved

    Also tests that logic must be one of the three acceptable values
    """
    descriptor = "Property B"
    elements = ["Mg", "C"]

    try:
        asdf = "asdf"
        c = ElementalInclusionConstraint(descriptor=descriptor, elements=elements, logic=asdf)
    except CitrinationClientError:
        assert True

    try:
        should = "should"
        ElementalInclusionConstraint(descriptor=descriptor, elements=elements, logic=should)
        must = "must"
        ElementalInclusionConstraint(descriptor=descriptor, elements=elements, logic=must)
        exclude = "exclude"
        ElementalInclusionConstraint(descriptor=descriptor, elements=elements, logic=exclude)
        assert True

    except CitrinationClientError:
        assert False

    logic="should"
    c = ElementalInclusionConstraint(descriptor=descriptor, elements=elements, logic=logic)

    mapped_c = c.to_dict()

    assert mapped_c["type"] is "elementalInclusionConstraint"
    assert mapped_c["name"] is descriptor
    assert mapped_c["options"]["logic"] is logic
    assert mapped_c["options"]["elements"] is elements    