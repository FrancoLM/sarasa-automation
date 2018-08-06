from slayer.behave_executor import BehaveExecutor
from slayer.slayer_runner import SlayerRunner
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


def run_framework(framework_name="SLAYER"):
    """Sets all the settings required for executing Slayer.

    - Configures the necessary environment variables
    -- logger
    -- output folder
    -- Slayer report
    - Sets Behave-specific variables, like the paths where the feature files will be located and tags to run
    - Calls the behave executor"""

    slayer_runner = SlayerRunner(framework_name)
    slayer_runner.parse_slayer_arguments()
    slayer_runner.set_environment_variables()

    # Duplicate stdout to the slayer logger file
    slayer_runner.configure_stdout_logger()

    # configure execution for Slayer. This step needs to be executed after creating the behave config object since
    # Slayer overrides some of the settings behave sets when importing the library
    slayer_runner.configure_execution()

    # FIXME: Add variable for not printing the banner
    slayer_runner.log_slayer_information()

    slayer_runner.cleanup_output_folder()

    # FIXME: Mention in doc that adding logging in the environment.py file could mess up the logging (for the before_all
    # FIXME: especially. Maybe a new logger could be added....
    behave_executor = BehaveExecutor()
    behave_executor.create_behave_config()
    behave_executor.parse_behave_arguments()

    behave_executor.import_steps_directories()
    behave_executor.call_executor()
    # TODO: Refactor results output (execution summary)
    # TODO: Reporter Factory
    # generate_report()


if __name__ == "__main__":
    run_framework(framework_name="SLAYER-dev")
