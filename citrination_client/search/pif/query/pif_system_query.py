from citrination_client.search.core.query.filter import Filter
from citrination_client.search.pif.query.chemical.chemical_field_query import ChemicalFieldQuery
from citrination_client.search.pif.query.chemical.composition_query import CompositionQuery
from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.classification_query import ClassificationQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery
from citrination_client.search.pif.query.core.id_query import IdQuery
from citrination_client.search.pif.query.core.process_step_query import ProcessStepQuery
from citrination_client.search.pif.query.core.property_query import PropertyQuery
from citrination_client.search.pif.query.core.quantity_query import QuantityQuery
from citrination_client.search.pif.query.core.reference_query import ReferenceQuery
from citrination_client.search.pif.query.core.source_query import SourceQuery


class PifSystemQuery(BaseObjectQuery):
    """
    Class to store information about a PIF query.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, extract_as=None, extract_all=None,
                 extract_when_missing=None, tags=None, length=None, offset=None, uid=None, updated_at=None,
                 names=None, ids=None, classifications=None, source=None, quantity=None, chemical_formula=None,
                 composition=None, properties=None, preparation=None, references=None, sub_systems=None,
                 query=None, **kwargs):
        """
        Constructor.

        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param weight: Weight of the query.
        :param simple: String with the simple search to run against all fields.
        :param simple_weight: Dictionary of relative paths to their weights for simple queries.
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        :param uid: One or more :class:`Filter` objects with the filters against the uid field.
        :param updated_at: One or more :class:`Filter` objects with filters against the time that the PIF record was last updated.
        :param names: One or more :class:`FieldQuery` objects with queries against the names field.
        :param ids: One or more :class:`IdQuery` objects with queries against the ids field.
        :param classifications: One or more :class:`ClassificationQuery` objects with queries against the classifications field.
        :param source: One or more :class:`SourceQuery` objects with queries against the source field.
        :param quantity: One or more :class:`QuantityQuery` objects with queries against the quantity field.
        :param chemical_formula: One or more :class:`ChemicalFieldQuery` objects with queries against the chemicalFormula field.
        :param composition: One or more :class:`CompositionQuery` objects with queries against the composition field.
        :param properties: One or more :class:`PropertyQuery` objects with queries against the properties field.
        :param preparation: One or more :class:`ProcessStepQuery` objects with queries against the preparation field.
        :param references: One or more :class:`ReferenceQuery` objects with queries against the references field.
        :param sub_systems: One or more :class:`PifSystemQuery` objects with queries against the subSystems field.
        :param query: One or more :class:`PifSystemQuery` objects with nested queries.
        """
        super(PifSystemQuery, self).__init__(
            logic=logic, weight=weight, simple=simple, simple_weight=simple_weight, extract_as=extract_as,
            extract_all=extract_all, extract_when_missing=extract_when_missing, tags=tags, length=length,
            offset=offset, **kwargs)
        self._uid = None
        self.uid = uid
        self._updated_at = None
        self.updated_at = updated_at
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
        self._query = None
        self.query = query

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = self._get_object(Filter, uid)

    @uid.deleter
    def uid(self):
        self._uid = None

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        self._updated_at = self._get_object(Filter, updated_at)

    @updated_at.deleter
    def updated_at(self):
        self._updated_at = None

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
        self._sub_systems = self._get_object(PifSystemQuery, sub_systems)

    @sub_systems.deleter
    def sub_systems(self):
        self._sub_systems = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(PifSystemQuery, query)

    @query.deleter
    def query(self):
        self._query = None
