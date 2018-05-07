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
    if type == "Real":
        return RealColumn
    elif type == 'Categorical':
        return CategoricalColumn
    elif type == 'Alloy composition':
        return AlloyCompositionColumn
    elif type == 'Inorganic':
        return InorganicChemicalFormulaColumn
    elif type == "Vector":
        return VectorColumn
    else:
        raise CitrinationClientError("Unknown column type: {}".format(type))

class ColumnFactory(object):

    @staticmethod
    def from_dict(response_dict):
        column_class = _get_column_class_from_type(response_dict["type"])
        processed_dict = _flatten_column_dict(response_dict)
        return column_class(**processed_dict)
