from dotenv import dotenv_values
from decouple import config
import pprint
import os

## Control switch for production and dev configurations
# Set is_prod as a boolean, developers should set env var to 0 when dev testing
is_prod = bool(int(os.environ.get('IS_PROD', default='1')))

if is_prod:
    # Load configuration that loads from remote knowledgebase
    env = dotenv_values('.env.remote')      

else:
    # Load configuration for local knowledge startup for development
    env = dotenv_values('.env.local')

# Merge env vars from selected .env to the current environment:
os.environ.update(env)  # Respects the unix way, CLI variable settings take precedence

## Settings class to store decoupled instance and build settings:
class Settings:
    def __init__(self):
        # Knowledge settings
        self.templates = config('templates', cast=str, default='https://api.github.com/repos/Display-Lab/knowledge-base/contents/message_templates')
        self.pathways  = config('pathways', cast=str, default='https://api.github.com/repos/Display-Lab/knowledge-base/contents/causal_pathways')
        self.measures  = config('measures', cast=str, default='https://raw.githubusercontent.com/Display-Lab/knowledge-base/main/measures.json')
        self.mpm       = config('mpm', cast=str, default='https://raw.githubusercontent.com/Display-Lab/knowledge-base/main/motivational_potential_model.csv')

        # Instance settings
        self.log_level      = config('log_level', cast=str, default='INFO')    # Logging level for instance
        self.generate_image = config('generate_image', cast=bool, default=1)   # Generate image flag (pictoraless)
        self.cache_image    = config('cache_image', cast=bool, default=0)      # Cache generated image flag

        # Instance display settings
        self.display_window = config('display_window', cast=int, default=6)
        self.plot_goal_line = config('plot_goal_line', cast=bool, default=1)

# Instantiate
settings = Settings()

# Debug
print(f"Startup configuration for this instance:")
for attribute in dir(settings):
    if not attribute.startswith("__"):
        value = getattr(settings, attribute)
        print(f"{attribute}:\t{value}")
