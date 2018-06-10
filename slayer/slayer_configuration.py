import os

from configobj import ConfigObj

SLAYER_CONFIG = None


def get_slayer_configuration():
    """Gets the Slayer configuration, an object with all the settings for running Slayer.

    The Slayer configuration is stored in a global variable, and allows to modify the execution of Slayer."""
    global SLAYER_CONFIG
    if SLAYER_CONFIG is None:
        config_path = os.getenv("SLAYER_CONFIG")
        SLAYER_CONFIG = ConfigObj(config_path)
    return SLAYER_CONFIG


