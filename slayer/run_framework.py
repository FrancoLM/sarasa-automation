from behave.__main__ import run_behave

from slayer.slayer_configuration import set_behave_config
from slayer.slayer_configuration import Slayer


def behave_executor(behave_config):
    """Calls the Behave executor to run the scenarios"""
    run_behave(behave_config)


def run_framework():
    """Sets all settings for executing Slayer.

    - Configures the necessary environment variables
    -- logger
    -- output folder
    -- Slayer report
    - Sets Behave-specific variables, like the paths where the feature files will be located and tags to run
    - Calls the behave executor"""
    slayer_framework = Slayer()
    slayer_framework.print_banner()

    # Set env variables and paths
    slayer_framework.configure_environment()
    slayer_framework.set_slayer_environment_variables()
    slayer_framework.create_output_folders()
    #clean_output_folder()

    # Read the Behave config file and customize it for SLAYER
    behave_config = set_behave_config()
    # configure_logging()
    # Run tests with the behave executor
    slayer_framework.configure_logging()
    behave_executor(behave_config)
    # TODO: Reporter Factory
    # generate_report()


if __name__ == "__main__":
    run_framework()
