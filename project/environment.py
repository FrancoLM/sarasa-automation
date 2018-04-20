# before / after functions here
# Fixtures here

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry

def before_feature(context, feature):
    for scenario in feature.scenarios:
        if "AUTORETRY" in scenario.effective_tags:
            patch_scenario_with_autoretry(scenario, max_attempts=3)