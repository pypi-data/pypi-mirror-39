"""dtool_config.cli module."""

import click

import dtoolcore.utils

import dtool_config.utils


CONFIG_PATH = dtoolcore.utils.DEFAULT_CONFIG_PATH


@click.group()
def config():
    """Configure dtool settings."""


@config.group()
def user():
    """Configure user settings."""


@user.command()
@click.argument("username", required=False)
def name(username):
    """Display / set / update the user name."""
    if not username:
        click.secho(dtool_config.utils.get_username(CONFIG_PATH))
    else:
        click.secho(dtool_config.utils.set_username(CONFIG_PATH, username))


@user.command()
@click.argument("email_address", required=False)
def email(email_address):
    """Display / set / update the user email."""
    if not email_address:
        click.secho(dtool_config.utils.get_user_email(CONFIG_PATH))
    else:
        click.secho(dtool_config.utils.set_user_email(
            CONFIG_PATH,
            email_address
        ))


@config.group()
def ecs():
    """Configure ECS S3 object storage."""


@ecs.command()
@click.argument("url", required=False)
def endpoint(url):
    """Display / set / update the ECS endpoint URL."""
    if not url:
        click.secho(dtool_config.utils.get_ecs_endpoint(CONFIG_PATH))
    else:
        click.secho(dtool_config.utils.set_ecs_endpoint(CONFIG_PATH, url))


@ecs.command()
@click.argument("ecs_access_key_id", required=False)
def access_key_id(ecs_access_key_id):
    """Display / set / update the ECS access key id."""
    if not ecs_access_key_id:
        click.secho(dtool_config.utils.get_ecs_access_key_id(CONFIG_PATH))
    else:
        click.secho(dtool_config.utils.set_ecs_access_key_id(
            CONFIG_PATH,
            ecs_access_key_id
        ))


@ecs.command()
@click.argument("ecs_secret_access_key", required=False)
def secret_access_key(ecs_secret_access_key):
    """Display / set / update the ECS secret access key."""
    if not ecs_secret_access_key:
        click.secho(dtool_config.utils.get_ecs_secret_access_key(CONFIG_PATH))
    else:
        click.secho(dtool_config.utils.set_ecs_secret_access_key(
            CONFIG_PATH,
            ecs_secret_access_key
        ))


@config.group()
def cache():
    """Configure ECS S3 object storage."""


@cache.command()
@click.argument(
    "scheme",
    type=click.Choice(dtool_config.utils.CACHE_KEYS.keys())
)
def get(scheme):
    """Print the cache directory of the specific storage scheme."""
    click.secho(dtool_config.utils.get_cache(
        CONFIG_PATH,
        scheme
    ))


@cache.command()
@click.argument(
    "scheme",
    type=click.Choice(dtool_config.utils.CACHE_KEYS.keys())
)
@click.argument(
    "cache_directory_path",
    type=click.Path(exists=True, file_okay=False)
)
def set(scheme, cache_directory_path):
    """Configure the cache directory of the specific storage scheme."""
    click.secho(dtool_config.utils.set_cache(
        CONFIG_PATH,
        scheme,
        cache_directory_path
    ))


@cache.command()
def ls():
    """List the storage scheme cache directories."""
    for scheme in dtool_config.utils.CACHE_KEYS.keys():
        line = "{}\t{}".format(
            scheme,
            dtool_config.utils.get_cache(CONFIG_PATH, scheme)
        )
        click.secho(line)


@click.argument(
    "cache_directory_path",
    type=click.Path(exists=True, file_okay=False)
)
@cache.command()
def set_all(cache_directory_path):
    """Configure the cache directory for all storage schemes."""
    for scheme in dtool_config.utils.CACHE_KEYS.keys():
        click.secho(scheme + "\t", nl=False)
        click.secho(dtool_config.utils.set_cache(
            CONFIG_PATH,
            scheme,
            cache_directory_path
        ))


@config.group()
def azure():
    """Configure Azure Storage."""


@azure.command()  # NOQA
@click.argument("container")
def get(container):
    """Print the secret access key of the specified Azure storage container."""
    click.secho(dtool_config.utils.get_azure_secret_access_key(
        CONFIG_PATH,
        container,
    ))


@azure.command()  # NOQA
@click.argument("container")
@click.argument("azure_secret_access_key")
def set(container, azure_secret_access_key):
    """Set/update the access key for the specified Azure storage container."""
    click.secho(dtool_config.utils.set_azure_secret_access_key(
        CONFIG_PATH,
        container,
        azure_secret_access_key
    ))


@azure.command()  # NOQA
def ls():
    """List all Azure storage containers."""
    for container in dtool_config.utils.list_azure_containers(CONFIG_PATH):
        click.secho(container)
