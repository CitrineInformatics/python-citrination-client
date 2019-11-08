import yaml
import os
import sys
import citrination_client.util.env as citr_env_vars
from citrination_client.base.errors import CitrinationClientError

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
    """
    Given a filepath, loads the file as a dictionary from YAML

    :param path: The path to a YAML file
    """
    with open(path, "r") as f:
      raw_yaml = f.read()
      parsed_dict = yaml.load(raw_yaml, Loader=yaml.FullLoader)
    return parsed_dict

def get_credentials_from_file(filepath):
    """
    Extracts credentials from the yaml formatted credential filepath
    passed in. Uses the default profile if the CITRINATION_PROFILE env var
    is not set, otherwise looks for a profile with that name in the credentials file.

    :param filepath: The path of the credentials file
    """
    try:
        creds = load_file_as_yaml(filepath)
    except Exception:
        creds = {}

    profile_name = os.environ.get(citr_env_vars.CITRINATION_PROFILE)
    if profile_name is None or len(profile_name) == 0:
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
    """
    Given an API key, a site url and a credentials file path, runs through a prioritized list of credential sources to find credentials.

    Specifically, this method ranks credential priority as follows:
        1. Those passed in as the first two parameters to this method
        2. Those found in the environment as variables
        3. Those found in the credentials file at the profile specified
           by the profile environment variable
        4. Those found in the default stanza in the credentials file

    :param api_key: A Citrination API Key or None
    :param site: A Citrination site URL or None
    :param cred_file: The path to a credentials file
    """
    profile_api_key, profile_site = get_credentials_from_file(cred_file)
    if api_key is None:
        api_key =  os.environ.get(citr_env_vars.CITRINATION_API_KEY)
    if api_key is None or len(api_key) == 0:
        api_key = profile_api_key

    if site is None:
        site = os.environ.get(citr_env_vars.CITRINATION_SITE)
    if site is None or len(site) == 0:
        site = profile_site
    if site is None:
        site = "https://citrination.com"

    return api_key, site
