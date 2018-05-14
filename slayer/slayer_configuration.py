import logging.config
import os
import sys
from argparse import ArgumentParser

import yaml
from behave.configuration import Configuration as BehaveConfig
from configobj import ConfigObj
from yaml.scanner import ScannerError

SLAYER_CONFIG = None


def new_env_variable(name, value, print_to_console=True):
    os.environ[name] = value
    if print_to_console:
        print("{var_name:>15} ==> {var_value}".format(var_name=name, var_value=value))


def get_config():
    global SLAYER_CONFIG
    if SLAYER_CONFIG is None:
        config_path = os.getenv("SLAYER_CONFIG")
        SLAYER_CONFIG = ConfigObj(config_path)
    return SLAYER_CONFIG


def clean_output_folder():
    pass
    # raise("Not Implemented")


def set_env_variables():
    cfg = get_config()
    slayer_cfg = cfg["slayer"]

    # Output folders
    new_env_variable("OUTPUT_DIR", os.path.join(os.getenv("SLAYER_ROOT"), slayer_cfg["output"]["path"]))
    new_env_variable("LOGS_DIR", os.path.join(os.getenv("OUTPUT_DIR"), slayer_cfg["logs"]["path"]))

    # Proxy
    new_env_variable("HTTP_PROXY", slayer_cfg["proxy"]["http_proxy"])
    new_env_variable("HTTPS_PROXY", slayer_cfg["proxy"]["https_proxy"])
    new_env_variable("NO_PROXY", slayer_cfg["proxy"]["no_proxy"])


def configure_logging(context):
    if not os.path.isdir(os.getenv("LOGS_DIR")):
        os.makedirs(os.getenv("LOGS_DIR"))
    try:
        with open(os.getenv("LOGS_CONFIG"), 'r') as f:
            log_config = yaml.safe_load(f.read())
        if "filename" in log_config["handlers"]["file"].keys():
            filename = log_config["handlers"]["file"]["filename"]
            log_config["handlers"]["file"]["filename"] = os.path.join(os.getenv("LOGS_DIR"), filename)
        logging.config.dictConfig(log_config)
    except KeyError:
        print("Could not load logging settings. Using default configuration")
    except ScannerError:
        print("There was an error when loading the logging configuration")
        raise


def configure_environment():
    parser = ArgumentParser(description='Slayer Framework... it came to SLAY!')
    parser.add_argument('--framework-config',
                        required=True,
                        action='store',
                        help='Slayer Framework Configuration File')
    parser.add_argument('--logs-config',
                        required=True,
                        help='Slayer Logs Configuration File')
    parser.add_argument('--behave-config',
                        required=False,
                        help='Relative Path for the Behave Configuration File. The file must be named "behave.ini"',
                        default="")

    default_args, other_args = parser.parse_known_args()

    # TODO: double-check slayer root. Make SLAYER_CONFIG configurable with a config file!
    new_env_variable("SLAYER_ROOT", os.getcwd())
    new_env_variable("APPDATA", os.path.join(os.getenv("SLAYER_ROOT"), default_args.behave_config))
    new_env_variable("SLAYER_CONFIG", os.path.join(os.getenv("SLAYER_ROOT"), default_args.framework_config))
    new_env_variable("LOGS_CONFIG", os.path.join(os.getenv("SLAYER_ROOT"), default_args.logs_config))

    # Remove the custom parameters from sys.argv
    sys.argv = sys.argv[:1] + other_args
    # Set env variables from the config file (--framework-config)
    set_env_variables()


def set_behave_args():
    # cfg_file = os.getenv("APPDATA")
    cfg = BehaveConfig()
    # Test logging
    # logging.getLogger().addHandler(cfg.outputs[0])
    # TODO: Create functions to load the config files (#21122)
    # cfg.environment_file = # Configurable by user
    return cfg