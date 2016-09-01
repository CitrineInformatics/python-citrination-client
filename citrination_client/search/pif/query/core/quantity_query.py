from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation


class QuantityQuery(BaseObjectQuery):
    """
    Class to query against a PIF Quantity object.
    """

    def __init__(self, actual_mass_percent=None, actual_volume_percent=None, actual_number_percent=None,
                 ideal_mass_percent=None, ideal_volume_percent=None, ideal_number_percent=None, logic=None,
                 tags=None, length=None, offset=None):
        """
        Constructor.

        :param actual_mass_percent: One or more :class:`FieldOperation` operations against the actual mass
        percent field.
        :param actual_volume_percent: One or more :class:`FieldOperation` operations against the actual volume
        percent field.
        :param actual_number_percent: One or more :class:`FieldOperation` operations against the actual number
        percent field.
        :param ideal_mass_percent: One or more :class:`FieldOperation` operations against the ideal mass
        percent field.
        :param ideal_volume_percent: One or more :class:`FieldOperation` operations against the ideal volume
        percent field.
        :param ideal_number_percent: One or more :class:`FieldOperation` operations against the ideal number
        percent field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param tags: One or more :class:`FieldOperation` operations against the tags field.
        :param length: One or more :class:`FieldOperation` operations against the length field.
        :param offset: One or more :class:`FieldOperation` operations against the offset field.
        """
        super(QuantityQuery, self).__init__(logic=logic, tags=tags, length=length, offset=offset)
        self._actual_mass_percent = None
        self.actual_mass_percent = actual_mass_percent
        self._actual_volume_percent = None
        self.actual_volume_percent = actual_volume_percent
        self._actual_number_percent = None
        self.actual_number_percent = actual_number_percent
        self._ideal_mass_percent = None
        self.ideal_mass_percent = ideal_mass_percent
        self._ideal_volume_percent = None
        self.ideal_volume_percent = ideal_volume_percent
        self._ideal_number_percent = None
        self.ideal_number_percent = ideal_number_percent

    @property
    def actual_mass_percent(self):
        return self._actual_mass_percent

    @actual_mass_percent.setter
    def actual_mass_percent(self, actual_mass_percent):
        self._actual_mass_percent = self._get_object(FieldOperation, actual_mass_percent)

    @actual_mass_percent.deleter
    def actual_mass_percent(self):
        self._actual_mass_percent = None

    @property
    def actual_volume_percent(self):
        return self._actual_volume_percent

    @actual_volume_percent.setter
    def actual_volume_percent(self, actual_volume_percent):
        self._actual_volume_percent = self._get_object(FieldOperation, actual_volume_percent)

    @actual_volume_percent.deleter
    def actual_volume_percent(self):
        self._actual_volume_percent = None

    @property
    def actual_number_percent(self):
        return self._actual_number_percent

    @actual_number_percent.setter
    def actual_number_percent(self, actual_number_percent):
        self._actual_number_percent = self._get_object(FieldOperation, actual_number_percent)

    @actual_number_percent.deleter
    def actual_number_percent(self):
        self._actual_number_percent = None

    @property
    def ideal_mass_percent(self):
        return self._ideal_mass_percent

    @ideal_mass_percent.setter
    def ideal_mass_percent(self, ideal_mass_percent):
        self._ideal_mass_percent = self._get_object(FieldOperation, ideal_mass_percent)

    @ideal_mass_percent.deleter
    def ideal_mass_percent(self):
        self._ideal_mass_percent = None

    @property
    def ideal_volume_percent(self):
        return self._ideal_volume_percent

    @ideal_volume_percent.setter
    def ideal_volume_percent(self, ideal_volume_percent):
        self._ideal_volume_percent = self._get_object(FieldOperation, ideal_volume_percent)

    @ideal_volume_percent.deleter
    def ideal_volume_percent(self):
        self._ideal_volume_percent = None

    @property
    def ideal_number_percent(self):
        return self._ideal_number_percent

    @ideal_number_percent.setter
    def ideal_number_percent(self, ideal_number_percent):
        self._ideal_number_percent = self._get_object(FieldOperation, ideal_number_percent)

    @ideal_number_percent.deleter
    def ideal_number_percent(self):
        self._ideal_number_percent = None
