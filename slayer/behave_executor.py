import os
import sys
import fnmatch
from argparse import ArgumentParser

from behave.__main__ import run_behave
from behave.configuration import Configuration as BehaveConfig
from behave.formatter.base import StreamOpener


class BehaveExecutor(object):

    def __init__(self):
        self.behave_config = None
        """Sets behave-specific arguments.

                Note: This function uses both the arguments in the behave.ini file and the command line arguments, but the latter
                take precedence."""
        # TODO: cannot send parameters
        # TODO: Mention the arguments

    def parse_behave_arguments(self):
        """Reads the Behave-specific arguments provided in the execution of Slayer."""
        parser = ArgumentParser()
        # Behave arguments
        # TODO: Complete with the rest of the arguments

    def create_behave_config(self):
        self.behave_config = BehaveConfig(sys.argv[1:])
        # TODO: Create functions to load the config files
        # cfg.environment_file = # Configurable by user

    def call_executor(self):
        """Calls the Behave executor to run the scenarios"""
        run_behave(self.behave_config)

    def setup_allure_logger(self, output_directory):
        # Insert the Allure formatter as the first element of the outputs list, in order to make it match with the
        # formats (since the default Behave formatter does not add a format)
        # TODO: improve description
        allure_report_directory = "allure"
        self.behave_config.outputs.insert(0, StreamOpener(filename=os.path.join(output_directory, allure_report_directory)))
        self.behave_config.format.append("allure_behave.formatter:AllureFormatter")


    @classmethod
    def import_steps_directories(cls):
        """Imports steps subdirectories.

        The steps directory, along with its subfolders are imported in order to let Behave find the steps.
        This allows Slayer to have the features and steps anywhere, regardless of where in the path it's called."""
        features_directory = os.path.join(os.path.dirname(sys.argv[0]), "features")

        # os.environ.setdefault('FEATURES_PATH', FEATURES_DIRECTORY)
        sys.path.append(features_directory)
        for dirpath, dirnames, filenames in os.walk(features_directory):
            for directory in dirnames:
                filenames = os.listdir(os.path.join(dirpath, directory))
                for python_script in fnmatch.filter(filenames, "*.py"):
                    if python_script == '__init__.py':
                        continue
                    python_module = directory + "." + python_script[:-3]
                    if dirpath != features_directory:
                        python_module = dirpath.replace(features_directory, "")[1:] + "." + python_module
                        python_module = python_module.replace(os.sep, ".")
                    __import__(python_module, locals(), globals())
        del sys.path[-1]
