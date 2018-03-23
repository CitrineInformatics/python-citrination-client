from citrination_client.util.credentials import *
from citrination_client.util import env as citr_env_vars
from citrination_client.errors import CitrinationClientError
import os

mock_credentials_path = './citrination_client/util/tests/mock_credentials'

def test_initialization_parameters_preferred():
    api_key = "mykey"
    site = "mysite.citrination.com"
    os.environ[citr_env_vars.CITRINATION_API_KEY] = "definitelysomekey"
    os.environ[citr_env_vars.CITRINATION_SITE] = "wrong.citrination.com"
    os.environ[citr_env_vars.CITRINATION_PROFILE] = "test"
    preferred_key, preferred_site = get_preferred_credentials(api_key, site, mock_credentials_path)
    assert preferred_key == api_key
    assert preferred_site == site
    _reset_env()

def test_only_initialization_parameters():
    api_key = "mykey"
    site = "mysite.citrination.com"
    preferred_key, preferred_site = get_preferred_credentials(api_key, site, mock_credentials_path)
    assert preferred_key == api_key
    assert preferred_site == site

def test_env_vars_preferred():
    api_key = "mykey"
    site = "mysite.citrination.com"
    os.environ[citr_env_vars.CITRINATION_API_KEY] = api_key
    os.environ[citr_env_vars.CITRINATION_SITE] = site
    os.environ[citr_env_vars.CITRINATION_PROFILE] = "test"
    preferred_key, preferred_site = get_preferred_credentials(None, None, mock_credentials_path)
    assert preferred_key == api_key
    assert preferred_site == site
    _reset_env()

def test_specified_profile_preferred():
    os.environ[citr_env_vars.CITRINATION_PROFILE] = "test"
    preferred_key, preferred_site = get_preferred_credentials(None, None, mock_credentials_path)
    assert preferred_key == "my_test_profile_key"
    assert preferred_site == "my_test_profile_site"
    _reset_env()

def test_default_profile_last_resort():
    preferred_key, preferred_site = get_preferred_credentials(None, None, mock_credentials_path)
    assert preferred_key == "my_default_profile_key"
    assert preferred_site == "my_default_profile_site"
    _reset_env()

def test_creds_none_if_no_file():
    key, site = get_credentials_from_file("obviously_doesnt_exist.yaml")
    assert key is None
    assert site is None

def _reset_env():
    os.environ.pop(citr_env_vars.CITRINATION_API_KEY, None)
    os.environ.pop(citr_env_vars.CITRINATION_SITE, None)
    os.environ.pop(citr_env_vars.CITRINATION_PROFILE, None)