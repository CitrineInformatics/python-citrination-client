from citrination_client.design.constraints import *
from citrination_client.errors import *

def test_real_value_constraint():
    """
    Tests that a real constraint will only serialize
    with min and max OR value but not both
    """
    prop = "Property Band gap"
    c_value = RealValueConstraint(name=prop,value=3)
    mapped_c_value = c_value.to_dict()

    assert mapped_c_value["name"] == prop
    assert mapped_c_value["type"] == "real"
    assert mapped_c_value["options"]["value"] == 3

def test_real_range_constraint():

    prop = "Property Band gap"
    c = RealRangeConstraint(name=prop,minimum=1,maximum=2)
    mapped_c_range = c.to_dict()

    assert mapped_c_range["name"] == prop
    assert mapped_c_range["type"] == "real"
    assert mapped_c_range["options"].get("min") == 1.0
    assert mapped_c_range["options"].get("max") == 2.0

def test_real_range_constraint_validation():
    """
    Tests that minimum and maxmimum values are validated correctly
    on initialization of RealRangeConstraint
    """

    # Test valid values OK
    minimum = 1
    maximum = 2
    c = RealRangeConstraint(name="Property Band gap",minimum=minimum,maximum=maximum)

    # Test minimum must be less than maximum
    minimum = 3
    maximum = 2
    try:
        c = RealRangeConstraint(name="Property Band gap",minimum=minimum,maximum=maximum)
        assert False, "RealRangeConstraint should require that minimum be less than maxmimum"
    except CitrinationClientError:
        pass

    # Test values must be castable to float
    minimum = {}
    maximum = 2
    try:
        c = RealRangeConstraint(name="Property Band gap",minimum=minimum,maximum=maximum)
        assert False, "RealRangeConstraint should require that minimum and maximum be castable to floats"
    except CitrinationClientError:
        pass

def test_categorical_constraint():
    """
    Tests that a categorical constraint converts to a map
    properly: type is correct, name is correct, and the categories
    array is preserved
    """
    categories = ["Blue", "Red", "Yellow"]
    prop = "Property Color"
    c = CategoricalConstraint(name=prop, accepted_categories=categories)

    mapped_c = c.to_dict()

    assert mapped_c["type"] is "categorical"
    assert mapped_c["name"] is prop
    assert mapped_c["options"]["categories"] is categories

def test_elemental_composition_constraint():
    """
    Tests that the elemental composition constraint is correctly
    converted to a map with min, max, and elements preserved
    """
    name = "Property Band gap"
    minimum = 1
    maximum = 2
    elements = ["Ga", "N"]

    c = ElementalCompositionConstraint(name=name,
                                       elements=elements,
                                       minimum=minimum,
                                       maximum=maximum)

    mapped_c = c.to_dict()

    assert mapped_c["type"] is "elementalCompositionConstraint"
    assert mapped_c["name"] is name
    assert mapped_c["options"]["min"] is minimum
    assert mapped_c["options"]["max"] is maximum
    assert mapped_c["options"]["elements"] is elements

def test_elemental_composition_constraint_validation():
    """
    Tests that the elemental composition constraint cannot be
    instantiated with invalid minimum and maximum values
    """
    name = "Property Band gap"
    elements = ["Ga", "N"]

   # Minimum can't be less than 0
    minimum = -1
    maximum = 2

    try:
        c = ElementalCompositionConstraint(name=name,
                                           elements=elements,
                                           minimum=minimum,
                                           maximum=maximum)
        assert False
    except CitrinationClientError:
        pass

   # Maximum can't be greater than 100
    minimum = 30
    maximum = 120

    try:
        c = ElementalCompositionConstraint(name=name,
                                           elements=elements,
                                           minimum=minimum,
                                           maximum=maximum)
        assert False
    except CitrinationClientError:
        pass

    # Maximum can't be less than minimum
    minimum = 90
    maximum = 60

    try:
        c = ElementalCompositionConstraint(name=name,
                                           elements=elements,
                                           minimum=minimum,
                                           maximum=maximum)
        assert False
    except CitrinationClientError:
        pass

    # Valid values are OK
    minimum = 20
    maximum = 50

    c = ElementalCompositionConstraint(name=name,
                                       elements=elements,
                                       minimum=minimum,
                                       maximum=maximum)

def test_elemental_inclusion_constraint():
    """
    Tests that the elemental inclusion constraint is correctly
    converted to a map with elements and logic preserved

    Also tests that logic must be one of the three acceptable values
    """
    name = "Property Band gap"
    elements = ["Ga", "N"]

    # Bad logic raises an error
    try:
        asdf = "asdf"
        c = ElementalInclusionConstraint(name=name, elements=elements, logic=asdf)
        assert False
    except CitrinationClientError:
        pass

    # Good logics do not raise an error
    should = "should"
    ElementalInclusionConstraint(name=name, elements=elements, logic=should)
    must = "must"
    ElementalInclusionConstraint(name=name, elements=elements, logic=must)
    exclude = "exclude"
    ElementalInclusionConstraint(name=name, elements=elements, logic=exclude)

    # Dictionary is formatted properly
    logic="should"
    c = ElementalInclusionConstraint(name=name, elements=elements, logic=logic)

    mapped_c = c.to_dict()

    assert mapped_c["type"] is "elementalInclusionConstraint"
    assert mapped_c["name"] is name
    assert mapped_c["options"]["logic"] is logic
    assert mapped_c["options"]["elements"] is elements