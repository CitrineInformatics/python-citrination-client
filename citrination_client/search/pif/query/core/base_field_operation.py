from citrination_client.search.pif.query.core.base_field_query import BaseFieldQuery


def BaseFieldOperation(extract_as=None, extract_all=None, extract_when_missing=None, length=None, offset=None):
    """
    Generate a new :class:`.BaseFieldQuery` object.

    :param extract_as: String with the alias to save this field under.
    :param extract_all: Boolean setting whether all values in an array should be extracted.
    :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value
    is missing that should be extracted (and the overall query is still satisfied).
    :param length: One or more :class:`.FieldQuery` operations against the length field.
    :param offset: One or more :class:`.FieldQuery` operations against the offset field.
    """
    from warnings import warn
    warn("BaseFieldOperation has been deprecated in favor of BaseFieldQuery starting with version 1.3.0")
    return BaseFieldQuery(extract_as=extract_as, extract_all=extract_all, extract_when_missing=extract_when_missing,
                          length=length, offset=offset)
