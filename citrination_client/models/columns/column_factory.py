from citrination_client.models.columns import *
from citrination_client.base import CitrinationClientError

def _flatten_column_dict(response_dict):
    flat_dict = {}
    for k in response_dict:
        if k == "options" or k == "type":
            continue
        flat_dict[k] = response_dict[k]

    if response_dict["options"]:
        for option in response_dict["options"]:
            flat_dict[option] = response_dict["options"][option]

    return flat_dict

def _get_column_class_from_type(type):
    if type == RealColumn.TYPE:
        return RealColumn
    if type == IntColumn.TYPE:
        return IntColumn
    elif type == CategoricalColumn.TYPE:
        return CategoricalColumn
    elif type == AlloyCompositionColumn.TYPE:
        return AlloyCompositionColumn
    elif type == InorganicChemicalFormulaColumn.TYPE:
        return InorganicChemicalFormulaColumn
    elif type == VectorColumn.TYPE:
        return VectorColumn
    else:
        raise CitrinationClientError("Unknown column type: {}".format(type))

class ColumnFactory(object):

    @staticmethod
    def from_dict(response_dict):
        column_class = _get_column_class_from_type(response_dict["type"])
        processed_dict = _flatten_column_dict(response_dict)
        return column_class(**processed_dict)
