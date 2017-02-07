from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery


class QuantityQuery(BaseObjectQuery):
    """
    Class to query against a PIF Quantity object.
    """

    def __init__(self, actual_mass_percent=None, actual_volume_percent=None, actual_number_percent=None,
                 ideal_mass_percent=None, ideal_volume_percent=None, ideal_number_percent=None, logic=None,
                 extract_as=None, extract_all=None, extract_when_missing=None, tags=None, length=None, offset=None):
        """
        Constructor.

        :param actual_mass_percent: One or more :class:`FieldQuery` operations against the actual mass
        percent field.
        :param actual_volume_percent: One or more :class:`FieldQuery` operations against the actual volume
        percent field.
        :param actual_number_percent: One or more :class:`FieldQuery` operations against the actual number
        percent field.
        :param ideal_mass_percent: One or more :class:`FieldQuery` operations against the ideal mass
        percent field.
        :param ideal_volume_percent: One or more :class:`FieldQuery` operations against the ideal volume
        percent field.
        :param ideal_number_percent: One or more :class:`FieldQuery` operations against the ideal number
        percent field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value
        is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        """
        super(QuantityQuery, self).__init__(logic=logic, extract_as=extract_as, extract_all=extract_all,
                                            extract_when_missing=extract_when_missing, tags=tags, length=length,
                                            offset=offset)
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
        self._actual_mass_percent = self._get_object(FieldQuery, actual_mass_percent)

    @actual_mass_percent.deleter
    def actual_mass_percent(self):
        self._actual_mass_percent = None

    @property
    def actual_volume_percent(self):
        return self._actual_volume_percent

    @actual_volume_percent.setter
    def actual_volume_percent(self, actual_volume_percent):
        self._actual_volume_percent = self._get_object(FieldQuery, actual_volume_percent)

    @actual_volume_percent.deleter
    def actual_volume_percent(self):
        self._actual_volume_percent = None

    @property
    def actual_number_percent(self):
        return self._actual_number_percent

    @actual_number_percent.setter
    def actual_number_percent(self, actual_number_percent):
        self._actual_number_percent = self._get_object(FieldQuery, actual_number_percent)

    @actual_number_percent.deleter
    def actual_number_percent(self):
        self._actual_number_percent = None

    @property
    def ideal_mass_percent(self):
        return self._ideal_mass_percent

    @ideal_mass_percent.setter
    def ideal_mass_percent(self, ideal_mass_percent):
        self._ideal_mass_percent = self._get_object(FieldQuery, ideal_mass_percent)

    @ideal_mass_percent.deleter
    def ideal_mass_percent(self):
        self._ideal_mass_percent = None

    @property
    def ideal_volume_percent(self):
        return self._ideal_volume_percent

    @ideal_volume_percent.setter
    def ideal_volume_percent(self, ideal_volume_percent):
        self._ideal_volume_percent = self._get_object(FieldQuery, ideal_volume_percent)

    @ideal_volume_percent.deleter
    def ideal_volume_percent(self):
        self._ideal_volume_percent = None

    @property
    def ideal_number_percent(self):
        return self._ideal_number_percent

    @ideal_number_percent.setter
    def ideal_number_percent(self, ideal_number_percent):
        self._ideal_number_percent = self._get_object(FieldQuery, ideal_number_percent)

    @ideal_number_percent.deleter
    def ideal_number_percent(self):
        self._ideal_number_percent = None
