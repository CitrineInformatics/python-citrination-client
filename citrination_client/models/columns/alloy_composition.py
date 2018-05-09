from citrination_client.models.columns.base import BaseColumn

class AlloyCompositionColumn(BaseColumn):
    """
    An alloy composition column configuration for a data view. Parameterized
    with the basic column options, plus the balance element for the column
    and the basis value for the composition.
    """

    TYPE = "Alloy composition"

    def __init__(self, name, role, balance_element, group_by_key=False, units=None, basis=100.0):
        """
        Constructor.

        :param name: The name of the column
        :type name: str
        :param role: The role the column will play in machine learning:
                       "Input"
                       "Output"
                       "Latent Variable"
                       "Ignore"
        :type role: str
        :param group_by_key: Whether or not this column should be used for
            grouping during cross validation
        :type group_by_key: bool
        :param units: Optionally, the units for the column
        :type units: str
        :param balance_element: The element making up the balance in the
            composition
        :type balance_element: str
        :param basis: The total amount of composition when deciding how to fill
            the balance
        :type basis: float

        """
        super(AlloyCompositionColumn, self).__init__(name=name,
                                                role=role,
                                                group_by_key=group_by_key,
                                                units=units)
        self._balance_element = balance_element
        self._basis = basis

    def build_options(self):
        return {
            "balance_element": self.balance_element,
            "basis": self.basis
        }

    @property
    def basis(self):
        return self._basis

    @basis.setter
    def basis(self, value):
        self._basis = value

    @basis.deleter
    def basis(self):
        self._basis = None

    @property
    def balance_element(self):
        return self._balance_element

    @balance_element.setter
    def balance_element(self, value):
        self._balance_element = value

    @balance_element.deleter
    def balance_element(self):
        self._balance_element = None
