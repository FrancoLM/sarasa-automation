from behave.__main__ import run_behave

from slayer_class import Slayer
from slayer_configuration import set_behave_arguments


def behave_executor(behave_config):
    """Calls the Behave executor to run the scenarios"""
    run_behave(behave_config)


def run_framework():
    """Sets all the settings required for executing Slayer.

    - Configures the necessary environment variables
    -- logger
    -- output folder
    -- Slayer report
    - Sets Behave-specific variables, like the paths where the feature files will be located and tags to run
    - Calls the behave executor"""
    slayer_framework = Slayer()
    slayer_framework.print_banner()

    # Set env variables and paths
    slayer_framework.set_arguments_from_command_line()
    slayer_framework.set_slayer_environment_variables()
    slayer_framework.create_output_folders()
    #clean_output_folders()

    # Read the Behave config file and customize it for SLAYER
    behave_config = set_behave_arguments()
    # configure logging for Slayer. This step needs to be executed after creating the behave config object since
    # Slayer overrides some of the settings behave sets for logging
    slayer_framework.configure_logging()

    # Run tests with the behave executor
    behave_executor(behave_config)
    # TODO: Reporter Factory
    # generate_report()


if __name__ == "__main__":
    run_framework()
