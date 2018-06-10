import logging.config
import os
import shutil
import sys
from argparse import ArgumentParser

import yaml
from yaml.scanner import ScannerError

from slayer.slayer_configuration import get_slayer_configuration


class SlayerRunner(object):
    """Slayer framework object."""

    def __init__(self):
        self.variables = {}
        self.arguments = None

    @classmethod
    def print_banner(cls):
        """Prints the SLayer Banner in console"""
        print("SLAYER FRAMEWORK".center(38, "-"))
        print("-" * 38)

    def set_new_environment_variable(self, name, value, print_to_console=True):
        """Creates a new environment variable and stores it in the variables attribute.

        Keyword arguments:
        name -- the name of the new environment variable
        value -- the value it will be assigned
        print_to_console -- whether to print the variable in the console (default True)
        """
        try:
            os.environ[name] = value
            self.variables[name] = value
            if print_to_console:
                print("{var_name:>15} ==> {var_value}".format(var_name=name, var_value=value))
            return self.variables[name]
        except TypeError:
            print("ERROR. Environment variable {} could not be set!".format(name))
            raise

    def overwrite_default_configuration(self):
        pass

    def parse_slayer_arguments(self):
        """Reads the Slayer-specific arguments provided in the execution of Slayer."""
        parser = ArgumentParser(description='Slayer Framework... it came to SLAY!')
        parser.add_argument('--slayer-config',
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

        default_args, other_args = parser.parse_known_args()
        self.arguments = default_args

        # Remove the custom parameters from sys.argv
        sys.argv = sys.argv[:1] + other_args

    def set_environment_variables(self):
        """Sets the value for all the Slayer-related environment variables"""
        args = self.arguments

        # Set the environment SLAYER_ROOT to the path where the main script is executed. This is to provide
        # Slayer with the ability of using custom config and feature files and modify behavior mid-execution
        self.set_new_environment_variable("SLAYER_ROOT", os.getcwd())

        slayer_config = os.path.join(self.variables["SLAYER_ROOT"], args.slayer_config)
        self.set_new_environment_variable("SLAYER_CONFIG", slayer_config)

        logs_config = os.path.join(self.variables["SLAYER_ROOT"], args.logs_config)
        self.set_new_environment_variable("LOGS_CONFIG", logs_config)

        # APPDATA is used by the Behave executor
        app_data = os.path.join(self.variables["SLAYER_ROOT"], args.behave_config)
        self.set_new_environment_variable("APPDATA", app_data)

        # Get the configuration options from the Slayer config file
        cfg = get_slayer_configuration()
        slayer_cfg = cfg["slayer"]

        slayer_output_dir = os.path.join(self.variables["SLAYER_ROOT"], slayer_cfg["output"]["path"])
        self.set_new_environment_variable("SLAYER_OUTPUT_DIR", slayer_output_dir)

        slayer_logs_dir = os.path.join(self.variables["SLAYER_OUTPUT_DIR"], slayer_cfg["logs"]["path"])
        self.set_new_environment_variable("SLAYER_LOGS_DIR", slayer_logs_dir)

        proxy = slayer_cfg["proxy"]
        self.set_new_environment_variable("HTTP_PROXY", proxy["http_proxy"])
        self.set_new_environment_variable("HTTPS_PROXY", proxy["https_proxy"])
        self.set_new_environment_variable("NO_PROXY", proxy["no_proxy"])

    def cleanup_output_folder(self):
        """Creates and empties the folder where the output artifacts and logs will be stored after executing Slayer"""
        self.delete_output_folders()
        output_folder = self.variables["SLAYER_OUTPUT_DIR"]
        logs_folder = self.variables["SLAYER_LOGS_DIR"]
        for folder in (output_folder, logs_folder):
            if not os.path.isdir(folder):
                os.makedirs(folder)

    def delete_output_folders(self):
        """Cleans the output folder, where the logs and results of the execution are stored."""
        shutil.rmtree(self.variables["SLAYER_OUTPUT_DIR"], ignore_errors=True)

    def configure_execution(self):
        self.configure_logging()

    def configure_logging(self):
        """Reads the logger configuration file and set the logger for Slayer.

        Function sets all config-related settings, like log-level and format. If the config file cannot be found,
        then the default logger file is used
        """
        try:
            with open(self.variables["LOGS_CONFIG"], 'r') as f:
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
