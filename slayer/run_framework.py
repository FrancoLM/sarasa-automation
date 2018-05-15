from behave.__main__ import run_behave

from slayer.slayer_configuration import configure_environment, set_behave_config


def behave_executor(behave_config):
    # Behave-specific configuration
    run_behave(behave_config)


def run_framework():
    print("SLAYER FRAMEWORK".center(35, "-"))
    print("-" * 35)
    # Set env vairables and paths
    configure_environment()
    #clean_output_folder()
    # Read behave config file and customize it for SLAYER
    behave_config = set_behave_config()
    # configure_logging()
    # Run tests with the behave executor
    behave_executor(behave_config)
    # TODO: Reporter Factory
    # generate_report()


if __name__ == "__main__":
    run_framework()
