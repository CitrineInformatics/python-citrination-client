import yaml
import os
import sys
import citrination_client.util.env as citr_env_vars
from citrination_client.errors import CitrinationClientError

home = os.path.expanduser("~")

DEFAULT_CITRINATION_CONFIG_DIRECTORY = ".citrination"
DEFAULT_CITRINATION_CREDENTIALS_FILE = os.path.join(
        home,
        DEFAULT_CITRINATION_CONFIG_DIRECTORY,
        "credentials"
    )

DEFAULT_CITRINATION_PROFILE = "default"
CREDENTIALS_API_KEY_KEY = "api_key"
CREDENTIALS_SITE_KEY = "site"

def load_file_as_yaml(path):
    with open(path, "r") as f:
      raw_yaml = f.read()
      parsed_dict = yaml.load(raw_yaml)
    return parsed_dict

def get_credentials_from_file(file):
    try:
        creds = load_file_as_yaml(file)
    except Exception:
        creds = {}

    profile_name = os.environ[citr_env_vars.CITRINATION_PROFILE]
    if len(profile_name) == 0:
        profile_name = DEFAULT_CITRINATION_PROFILE
    api_key = None
    site = None
    try:
        profile = creds[profile_name]
        api_key = profile[CREDENTIALS_API_KEY_KEY]
        site = profile[CREDENTIALS_SITE_KEY]
    except KeyError:
        pass

    return (api_key, site)

def get_preferred_credentials(api_key, site, cred_file=DEFAULT_CITRINATION_CREDENTIALS_FILE):
    profile_api_key, profile_site = get_credentials_from_file(cred_file)
    if api_key is None:
        api_key =  os.environ[citr_env_vars.CITRINATION_API_KEY]
    if len(api_key) == 0:
        api_key = profile_api_key

    if site is None:
        site = os.environ[citr_env_vars.CITRINATION_SITE]
    if len(site) == 0:
        site = profile_site
    if site is None:
        site = "https://citrination.com"

    return api_key, site
