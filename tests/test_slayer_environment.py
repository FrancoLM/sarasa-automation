import pytest
import os
import sys

from ..slayer.slayer_class import Slayer


@pytest.fixture
def slayer():
    slayer = Slayer()
    return slayer


def test_can_create_environment_variables(slayer):
    variable_name_1 = "test_variable1"
    variable_value_1 = "test_variable_value1"
    variable_name_2 = "test_variable2"
    variable_value_2 = "test_variable_value2"
    slayer.set_new_environment_variable(variable_name_1, variable_value_1, print_to_console=False)
    slayer.set_new_environment_variable(variable_name_2, variable_value_2, print_to_console=True)
    assert os.environ.get(variable_name_1) == variable_value_1
    assert slayer.variables[variable_name_1] == variable_value_1
    assert os.environ.get(variable_name_2) == variable_value_2
    assert slayer.variables[variable_name_2] == variable_value_2


def test_cannot_create_environment_variable_if_name_not_string(slayer):
    variable_name = 500.0
    variable_value = "test_variable_value"
    with pytest.raises(TypeError):
        slayer.set_new_environment_variable(variable_name, variable_value, print_to_console=False)

def test_cannot_create_environment_variable_if_value_not_string(slayer):
    variable_name = "test_variable"
    variable_value = 300
    with pytest.raises(TypeError):
        slayer.set_new_environment_variable(variable_name, variable_value, print_to_console=False)


def test_can_use_custom_config_file(slayer):
    pass


def test_can_use_custom_logger_file(slayer):
    pass


def test_can_use_custom_behave_file(slayer):
    pass


def can_use_custom_environment_py_file(slayer):
    pass
