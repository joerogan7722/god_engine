"""
Initialize registry and core directives for the god_engine.
"""

from .framework_registry import FrameworkRegistry
from .config import load_config

# Initialize and register core components
config = load_config()
registry = FrameworkRegistry(config)

print("god_engine initialized.")
