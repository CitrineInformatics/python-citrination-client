from citrination_client.util.credentials import *
from citrination_client.util import env as citr_env_vars
from citrination_client.base.errors import CitrinationClientError
import os

mock_credentials_path = './citrination_client/util/tests/mock_credentials'
# Save these, to be restored later
original_env_api_key = None
original_env_site = None
original_env_profile = None


def save_env():
    global original_env_api_key
    global original_env_site
    global original_env_profile

    original_env_api_key = os.environ.get(citr_env_vars.CITRINATION_API_KEY, "")
    original_env_site = os.environ.get(citr_env_vars.CITRINATION_SITE, "")
    original_env_profile = os.environ.get(citr_env_vars.CITRINATION_PROFILE, "")


def test_initialization_parameters_preferred():
    """
    Tests that if:
        a) the environment specifies a citrination profile
        and
        b) the environment specifies credentials

    The credential prioritizer will still select the ones passed into it as arguments
    """
    api_key = "mykey"
    site = "mysite.citrination.com"
    save_env()
    os.environ[citr_env_vars.CITRINATION_API_KEY] = "definitelysomekey"
    os.environ[citr_env_vars.CITRINATION_SITE] = "wrong.citrination.com"
    os.environ[citr_env_vars.CITRINATION_PROFILE] = "test"
    preferred_key, preferred_site = get_preferred_credentials(api_key, site, mock_credentials_path)
    assert preferred_key == api_key
    assert preferred_site == site
    _reset_env()

def test_only_initialization_parameters():
    """
    Tests that if the only source of credentials is initialization paremeters, the credential prioritizer will return them
    """
    api_key = "mykey"
    site = "mysite.citrination.com"
    preferred_key, preferred_site = get_preferred_credentials(api_key, site, mock_credentials_path)
    assert preferred_key == api_key
    assert preferred_site == site

def test_env_vars_preferred():
    """
    Tests that credentials in environment variables are preferred to credentials
    stored in the citrination profile specified
    """
    api_key = "mykey"
    site = "mysite.citrination.com"
    save_env()
    os.environ[citr_env_vars.CITRINATION_API_KEY] = api_key
    os.environ[citr_env_vars.CITRINATION_SITE] = site
    os.environ[citr_env_vars.CITRINATION_PROFILE] = "test"
    preferred_key, preferred_site = get_preferred_credentials(None, None, mock_credentials_path)
    assert preferred_key == api_key
    assert preferred_site == site
    _reset_env()

def test_specified_profile_preferred():
    """
    Tests that credentials pointed to by the profile environment variable are prioritized over the default credential file credentials.
    """
    save_env()
    os.environ[citr_env_vars.CITRINATION_API_KEY] = ""
    os.environ[citr_env_vars.CITRINATION_SITE] = ""
    os.environ[citr_env_vars.CITRINATION_PROFILE] = "test"
    preferred_key, preferred_site = get_preferred_credentials(None, None, mock_credentials_path)
    assert preferred_key == "my_test_profile_key"
    assert preferred_site == "my_test_profile_site"
    _reset_env()

def test_default_profile_last_resort():
    """
    Tests that in the absence of all other information, credentials are pulled
    from the default stanza in the credentials file
    """
    save_env()
    os.environ[citr_env_vars.CITRINATION_API_KEY] = ""
    os.environ[citr_env_vars.CITRINATION_SITE] = ""
    os.environ[citr_env_vars.CITRINATION_PROFILE] = ""
    preferred_key, preferred_site = get_preferred_credentials(None, None, mock_credentials_path)
    assert preferred_key == "my_default_profile_key"
    assert preferred_site == "my_default_profile_site"
    _reset_env()

def test_creds_none_if_no_file():
    """
    Tests that no error is thrown if a nonexistant file is given to the
    credentials-from-file extraction method
    """
    key, site = get_credentials_from_file("obviously_doesnt_exist.yaml")
    assert key is None
    assert site is None

def _reset_env():
    os.environ[citr_env_vars.CITRINATION_API_KEY] = original_env_api_key
    os.environ[citr_env_vars.CITRINATION_SITE] = original_env_site
    os.environ[citr_env_vars.CITRINATION_PROFILE] = original_env_profile

