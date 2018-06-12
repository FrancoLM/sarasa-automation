from slayer.behave_executor import BehaveExecutor
from slayer.slayer_runner import SlayerRunner
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


def run_framework():
    """Sets all the settings required for executing Slayer.

    - Configures the necessary environment variables
    -- logger
    -- output folder
    -- Slayer report
    - Sets Behave-specific variables, like the paths where the feature files will be located and tags to run
    - Calls the behave executor"""
    slayer_runner = SlayerRunner()
    slayer_runner.print_banner()

    slayer_runner.parse_slayer_arguments()
    slayer_runner.set_environment_variables()

    slayer_runner.cleanup_output_folder()

    behave_executor = BehaveExecutor()
    behave_executor.create_behave_config()
    behave_executor.parse_behave_arguments()

    # configure execution for Slayer. This step needs to be executed after creating the behave config object since
    # Slayer overrides some of the settings behave sets when importing the library
    slayer_runner.configure_execution()

    behave_executor.import_steps_directories()
    behave_executor.call_executor()
    # TODO: Reporter Factory
    # generate_report()


if __name__ == "__main__":
    run_framework()
