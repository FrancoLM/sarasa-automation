import os

from behave.__main__ import main
from argparse import ArgumentParser
import logging.config
import yaml

# Config file which stores the Environment information
from yaml.scanner import ScannerError

from slayer.slayer_configuration import set_env_variables, new_env_variable#, get_behave_args


def configure_environment():
    # TODO: Add validation for each variable
    # TODO: Support arguments as well as config variables
    parser = ArgumentParser(description='Slayer Framework... it came to SLAY!')
    parser.add_argument('--framework-config', type=str, help='Slayer Framework Configuration File', required=False, default="config.cfg")
    parser.add_argument('--logs-config', type=str, help='Slayer Logs Configuration File', required=False, default="logger.yaml")
    # TODO: See if it's possible to relocate the behave config file
    # parser.add_argument('--behave-config', type=str, help='Configuration File for Behave-specific options',
    #                     required=False, default="behave.ini")

    # Proyect-specific variables (_) should be parsed separately
    default_args, _ = parser.parse_known_args()

    new_env_variable("SLAYER_ROOT", os.getcwd())
    new_env_variable("SLAYER_CONFIG", os.path.join(os.getenv("SLAYER_ROOT"), "config", default_args.framework_config))
    new_env_variable("LOGS_CONFIG", os.path.join(os.getenv("SLAYER_ROOT"), "config", default_args.logs_config))
    new_env_variable("APPDATA", os.path.join(os.getenv("SLAYER_ROOT"), "behave.ini"))


    set_env_variables()
    # set_behave_args()


def clean_output_folder():
    pass
    # raise("Not Implemented")


def configure_logging():
    # FIXME: Support DEBUG logging. This logger is created before the logging configuration for behave
    #   is called. Since behave configures the root logger, the configuration is overwritten.
    # FIXME: Log file should include the behave output too
    # Create log folder
    if not os.path.isdir(os.getenv("LOGS_DIR")):
        os.makedirs(os.getenv("LOGS_DIR"))

    # get logging configuration
    # dictConfig()
    try:
        with open(os.getenv("LOGS_CONFIG"), 'r') as f:
            log_config = yaml.safe_load(f.read())
        logging.config.dictConfig(log_config)
    except ScannerError:
        print("There has been an error loading the logging configuration")
        raise

    print("Logger configured")


def behave_executor():
    # Behave-specific configuration
    #config = get_behave_args()
    #cfg = behave_main.Configuration(config)
    #behave_main.run_behave(cfg)
    main()


def run_framework():
    configure_environment()
    clean_output_folder()
    configure_logging()

    behave_executor()
    # TODO: Reporter Factory
    # generate_report()

