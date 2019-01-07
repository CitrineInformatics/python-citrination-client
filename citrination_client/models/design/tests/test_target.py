from citrination_client.base.errors import *
from citrination_client.models.design import Target

def test_target_initialization():
    """
    Tests that the design target must be initialized
    with an objective that is either Min or Max
    """

    try:
        Target(name="Band gap", objective="asdf")
        assert False, "Target class should require that objective be one of Min or Max"
    except CitrinationClientError:
        pass

    # These initializations should not throw an error
    Target(name="Band gap", objective="Min")
    Target(name="Band gap", objective="Max")
    Target(name="Band gap", objective="5.0")
