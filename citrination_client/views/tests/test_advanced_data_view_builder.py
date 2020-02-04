import pytest

from citrination_client.views.advanced_data_view_builder import AdvancedDataViewBuilder
from citrination_client.views.descriptors.real_descriptor import RealDescriptor


def check_exception(func):
    try:
        func()
        return True
    except ValueError as e:
        return False


def test_add_relations():
    builder = AdvancedDataViewBuilder()

    builder.add_descriptor(RealDescriptor("a", lower_bound=-1, upper_bound=1), "Input", True)
    builder.add_descriptor(RealDescriptor("b", lower_bound=-1, upper_bound=1), "Output", True)
    builder.add_descriptor(RealDescriptor("c", lower_bound=-1, upper_bound=1), "Output", True)

    assert not check_exception(lambda: builder.add_relation(123, 123))
    assert check_exception(lambda: builder.add_relation('a', 'b'))
    assert check_exception(lambda: builder.add_relation('a', 'c'))
    assert not check_exception(lambda: builder.add_relation('c', ['d']))
    assert not check_exception(lambda: builder.add_relation([], 'b'))
    assert not check_exception(lambda: builder.add_relation(['a'], []))

    # duplicate
    assert not check_exception(lambda: builder.add_relation('a', 'b'))
    assert check_exception(lambda: builder.add_relation(['a', 'c'], 'b'))
    assert not check_exception(lambda: builder.add_relation(['c', 'a'], 'b'))
    assert not check_exception(lambda: builder.add_relation(['c', 'c'], 'b'))
    assert not check_exception(lambda: builder.add_relation('c', 'c'))

    # key not found
    assert not check_exception(lambda: builder.add_relation('z', 'b'))
    assert not check_exception(lambda: builder.add_relation('a', 'z'))

    # limit exceeded
    limit_hit = False
    for x in range(0, 50):
        try:
            builder.add_descriptor(RealDescriptor("a" + str(x), lower_bound=-1, upper_bound=1), "Input", True)
            builder.add_descriptor(RealDescriptor("b" + str(x), lower_bound=-1, upper_bound=1), "Output", True)
            builder.add_relation('a' + str(x), 'b' + str(x))
        except ValueError:
            if x > 0:
                limit_hit = True
    assert limit_hit
