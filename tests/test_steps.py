import pytest
import os
from ..slayer.slayer_configuration import Slayer


# test -> can read custom config file and logger, and behave.ini
# test -> can set environment variable
# test -> proxy


@pytest.fixture
def slayer():
    slayer = Slayer()
    return slayer


def test_set_new_environment_variable(slayer):
    variable_name = "test_variable"
    variable_value = "test_variable_value"
    slayer.set_new_environment_variable(variable_name, variable_value, print_to_console=False)
    assert os.environ.get(variable_name) == variable_value


def test_set_new_environment_variable_invalid_name(slayer):
    variable_name = 500
    variable_value = "test_variable_value"
    with pytest.raises(TypeError):
        slayer.set_new_environment_variable(variable_name, variable_value, print_to_console=False)


def test_set_new_environment_variable_invalid_value(slayer):
    variable_name = "test_variable"
    variable_value = 300
    with pytest.raises(TypeError):
        slayer.set_new_environment_variable(variable_name, variable_value, print_to_console=False)
