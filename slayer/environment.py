"""Environment file for behave
Selenium grid may be set here too"""
import logging

LINE_LENGTH = 42
PASSED = "passed"
FAILED = "failed"

def before_all(context):
    # Setup logging for SLAYER, according to behave API reference:
    # http://python-behave.readthedocs.io/en/latest/api.html#logging-setup
    # configure_logging()
    pass


def after_all(context):
    logging.info("%s" % ("-" * LINE_LENGTH))
    scenarios = []
    for feature in context._runner.features:
        scenarios += feature.scenarios
    # Scenario.duration is the execution time
    # step.duration is the execution time for each step
    logging.info("PASSED Scenarios:")
    [logging.info("\t" + scenario.name) for scenario in scenarios if scenario.status.name == PASSED]
    logging.info("FAILED Scenarios:")
    [logging.info("\t" + scenario.name) for scenario in scenarios if scenario.status.name == FAILED]
    logging.info("")
    logging.info("SLAYER EXECUTION FINISHED")


def before_tag(context, tag):
    pass


def after_tag(context, tag):
    pass


def before_feature(context, feature):
    logging.info("%s" % ("-" * LINE_LENGTH))
    logging.info("Feature '{}' Start".format(feature.name.upper()))
    logging.info("%s" % ("-" * LINE_LENGTH))


def after_feature(context, feature):
    logging.info("Feature '{}' End".format(feature.name.upper()))
    logging.info("%s" % ("-" * LINE_LENGTH))


def before_scenario(context, scenario):
    logging.info("Scenario '{}' Start".format(scenario.name.upper()))


def after_scenario(context, scenario):
    logging.info("Scenario '{0}' End. Result: '{1}'".format(scenario.name.upper(), scenario.status.name.upper()))
    logging.info("%s" % ("-" * LINE_LENGTH))


def before_step(context, step):
    logging.info("Step: '{}'   {}".format(step.name, "# {}:{}".format(step.location.filename, step.location.line)))


def after_step(context, step):
    if step.status.name == FAILED:
        logging.info("Step: '{}': {}".format(step.name, step.status.name.upper()))
