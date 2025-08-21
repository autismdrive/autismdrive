import os
from typing import Literal

import click

from config.base import Settings

type EnvName = Literal[
    "ci",
    "docker",
    "local",
    "mirror",
    "template",
    "testing",
]

_error_message = (
    "Environment variable 'ENV_NAME' is not set. Please set it to one of the following "
    "valid environment names: 'ci', 'docker', 'local', 'mirror', 'template', or 'testing'."
)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SettingsSingleton(metaclass=Singleton):
    """
    Creates a singleton instance of Settings that can be accessed globally.
    """

    _instance: Settings = None
    _env_name: EnvName = None

    def __new__(cls) -> Settings:
        """
        Initializes the singleton instance with the environment name from the environment variable `ENV_NAME`.
        If an instance already exists for the current environment name, it returns that instance. If the environment
        variable `ENV_NAME` has changed, it reinitializes the instance with the new environment name.

        Runs BEFORE a SettingsSingleton instance object is created.
        """

        env_name = os.getenv("ENV_NAME", default=None)
        click.secho(f"\n*** config.load.SettingsSingleton.__new__ > env_name: {env_name} ***\n")

        if env_name is None:
            raise ValueError(
                "Environment variable 'ENV_NAME' is not set. Please set it to one of the valid environment names."
            )

        if cls._instance is not None and cls._env_name == env_name:
            click.secho(
                f"\n*** config.load.SettingsSingleton.__new__ > Using existing instance for env_name: {env_name} ***\n"
            )

        else:
            click.secho(
                f"\n*** config.load.SettingsSingleton.__new__ > Creating new instance for env_name: {env_name} ***\n"
            )
            cls._instance = cls.load_settings()

        return cls._instance

    @classmethod
    def load_settings(cls) -> Settings:
        env_name = os.getenv("ENV_NAME", default=None)
        click.secho(f"\n*** config.load.SettingsSingleton.__new__ > env_name: {env_name} ***\n")

        if env_name is None:
            raise ValueError(
                "Environment variable 'ENV_NAME' is not set. Please set it to one of the valid environment names."
            )

        # Load settings from a specific environment file based on the environment name
        # Get the absolute path of the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the environment file
        env_file_path = os.path.join(current_dir, "env", f"{env_name}.env")

        click.secho(f"\n*** config.load.load_settings > env_file_path = {env_file_path} ***\n")
        new_settings = Settings(_env_file=env_file_path, _env_file_encoding="utf-8")

        click.secho(f"\n*** config.load.load_settings > new_settings.NAME = {new_settings.NAME} ***\n")
        return new_settings


settings = SettingsSingleton()
