from os import environ
from configobj import ConfigObj
import os.path

env_config_file = None
ssh_config_file = None
global is_cluster
is_cluster = False

global is_epocluster
is_epocluster = False


bastion_settings = 'SSH_connection'


def get_config():
    global env_config_file
    if not env_config_file:
        file_path = os.path.join("config/pods", "systems_" + environ.get("ENVIRONMENT") + ".cfg")
        env_config_file = ConfigObj(file_path)
    return env_config_file


def get_ssh_config():
    global ssh_config_file
    if not ssh_config_file:
        file_path = os.path.join("config/env_connection", "ssh_tunneling.cfg")
        ssh_config_file = ConfigObj(file_path)
    return ssh_config_file


def get_env_version(section='environment_version'):
    cfg = get_config()
    if not cfg[section]['env_version']:
        cfg[section]['env_version'] = "1"
        cfg[section]['keystorepassword'] = "snowcap"
    return cfg[section]['env_version'], cfg[section]['keystorepassword']


def get_epo_server(hostname='epo_server_1'):
    cfg = get_config()
    if environ.get("EPO_IP"):
        cfg[hostname]['ip'] = environ.get("EPO_IP")
    return cfg[hostname]['ip'], cfg[hostname]['port'], cfg[hostname]['user'], cfg[hostname]['password']

def get_consumer_service(hostname='consumer_service_1'):
    cfg = get_config()
    return cfg[hostname]['ip'], cfg[hostname]['port']

def get_dxl_broker_dns(hostname='DXL_Broker'):
    cfg = get_config()
    if environ.get("DXL_BROKER"):
        cfg[hostname]['dns'] = environ.get("DXL_BROKER")
    return cfg[hostname]['dns'], cfg[hostname]['ip'], cfg[hostname]['port']


def get_ahserver(hostname='ahserver_1'):
    cfg = get_config()
    if environ.get("EPO_IP"):
        cfg[hostname]['ip'] = environ.get("EPO_IP")
    return cfg[hostname]['ahserver'], cfg[hostname]['ahport'], True if cfg[hostname]['ahsecure'].lower() == 'true' else False


def get_tenant_info(tenant_name):
    cfg = get_config()
    return cfg[tenant_name]['tenant_guid'], cfg[tenant_name]['id'], cfg[tenant_name]['user'], cfg[tenant_name]['password']

def get_dxl_broker(hostname=None):
    cfg = get_config()
    return {
        "name": hostname,
        "hostname": cfg[hostname]['hostname'],
        "ip": cfg[hostname]['ip'],
        "port": cfg[hostname]['port'],
        "domain": cfg[hostname]['domain'],
        "user": cfg[hostname]['user'],
        "password": cfg[hostname]['password']
    }


def get_hbase_server(hostname="hbase_server_1"):
    cfg = get_config()
    return cfg[hostname]['ip'], cfg[hostname]['port'], cfg[hostname]['table_name']


def get_databus_server(hostname="databus_server_1"):
    cfg = get_config()
    if environ.get("DATABUS_IP"):
        cfg[hostname]['ip'] = environ.get("DATABUS_IP")
    return cfg[hostname]['ip'], cfg[hostname]['port']

def get_ssh_databus_server(hostname="databus_server_2"):
    cfg = get_config()
    if environ.get("DATABUS_IP_SSH"):
        cfg[hostname]['ip'] = environ.get("DATABUS_IP")
    return cfg[hostname]['ip'], cfg[hostname]['port'], cfg[hostname]['ssh_user']


def get_databridge_server(hostname="databridge_server_1"):
    cfg = get_config()
    if environ.get("DATABRIDGE_IP"):
        cfg[hostname]['ip'] = environ.get("DATABRIDGE_IP")
    return cfg[hostname]['ip'], cfg[hostname]['port']


def get_epo_sql_settings(hostname="epo_sql_server_settings_1"):
    cfg = get_config()
    if environ.get("EPO_IP"):
        cfg[hostname]['ip'] = environ.get("EPO_IP")
    return cfg[hostname]['ip'], cfg[hostname]['user_domain'], cfg[hostname]['user_name'], cfg[hostname]['password'], cfg[hostname]['port'], cfg[hostname]['database_name']

def get_powershell_epo_cluster_settings(hostname="powershell_epo_cluster"):
    cfg = get_config()
    return cfg[hostname]['user'], cfg[hostname]['password']


def get_storm_server():
    cfg = get_config()
    return cfg['storm_ui']['ip'], cfg['storm_ui']['port']

def get_etcd_server(hostname="etcd"):
    cfg = get_ssh_config()
    return "localhost", cfg['instances'][hostname]['ip'], cfg['instances'][hostname]['local_port']

def get_ssh_credentials():
    global ssh_config_file
    if not ssh_config_file:
        file_path = os.path.join("config/env_connection", "ssh_tunneling.cfg")
        ssh_config_file = ConfigObj(file_path)
    ssh_cert_route = os.path.join(os.getcwd(), ssh_config_file['credentials'][bastion_settings]['ssh_private_key'])
    ssh_user = ssh_config_file['credentials'][bastion_settings]['ssh_user']
    ssh_password = ssh_config_file['credentials'][bastion_settings]['ssh_password']
    return ssh_user, ssh_password, ssh_cert_route


def get_rlogin_service(hostname='rlogin_service'):
    cfg = get_config()
    return cfg[hostname]['ip'], cfg[hostname]['port']