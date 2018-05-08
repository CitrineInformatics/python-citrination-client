import pytest
from citrination_client.models.columns import *
from citrination_client.base.errors import *

class TestCategoricalColumn(object):

    def test_real_descriptor_correctly_converted(self):
        col_name = "Property Band gap"
        lower_bound = 0.0
        upper_bound = "Infinity"
        units = "eV"
        role = "Output"

        descriptor = {
            "category": "Real",
            "lowerBound": lower_bound,
            "upperBound": upper_bound
        }

        col = DescriptorConverter.convert(
                col_name=col_name,
                descriptor=descriptor,
                role=role,
                units=units
            )

        assert col.name == col_name
        assert col.role == role
        assert col.units == units
        assert col.upper_bound == float(upper_bound)
        assert col.lower_bound == float(lower_bound)
        assert col.__class__ == RealColumn

    def test_categorical_descriptor_correctly_converted(self):
        col_name = "Property Color"
        categories = ["Blue", "Grey"]
        role = "Output"

        descriptor = {
            "category": "Categorical",
            "descriptorValues": categories
        }

        col = DescriptorConverter.convert(
                col_name=col_name,
                descriptor=descriptor,
                role=role
            )

        assert col.name == col_name
        assert col.role == role
        assert col.categories == categories
        assert col.__class__ == CategoricalColumn

    def test_vector_descriptor_correctly_converted(self):
        col_name = "Propert Burgers vector"
        length = 3
        role = "Output"

        descriptor = {
            "category": "Vector",
            "length": length,
        }

        col = DescriptorConverter.convert(
                col_name=col_name,
                descriptor=descriptor,
                role=role
            )

        assert col.name == col_name
        assert col.role == role
        assert col.length == length
        assert col.__class__ == VectorColumn

    def test_alloy_composition_descriptor_correctly_converted(self):
        col_name = "composition"
        basis = 30.0
        balance_element = "ALUMINUM"
        role = "Input"

        descriptor = {
            "category": "Alloy composition",
            "balanceElement": balance_element,
            "basis": basis
        }

        col = DescriptorConverter.convert(
                col_name=col_name,
                descriptor=descriptor,
                role=role
            )

        assert col.name == col_name
        assert col.role == role
        assert col.basis == basis
        assert col.balance_element == balance_element
        assert col.__class__ == AlloyCompositionColumn

    def test_organic_descriptor_correctly_converted(self):
        col_name = "SMILES"
        role = "Input"

        descriptor = {
            "category": "Organic"
        }

        col = DescriptorConverter.convert(
                col_name=col_name,
                descriptor=descriptor,
                role=role
            )

        assert col.name == col_name
        assert col.role == role
        assert col.__class__ == OrganicChemicalFormulaColumn

    def test_inorganic_descriptor_correctly_converted(self):
        col_name = "formula"
        role = "Input"

        descriptor = {
            "category": "Inorganic"
        }

        col = DescriptorConverter.convert(
                col_name=col_name,
                descriptor=descriptor,
                role=role
            )

        assert col.name == col_name
        assert col.role == role
        assert col.__class__ == InorganicChemicalFormulaColumn
