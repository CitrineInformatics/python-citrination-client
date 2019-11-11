import pytest

from citrination_client.views.data_view_builder import DataViewBuilder
from citrination_client.views.descriptors.real_descriptor import RealDescriptor
from citrination_client.views.relations import RelationOptions


def test_add_descriptor():
    builder = DataViewBuilder()

    bandgap = RealDescriptor("band gap", lower_bound=-1, upper_bound=1)

    builder.add_descriptor(bandgap, "output", True)
    config = builder.build()

    assert config["group_by"] == ["band gap"]
    assert config["descriptors"] == [bandgap.as_dict()]
    assert config["roles"] == {"band gap": "output"}

    # Make sure duplicates raise an error
    with pytest.raises(ValueError) as err:
        builder.add_descriptor(RealDescriptor("band gap", lower_bound=-1, upper_bound=1), "input")


def check_exception(func):
    try:
        func()
        return True
    except ValueError:
        return False


def test_add_relations():
    builder = DataViewBuilder()

    assert not check_exception(lambda: builder.add_relation(123, 123))
    assert check_exception(lambda: builder.add_relation('a', 'b'))
    assert check_exception(lambda: builder.add_relation(['c'], ['d']))
    assert not check_exception(lambda: builder.add_relation([], ['b']))
    assert not check_exception(lambda: builder.add_relation(['a'], []))
    assert not check_exception(lambda: builder.add_relation('a', 'b', relation_type='asdf'))

    relation_options = RelationOptions()

    assert check_exception(lambda: builder.add_relation('e', 'f', options=relation_options))
    assert not check_exception(lambda: builder.add_relation('a', 'b', options=123))

    # duplicate
    assert not check_exception(lambda: builder.add_relation('e', 'f', options=relation_options))

    # limit exceeded
    limit_hit = False
    try:
        for x in range(0, 50):
            builder.add_relation('a' + str(x), 'b' + str(x))
    except ValueError:
        limit_hit = True
    assert limit_hit

