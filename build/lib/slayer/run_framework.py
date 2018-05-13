import os

from behave.__main__ import run_behave
from behave.configuration import Configuration as BehaveConfig
from argparse import ArgumentParser
import logging.config
import yaml

from yaml.scanner import ScannerError
from slayer.slayer_configuration import set_env_variables, new_env_variable


def configure_environment():
    # TODO: Add validation for each variable
    # TODO: Support arguments as well as config variables
    parser = ArgumentParser(description='Slayer Framework... it came to SLAY!')
    parser.add_argument('--framework-config', type=str, help='Slayer Framework Configuration File', required=False,
                        default="config.cfg")
    parser.add_argument('--logs-config', type=str, help='Slayer Logs Configuration File', required=False,
                        default="logger.yaml")
    # TODO: See if it's possible to relocate the behave config file

    # Proyect-specific variables (_) should be parsed separately
    default_args, _ = parser.parse_known_args()

    # TODO: double-check slayer root
    new_env_variable("SLAYER_ROOT", os.getcwd())
    new_env_variable("SLAYER_CONFIG", os.path.join(os.getenv("SLAYER_ROOT"), "config", default_args.framework_config))
    new_env_variable("LOGS_CONFIG", os.path.join(os.getenv("SLAYER_ROOT"), "config", default_args.logs_config))
    new_env_variable("APPDATA", os.path.join(os.getenv("SLAYER_ROOT")))

    # Set env variables from the config file (--framework-config)
    set_env_variables()


def clean_output_folder():
    pass
    # raise("Not Implemented")


def configure_logging(context):
    # FIXME: Support DEBUG logging. This logger is created before the logging configuration for behave
    #   is called. Since behave configures the root logger, the configuration is overwritten.
    # FIXME: Log file should include the behave output too
    # Create log folder
    if not os.path.isdir(os.getenv("LOGS_DIR")):
        os.makedirs(os.getenv("LOGS_DIR"))
    try:
        with open(os.getenv("LOGS_CONFIG"), 'r') as f:
            log_config = yaml.safe_load(f.read())
        # Configure output dir for the file logger (if available)
        # TODO: Improve in the future. Find by Handler class recursively
        if "filename" in log_config["handlers"]["file"].keys():
            filename = log_config["handlers"]["file"]["filename"]
            log_config["handlers"]["file"]["filename"] = os.path.join(os.getenv("LOGS_DIR"), filename)
        logging.config.dictConfig(log_config)
        # logging.getLogger().handlers[1].stream = context.config.outputs[0].stream
    except KeyError:
        print("Could not load logging settings. Using default configuration")
    except ScannerError:
        print("There was an error when loading the logging configuration")
        raise


def set_behave_args():
    # cfg_file = os.getenv("APPDATA")
    cfg = BehaveConfig()
    # Test logging
    # logging.getLogger().addHandler(cfg.outputs[0])
    # TODO: Create functions to load the config files (#21122)
    # cfg.environment_file = # Configurable by user
    return cfg


def behave_executor(behave_config):
    # Behave-specific configuration
    run_behave(behave_config)


def run_framework():
    print("SLAYER FRAMEWORK".center(35, "-"))
    print("-" * 35)
    # Set env vairables and paths
    configure_environment()
    clean_output_folder()
    # Read behave config file and customize it for SLAYER
    behave_config = set_behave_args()
    # configure_logging()
    # Run tests with the behave executor
    behave_executor(behave_config)
    # TODO: Reporter Factory
    # generate_report()
