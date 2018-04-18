import os

from behave.__main__ import run_behave
from behave.configuration import Configuration as BehaveConfiguration

from configobj import ConfigObj
import argparse


# Config file which stores the Environment information
FW_CFG_FILE = os.path.join(os.getcwd(), "config", "config.cfg")



def configure_environment():
    # Read the environment information from the config file
    fw_cfg_parser = ConfigObj(FW_CFG_FILE)

    # Read logger formatter information from the config file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Slayer Framework... it came to SLAY!')
    # parser.add_argument("")
    # parser.parse_args()

    configure_environment()

    # replace
    args = "test/features"

    # Behave-specific configuration
    config = BehaveConfiguration(args)
    run_behave(config)
    #behave_main(args)
