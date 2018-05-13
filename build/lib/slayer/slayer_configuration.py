import os
from configobj import ConfigObj

SLAYER_CONFIG = None


def new_env_variable(name, value, print_to_console=True):
    os.environ[name] = value
    if print_to_console:
        print("{var_name:>15} ==> {var_value}".format(var_name=name, var_value=value))


def get_config():
    global SLAYER_CONFIG
    if SLAYER_CONFIG is None:
        config_path = os.getenv("SLAYER_CONFIG")
        SLAYER_CONFIG = ConfigObj(config_path)
    return SLAYER_CONFIG


def set_env_variables():
    cfg = get_config()
    slayer_cfg = cfg["slayer"]

    # Output folders
    new_env_variable("OUTPUT_DIR", os.path.join(os.getenv("SLAYER_ROOT"), slayer_cfg["output"]["path"]))
    new_env_variable("LOGS_DIR", os.path.join(os.getenv("OUTPUT_DIR"), slayer_cfg["logs"]["path"]))

    # Proxy
    new_env_variable("HTTP_PROXY", slayer_cfg["proxy"]["http_proxy"])
    new_env_variable("HTTPS_PROXY", slayer_cfg["proxy"]["https_proxy"])
    new_env_variable("NO_PROXY", slayer_cfg["proxy"]["no_proxy"])


