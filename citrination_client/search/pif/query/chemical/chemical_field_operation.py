from citrination_client.search.pif.query.chemical.chemical_field_query import ChemicalFieldQuery


def ChemicalFieldOperation(filter=None, extract_as=None, extract_all=None, extract_when_missing=None,
                           length=None, offset=None):
    """
    Generate a new :class:`.ChemicalFieldQuery` object.

    :param filter: One or more :class:`.ChemicalFilter` objects for the query.
    :param extract_as: String with the alias to save this field under.
    :param extract_all: Boolean setting whether all values in an array should be extracted.
    :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value
    is missing that should be extracted (and the overall query is still satisfied).
    :param length: One or more :class:`.FieldOperation` objects against the length field.
    :param offset: One or more :class:`.FieldOperation` objects against the offset field.
    :param filter: One or more :class:`.ChemicalFilter` objects against this field.
    """
    from warnings import warn
    warn("ChemicalFieldOperation has been deprecated in favor of ChemicalFieldQuery starting with version 1.3.0")
    return ChemicalFieldQuery(filter=filter, extract_as=extract_as, extract_all=extract_all,
                              extract_when_missing=extract_when_missing, length=length, offset=offset)

