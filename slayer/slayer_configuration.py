import os

from configobj import ConfigObj

FWK_CONFIG = None


def get_slayer_configuration():
    """Gets the Slayer configuration, an object with all the settings for running Slayer.

    The Slayer configuration is stored in a global variable, and allows to modify the execution of Slayer."""
    global FWK_CONFIG
    if FWK_CONFIG is None:
        config_path = os.getenv("FWK_CONFIG")
        FWK_CONFIG = ConfigObj(config_path)
    return FWK_CONFIG


