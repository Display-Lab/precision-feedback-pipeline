from dotenv import dotenv_values
from decouple import config
import pprint
import os

## Control switch for production and dev configurations
# User specifies custom env var set to use on startup, else uses prod environment file
env_path = os.environ.get('ENV_PATH', default='.env.remote')

# Merge env vars from selected .env to the current environment (respecting unix way):
os.environ.update(dotenv_values(env_path))

## Settings class to store decoupled instance and build settings:
class Settings:
    def __init__(self):
        # Knowledge settings
        self.templates = config('templates', cast=str)
        self.pathways  = config('pathways', cast=str)
        self.measures  = config('measures', cast=str)
        self.mpm       = config('mpm', cast=str)

        # Instance settings
        self.log_level      = config('log_level', cast=str)    # Logging level for instance
        self.generate_image = config('generate_image', cast=bool)   # Generate image flag (pictoraless)
        self.cache_image    = config('cache_image', cast=bool)      # Cache generated image flag

        # Instance display settings
        self.display_window = config('display_window', cast=int)
        self.plot_goal_line = config('plot_goal_line', cast=bool)

# Instantiate
settings = Settings()

# Debug
print(f"Startup configuration for this instance:")
for attribute in dir(settings):
    if not attribute.startswith("__"):
        value = getattr(settings, attribute)
        print(f"{attribute}:\t{value}")
