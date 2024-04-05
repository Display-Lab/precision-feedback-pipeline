from loguru import logger
import sys
import os
from decouple import Config, RepositoryEnv, config

## Logging setup
logger.remove()
logger.add(sys.stdout, colorize=True, format="{level} | {message}")

## Control switch for production and dev configurations
# User specifies custom env var set to use on startup, else errors out at loading 'templates'
env_path = os.environ.get("ENV_PATH")
if env_path is not None:
    logger.debug(
        f"ENV_PATH specified. Running from environment variables in {env_path}..."
    )
    config = Config(RepositoryEnv(env_path))
else:
    logger.debug(
        "ENV_PATH not specified, running from manually set environment variables..."
    )


## Settings class to store decoupled instance and build settings:
class Settings:
    def __init__(self):
        # Knowledge settings
        self.templates = config("templates", cast=str)
        self.pathways = config("pathways", cast=str)
        self.measures = config("measures", cast=str)
        self.mpm = config("mpm", cast=str)
        self.comparators = config("comparators", cast=str)

        # Instance settings
        self.log_level = config(
            "log_level", cast=str, default="INFO"
        )  # Logging level for instance
        self.generate_image = config(
            "generate_image", cast=bool, default=True
        )  # Generate image flag (pictoraless)
        self.cache_image = config(
            "cache_image", cast=bool, default=False
        )  # Cache generated image flag
        self.outputs = config(
            "outputs", cast=bool, default=False
        )  # Logging of intermediate files


        # Instance display settings
        self.display_window = config("display_window", cast=int, default=6)
        self.plot_goal_line = config("plot_goal_line", cast=bool, default=True)


# Instantiate
settings = Settings()
