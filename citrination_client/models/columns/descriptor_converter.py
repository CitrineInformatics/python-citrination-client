from .alloy_composition import AlloyCompositionColumn
from .categorical import CategoricalColumn
from .formulation import FormulationColumn
from .inorganic_chemical_formula import InorganicChemicalFormulaColumn
from .integer import IntColumn
from .organic_chemical_formula import OrganicChemicalFormulaColumn
from .real import RealColumn
from .vector import VectorColumn


class DescriptorConverter(object):

    @classmethod
    def convert(self, col_name, descriptor, role, units=None):
        column_type = descriptor['category']
        if column_type == CategoricalColumn.TYPE:
            categories = [str(v) for v in descriptor["descriptorValues"]]

            return CategoricalColumn(
                name=col_name,
                role=role,
                units=units,
                categories=categories
            )
        elif column_type == RealColumn.TYPE:
            lower_bound = descriptor["lowerBound"]
            upper_bound = descriptor["upperBound"]

            return RealColumn(
                name=col_name,
                role=role,
                units=units,
                lower_bound=lower_bound,
                upper_bound=upper_bound
            )
        elif column_type == IntColumn.TYPE:
            lower_bound = descriptor["lowerBound"]
            upper_bound = descriptor["upperBound"]

            return IntColumn(
                name=col_name,
                role=role,
                units=units,
                lower_bound=lower_bound,
                upper_bound=upper_bound
            )
        elif column_type == AlloyCompositionColumn.TYPE:
            balance_element = descriptor['balanceElement']
            basis = descriptor['basis']

            return AlloyCompositionColumn(
                name=col_name,
                role=role,
                units=units,
                balance_element=balance_element,
                basis=basis
            )
        elif column_type == InorganicChemicalFormulaColumn.TYPE:
            return InorganicChemicalFormulaColumn(
                name=col_name,
                role=role,
                units=units
            )
        elif column_type == OrganicChemicalFormulaColumn.TYPE:
            return OrganicChemicalFormulaColumn(
                name=col_name,
                role=role,
                units=units
            )
        elif column_type == FormulationColumn.TYPE:
            return FormulationColumn(
                name=col_name,
                role=role,
                units=units
            )
        elif column_type == VectorColumn.TYPE:
            length = descriptor["length"]

            return VectorColumn(
                name=col_name,
                role=role,
                units=units,
                length=length
            )
