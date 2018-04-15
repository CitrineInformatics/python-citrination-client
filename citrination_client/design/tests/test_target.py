from citrination_client.errors import *
from citrination_client.design import Target

def test_target_initialization():
    """
    Tests that the design target must be initialized
    with an objective that is either Min or Max
    """

    try:
        Target(descriptor="Band gap", objective="asdf")
    except CitrinationClientError:
        assert True

    try:
        Target(descriptor="Band gap", objective="Min")
        Target(descriptor="Band gap", objective="Max")
        assert True
    except CitrinationClientError:
        assert False