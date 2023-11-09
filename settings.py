from decouple import Config, RepositoryEnv, config
import os

## Control switch for production and dev configurations
# User specifies custom env var set to use on startup, else errors out at loading 'templates'
env_path = os.environ.get('ENV_PATH')
if env_path != None:
    print(f"ENV_PATH specified. Running from environment variables in {env_path}...")
    config = Config(RepositoryEnv(env_path))
else:
    print(f"ENV_PATH not specified, running from manually set environment variables...")


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

# Debug print (implent when logging handler sorted)
print(f"Startup configuration for this instance:")
for attribute in dir(settings):
    if not attribute.startswith("__"):
        value = getattr(settings, attribute)
        print(f"{attribute}:\t{value}")
