from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.classification_query import ClassificationQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery
from citrination_client.search.pif.query.core.id_query import IdQuery
from citrination_client.search.pif.query.core.process_step_query import ProcessStepQuery
from citrination_client.search.pif.query.core.property_query import PropertyQuery
from citrination_client.search.pif.query.core.quantity_query import QuantityQuery
from citrination_client.search.pif.query.core.reference_query import ReferenceQuery
from citrination_client.search.pif.query.core.source_query import SourceQuery
from citrination_client.search.pif.query.chemical.chemical_field_query import ChemicalFieldQuery
from citrination_client.search.pif.query.chemical.composition_query import CompositionQuery


class SystemQuery(BaseObjectQuery):
    """
    Class to query against a PIF System.
    """

    def __init__(self, names=None, ids=None, classifications=None, source=None, quantity=None, chemical_formula=None, 
                 composition=None, properties=None, preparation=None, references=None, sub_systems=None, logic=None, 
                 extract_as=None, extract_all=None, extract_when_missing=None, tags=None, length=None, offset=None):
        """
        Constructor.

        :param names: One or more :class:`FieldQuery` operations against the names field.
        :param ids: One or more :class:`IdQuery` operations against the ids field.
        :param classifications: One or more :class:`ClassificationQuery` operations against the classifications field.
        :param source: One or more :class:`SourceQuery` operations against the source field.
        :param quantity: One or more :class:`QuantityQuery` operations against the quantity field.
        :param chemical_formula: One or more :class:`ChemicalFieldQuery` operations against the
        chemical formula field.
        :param composition: One or more :class:`CompositionQuery` operations against the composition field.
        :param properties: One or more :class:`PropertyQuery` operations against the properties field.
        :param preparation: One or more :class:`ProcessStepQuery` operations against the preparation field.
        :param references: One or more :class:`ReferenceQuery` operations against the references field.
        :param sub_systems: One or more :class:`SystemQuery` operations against the sub systems field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value
        is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        """
        super(SystemQuery, self).__init__(logic=logic, extract_as=extract_as, extract_all=extract_all,
                                          extract_when_missing=extract_when_missing, tags=tags, length=length,
                                          offset=offset)
        self._names = None
        self.names = names
        self._ids = None
        self.ids = ids
        self._classifications = None
        self.classifications = classifications
        self._source = None
        self.source = source
        self._quantity = None
        self.quantity = quantity
        self._chemical_formula = None
        self.chemical_formula = chemical_formula
        self._composition = None
        self.composition = composition
        self._properties = None
        self.properties = properties
        self._preparation = None
        self.preparation = preparation
        self._references = None
        self.references = references
        self._sub_systems = None
        self.sub_systems = sub_systems

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, names):
        self._names = self._get_object(FieldQuery, names)

    @names.deleter
    def names(self):
        self._names = None

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = self._get_object(IdQuery, ids)

    @ids.deleter
    def ids(self):
        self._ids = None

    @property
    def classifications(self):
        return self._classifications

    @classifications.setter
    def classifications(self, classifications):
        self._classifications = self._get_object(ClassificationQuery, classifications)

    @classifications.deleter
    def classifications(self):
        self._classifications = None

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = self._get_object(SourceQuery, source)

    @source.deleter
    def source(self):
        self._source = None

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        self._quantity = self._get_object(QuantityQuery, quantity)

    @quantity.deleter
    def quantity(self):
        self._quantity = None

    @property
    def chemical_formula(self):
        return self._chemical_formula

    @chemical_formula.setter
    def chemical_formula(self, chemical_formula):
        self._chemical_formula = self._get_object(ChemicalFieldQuery, chemical_formula)

    @chemical_formula.deleter
    def chemical_formula(self):
        self._chemical_formula = None

    @property
    def composition(self):
        return self._composition

    @composition.setter
    def composition(self, composition):
        self._composition = self._get_object(CompositionQuery, composition)

    @composition.deleter
    def composition(self):
        self._composition = None

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = self._get_object(PropertyQuery, properties)

    @properties.deleter
    def properties(self):
        self._properties = None

    @property
    def preparation(self):
        return self._preparation

    @preparation.setter
    def preparation(self, preparation):
        self._preparation = self._get_object(ProcessStepQuery, preparation)

    @preparation.deleter
    def preparation(self):
        self._preparation = None

    @property
    def references(self):
        return self._references

    @references.setter
    def references(self, references):
        self._references = self._get_object(ReferenceQuery, references)

    @references.deleter
    def references(self):
        self._references = None

    @property
    def sub_systems(self):
        return self._sub_systems

    @sub_systems.setter
    def sub_systems(self, sub_systems):
        self._sub_systems = self._get_object(SystemQuery, sub_systems)

    @sub_systems.deleter
    def sub_systems(self):
        self._sub_systems = None
