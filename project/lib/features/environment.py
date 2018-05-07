"""Environment file for behave
Selenium grid may be set here too"""
import logging
from slayer.run_framework import configure_logging
from behave.log_capture import capture

LINE_LENGTH = 42


def before_all(context):
    # Setup logging for SLAYER, according to behave API reference:
    # http://python-behave.readthedocs.io/en/latest/api.html#logging-setup
    configure_logging(context)


def after_all(context):
    for feature in context._runner.features:
        scenarios = feature.scenarios
        logging.info("PASSED Scenarios:")
        [logging.info(scenario.name) for scenario in scenarios if scenario.status.name == "passed"]
        logging.info("FAILED Scenarios:")
        [logging.info(scenario.name) for scenario in scenarios if scenario.status.name == "failed"]
    logging.info("SLAYER EXECUTION FINISHED")


def before_tag(context, tag):
    pass


def after_tag(context, tag):
    pass


def before_feature(context, feature):
    logging.info("%s" % ("-" * LINE_LENGTH))
    logging.info("Feature: '{}'".format(feature.name).center(LINE_LENGTH, " "))


def after_feature(context, feature):
    pass


def before_scenario(context, scenario):
    logging.info("SCENARIO: '{}'".format(scenario.name.upper()))


def after_scenario(context, scenario):
    logging.info("'{0}' RESULT: '{1}'".format(scenario.name.upper(), scenario.status.name.upper()))
    logging.info("%s" % ("-" * LINE_LENGTH))


def before_step(context, step):
    logging.info("STEP: '{}'".format(step.name))


def after_step(context, step):
    pass
