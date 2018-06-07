import os
import sys
from argparse import ArgumentParser

from behave.configuration import Configuration as BehaveConfig
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


def set_behave_arguments():
    """Sets behave-specific arguments

    Note: This function uses both the arguments in the behave.ini file and the command line arguments, but the latter
    take precedence."""
    # TODO: Mention the arguments
    parser = ArgumentParser()
    # Behave arguments
    # TODO: Complete with the rest of the arguments
    cfg = BehaveConfig(sys.argv[1:])

    cfg.environment_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "environment.py")
    # Test logging
    # logging.getLogger().addHandler(cfg.outputs[0])
    # TODO: Create functions to load the config files (#21122)
    # cfg.environment_file = # Configurable by user
    return cfg
