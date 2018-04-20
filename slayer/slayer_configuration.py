import os

from configobj import ConfigObj

SLAYER_CONFIG = None
#BEHAVE_CONFIG = None

def new_env_variable(name, value, print_to_console=True):
    os.environ[name] = value
    if print_to_console:
        print("{var_name}: {var_value}".format(var_name=name, var_value=value))


def get_config():
    global SLAYER_CONFIG
    if SLAYER_CONFIG is None:
        config_path = os.getenv("CONFIG")
        SLAYER_CONFIG = ConfigObj(config_path)
    return SLAYER_CONFIG


def set_env_variables():
    cfg = get_config()
    slayer_cfg = cfg["slayer"]

    # Output folders
    new_env_variable("OUTPUT_DIR", os.path.abspath(slayer_cfg["output"]["path"]))
    new_env_variable("LOGS_DIR", os.path.join(os.getenv("OUTPUT_DIR"), slayer_cfg["logs"]["path"]))

    # Proxy
    new_env_variable("HTTP_PROXY", slayer_cfg["proxy"]["http_proxy"])
    new_env_variable("HTTPS_PROXY", slayer_cfg["proxy"]["https_proxy"])
    new_env_variable("NO_PROXY", slayer_cfg["proxy"]["no_proxy"])

#def get_behave_args():
#    global BEHAVE_CONFIG
#    behave_cfg = get_config()
#    if BEHAVE_CONFIG is None:
#        BEHAVE_CONFIG = behave_cfg["behave"]
#    return BEHAVE_CONFIG

