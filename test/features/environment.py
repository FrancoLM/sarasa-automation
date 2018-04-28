"""Environment file for behave"""
from slayer.run_framework import configure_logging


def before_all(context):
    # Setup logging for SLAYER, according to behave API reference:
    # http://python-behave.readthedocs.io/en/latest/api.html#logging-setup
    configure_logging()
