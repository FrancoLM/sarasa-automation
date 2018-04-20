import os

from behave.__main__ import main
from configobj import ConfigObj
from argparse import ArgumentParser

# Config file which stores the Environment information
from slayer.slayer_configuration import set_env_variables, new_env_variable#, get_behave_args

LOG_CFG_FILE = os.path.join(os.getcwd(), "config", "logger.cfg")


def configure_environment():
    # TODO: Add validation for each variable
    # TODO: Support arguments as well as config variables
    parser = ArgumentParser(description='Slayer Framework... it came to SLAY!')
    parser.add_argument('--config', type=str, help='Configuration File', required=False, default="config/config.cfg")
    parser.add_argument('--behave-config', type=str, help='Configuration File for Behave-specific options',
                        required=False, default="config/behave.ini")

    # Proyect-specific variables (_) should be parsed separately
    default_args, _ = parser.parse_known_args()

    new_env_variable("CONFIG", default_args.config)
    new_env_variable("APPDATA", os.path.abspath(default_args.behave_config))


    set_env_variables()
    # set_behave_args()


def clean_output_folder():
    pass
    # raise("Not Implemented")


def configure_logging():
    # TODO: Fix logging to a file
    # TODO: Fix the printing of all scenarios in the console output
    # Create log folder
    pass
    #if not os.path.exists(logs_path):
    #   os.makedirs(logs_path)
    # get logging configuration
    #logger = logging.getLogger("SLAYER")
    #hdlr = logging.FileHandler(os.path.join(logs_path, "slayer.log"))
    #logger.addHandler(hdlr)
    #logging.config.fileConfig(LOG_CFG_FILE)


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

