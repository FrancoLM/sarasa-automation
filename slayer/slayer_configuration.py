import logging.config
import os
import sys
from argparse import ArgumentParser

import yaml
from behave.configuration import Configuration as BehaveConfig
from configobj import ConfigObj
from yaml.scanner import ScannerError

SLAYER_CONFIG = None


class Slayer(object):
    """Slayer framework object."""

    def __init__(self):
        self.variables = {}
        self.arguments = None

    @classmethod
    def print_banner(self):
        print("SLAYER FRAMEWORK".center(35, "-"))
        print("-" * 35)

    def configure_environment(self):
        """Reads the arguments passed to the execution of Slayer."""
        parser = ArgumentParser(description='Slayer Framework... it came to SLAY!')
        parser.add_argument('--framework-config',
                            required=False,
                            action='store',
                            help='Slayer Framework Configuration File',
                            default='{}{}config{}config.cfg'.format(os.path.dirname(__file__), os.sep, os.sep))
        parser.add_argument('--logs-config',
                            required=False,
                            help='Slayer Logs Configuration File',
                            default='{}{}config{}logger.yaml'.format(os.path.dirname(__file__), os.sep, os.sep))
        parser.add_argument('--behave-config',
                            required=False,
                            help='Relative Path for the Behave Configuration File. The file must be named "behave.ini"',
                            default='')
        parser.add_argument('--tags',
                            required=False,
                            help='Tags for the tests that will be executed',
                            default='')
        default_args, other_args = parser.parse_known_args()
        self.arguments = default_args
        # self.set_slayer_environment_variables(default_args)

        # Remove the custom parameters from sys.argv
        sys.argv = sys.argv[:1] + other_args
        # Set env variables from the config file (--framework-config)

    def set_slayer_environment_variables(self):
        """Set the value for all the Slayer-related environment variables"""
        args = self.arguments
        # Set the environment SLAYER_ROOT to the path where the main script is executed. This is to provide
        # SLayer with the ability of using custom config and feature files
        self.variables["SLAYER_ROOT"] = self.set_new_environment_variable("SLAYER_ROOT", os.getcwd())

        slayer_config = os.path.join(os.getenv("SLAYER_ROOT"), args.framework_config)
        self.variables["SLAYER_CONFIG"] = self.set_new_environment_variable("SLAYER_CONFIG", slayer_config)

        logs_config = os.path.join(os.getenv("SLAYER_ROOT"), args.logs_config)
        self.variables["LOGS_CONFIG"] = self.set_new_environment_variable("LOGS_CONFIG", logs_config)

        app_data = os.path.join(os.getenv("SLAYER_ROOT"), args.behave_config)
        self.variables["APPDATA"] = self.set_new_environment_variable("APPDATA", app_data)



        # Get the configuration options from the Slayer config file
        cfg = get_slayer_configuration()
        slayer_cfg = cfg["slayer"]

        # Set output-related environment variables
        slayer_output_dir = os.path.join(os.getenv("SLAYER_ROOT"), slayer_cfg["output"]["path"])
        self.variables["SLAYER_OUTPUT_DIR"] = self.set_new_environment_variable("SLAYER_OUTPUT_DIR", slayer_output_dir)

        slayer_logs_dir = os.path.join(os.getenv("SLAYER_OUTPUT_DIR"), slayer_cfg["logs"]["path"])
        self.variables["SLAYER_LOGS_DIR"] = self.set_new_environment_variable("SLAYER_LOGS_DIR", slayer_logs_dir)

        # Set Proxy-related environment variables
        proxy = slayer_cfg["proxy"]
        self.variables["HTTP_PROXY"] = self.set_new_environment_variable("HTTP_PROXY", proxy["http_proxy"])
        self.variables["HTTPS_PROXY"] = self.set_new_environment_variable("HTTPS_PROXY", proxy["https_proxy"])
        self.variables["NO_PROXY"] = self.set_new_environment_variable("NO_PROXY", proxy["no_proxy"])

    def clean_output_folders(self):
        """Clean the output folder, where the logs and results of the execution are stored."""
        pass
        # TODO: Not Implemented

    @classmethod
    def set_new_environment_variable(cls, name, value, print_to_console=True):
        """Create a new environment variable.

        Keyword arguments:
        name -- the name of the new environment variable
        value -- the value it will be assigned
        print_to_console -- whether to print the variable in the console (default True)
        """
        try:
            os.environ[name] = value
            if print_to_console:
                print("{var_name:>15} ==> {var_value}".format(var_name=name, var_value=value))
            return os.environ.get(name)
        except TypeError:
            print("ERROR. Environment variable {} could not be set!".format(name))
            raise

    def create_output_folders(self):
        output_folder = self.variables["SLAYER_OUTPUT_DIR"]
        logs_folder = self.variables["SLAYER_LOGS_DIR"]
        for folder in (output_folder, logs_folder):
            if not os.path.isdir(folder):
                os.makedirs(folder)

    @classmethod
    def configure_logging(cls):
        """Read the logger configuration file and set the logger for Slayer.

        Function sets all config-related settings, like log-level and format. If the config file cannot be found,
        then the default logger file is used
        """
        try:
            with open(os.getenv("LOGS_CONFIG"), 'r') as f:
                log_config = yaml.safe_load(f.read())
            if "filename" in log_config["handlers"]["file"].keys():
                filename = log_config["handlers"]["file"]["filename"]
                log_config["handlers"]["file"]["filename"] = os.path.join(os.getenv("SLAYER_LOGS_DIR"), filename)
            logging.config.dictConfig(log_config)
        except KeyError:
            print("Could not load logging settings. Using default configuration")
        except ScannerError:
            print("There was an error when loading the logging configuration")
            raise


def get_slayer_configuration():
    """Get the Slayer configuration, an object with all the settings for running Slayer."""
    global SLAYER_CONFIG
    if SLAYER_CONFIG is None:
        config_path = os.getenv("SLAYER_CONFIG")
        SLAYER_CONFIG = ConfigObj(config_path)
    return SLAYER_CONFIG


def set_behave_config():
    # cfg_file = os.getenv("APPDATA")
    cfg = BehaveConfig()
    cfg.environment_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "environment.py")
    # Test logging
    # logging.getLogger().addHandler(cfg.outputs[0])
    # TODO: Create functions to load the config files (#21122)
    # cfg.environment_file = # Configurable by user
    return cfg
