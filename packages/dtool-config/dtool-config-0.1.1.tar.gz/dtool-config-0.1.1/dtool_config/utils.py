"""Helper functions for getting and setting config values."""

import os
import json

from dtoolcore.utils import mkdir_parents

USERNAME_KEY = "DTOOL_USER_FULL_NAME"
USER_EMAIL_KEY = "DTOOL_USER_EMAIL"

ECS_ENDPOINT_KEY = "DTOOL_ECS_ENDPOINT"
ECS_ACCESS_KEY_ID_KEY = "DTOOL_ECS_ACCESS_KEY_ID"
ECS_SECRET_ACCESS_KEY_KEY = "DTOOL_ECS_SECRET_ACCESS_KEY"

AZURE_KEY_PREFIX = "DTOOL_AZURE_ACCOUNT_KEY_"

CACHE_KEYS = {
    "azure": "DTOOL_AZURE_CACHE_DIRECTORY",
    "ecs": "DTOOL_ECS_CACHE_DIRECTORY",
    "http": "DTOOL_HTTP_CACHE_DIRECTORY",
    "irods": "DTOOL_IRODS_CACHE_DIRECTORY",
    "s3": "DTOOL_S3_CACHE_DIRECTORY",
}


def _get_config_content(config_fpath):

    # Default (empty) content will be used if config file does not exist.
    config_content = {}

    # If the config file exists we use that content.
    if os.path.isfile(config_fpath):
        with open(config_fpath) as fh:
            config_content = json.load(fh)

    return config_content


def _get(config_fpath, key):

    config_content = _get_config_content(config_fpath)

    if key not in config_content:
        return ""

    return config_content[key]


def _set(config_fpath, key, value):

    config_content = _get_config_content(config_fpath)

    # Add/update the key/value pair.
    config_content[key] = value

    # Create parent directories if they are missing.
    mkdir_parents(os.path.dirname(config_fpath))

    with open(config_fpath, "w") as fh:
        json.dump(config_content, fh, sort_keys=True, indent=2)

    os.chmod(config_fpath, 33216)

    return _get(config_fpath, key)


def get_username(config_fpath):
    """Return the user name.

    :param config_fpath: path to the dtool config file
    :returns: the user name or an empty string
    """
    return _get(config_fpath, USERNAME_KEY)


def set_username(config_fpath, username):
    """Write the user name to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param username: user name
    """
    return _set(config_fpath, USERNAME_KEY, username)


def get_user_email(config_fpath):
    """Return the user email.

    :param config_fpath: path to the dtool config file
    :returns: the user email or an empty string
    """
    return _get(config_fpath, USER_EMAIL_KEY)


def set_user_email(config_fpath, email):
    """Write the user email to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param email: user email
    """
    return _set(config_fpath, USER_EMAIL_KEY, email)


def get_ecs_endpoint(config_fpath):
    """Return the ECS endpoint URL.

    :param config_fpath: path to the dtool config file
    :returns: the ECS endpoint URL or an empty string
    """
    return _get(config_fpath, ECS_ENDPOINT_KEY)


def set_ecs_endpoint(config_fpath, ecs_endpoint):
    """Write the ECS endpoint URL to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param ecs_endpoint: ECS endpoint URL
    """
    return _set(config_fpath, ECS_ENDPOINT_KEY, ecs_endpoint)


def get_ecs_access_key_id(config_fpath):
    """Return the ECS access key id.

    :param config_fpath: path to the dtool config file
    :returns: the ECS access key id or an empty string
    """
    return _get(config_fpath, ECS_ACCESS_KEY_ID_KEY)


def set_ecs_access_key_id(config_fpath, ecs_access_key_id):
    """Write the ECS access key id to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param ecs_access_key_id: ECS access key id
    """
    return _set(config_fpath, ECS_ACCESS_KEY_ID_KEY, ecs_access_key_id)


def get_ecs_secret_access_key(config_fpath):
    """Return the ECS secret access key.

    :param config_fpath: path to the dtool config file
    :returns: the ECS secret access key or an empty string
    """
    return _get(config_fpath, ECS_SECRET_ACCESS_KEY_KEY)


def set_ecs_secret_access_key(config_fpath, ecs_secret_access_key):
    """Write the ECS access key id to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param ecs_secret_access_key: ECS secret access key
    """
    return _set(config_fpath, ECS_SECRET_ACCESS_KEY_KEY, ecs_secret_access_key)


def get_cache(config_fpath, storage_scheme):
    """Return the cache directory for the specified storage broker.

    :param config_fpath: path to the dtool config file
    :param storage_scheme: storage scheme (as in URI scheme)
    :returns: the ECS secret access key or an empty string
    """

    return _get(config_fpath, CACHE_KEYS[storage_scheme])


def set_cache(config_fpath, storage_scheme, cache_dir):
    """Write the ECS access key id to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param storage_scheme: storage scheme (as in URI scheme)
    :param cache_dir: ECS cache direcotory
    """
    return _set(config_fpath, CACHE_KEYS[storage_scheme], cache_dir)


def get_azure_secret_access_key(config_fpath, container):
    """Return the Azure storage container secret access key.

    :param config_fpath: path to the dtool config file
    :param container: azure storage container name
    :returns: the Azure container secret access key or an empty string
    """
    key = AZURE_KEY_PREFIX + container
    return _get(config_fpath, key)


def set_azure_secret_access_key(config_fpath, container, az_secret_access_key):
    """Write the ECS access key id to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param container: azure storage container name
    :param az_secret_access_key: azure secret access key for the container
    """
    key = AZURE_KEY_PREFIX + container
    return _set(config_fpath, key, az_secret_access_key)


def list_azure_containers(config_fpath):
    """List the azure storage containers in the config file.

    :param config_fpath: path to the dtool config file
    :returns: the list of azure storage container names
    """
    config_content = _get_config_content(config_fpath)
    az_container_names = []
    for key in config_content.keys():
        if key.startswith(AZURE_KEY_PREFIX):
            name = key[len(AZURE_KEY_PREFIX):]
            az_container_names.append(name)
    return sorted(az_container_names)
