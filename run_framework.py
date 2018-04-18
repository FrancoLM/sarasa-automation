import os

from behave.__main__ import run_behave, main
from behave.configuration import Configuration as BehaveConfiguration

from configobj import ConfigObj
import argparse
import logging
import logging.config

# Config file which stores the Environment information
FW_CFG_FILE = os.path.join(os.getcwd(), "config", "config.cfg")
LOG_CFG_FILE = os.path.join(os.getcwd(), "config", "logger.cfg")


def configure_environment():
    # Read the environment information from the config file
    fw_cfg_parser = ConfigObj(FW_CFG_FILE)

    # TODO: Fix logging to a file
    # Create log folder
    logs_path = os.path.join(fw_cfg_parser["framework"]["output"]["path"], fw_cfg_parser["framework"]["logs"]["path"])
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    # get logging configuration
    logger = logging.getLogger("SLAYER")
    hdlr = logging.FileHandler(os.path.join(logs_path, "slayer.log"))
    logger.addHandler(hdlr)
    logging.config.fileConfig(LOG_CFG_FILE)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Slayer Framework... it came to SLAY!')
    # parser.add_argument("")
    # parser.parse_args()

    configure_environment()

    # replace
    args = ["test/features"]

    # Behave-specific configuration
    config = BehaveConfiguration(args)
    run_behave(config)
    #behave_main(args)
