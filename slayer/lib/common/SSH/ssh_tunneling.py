# SSH Tunnel creator for yarara IoT tests
# Version 0.0.1 (Ezequiel Audisio)
#
# Usage:
#      ssh_tunneling.py <config_file>
#
#                       config_file: a .cfg file located in /project/config/pods/ used by yarara tests
#

import logging
import os
import threading
import time
import sshtunnel
from features.steps.utils import pods_management

_is_main_thread_active = lambda: any((i.name == "MainThread") and i.is_alive() for i in threading.enumerate())


def set_connection_method():
    conn_method = {
        "1": _set_connection_for_v1,
        "2": _set_connection_for_v2
    }

    env_version = pods_management.get_env_version()[0]

    # Call the connection method for the environment
    conn_method[env_version]()


def _set_connection_for_v1():
    # No configuration required
    pass


def _set_connection_for_v2():
    if os.environ['ENABLE_TUNNEL'] == "True":
        setup_ssh_tunnels()


def setup_ssh_tunnels():
    remote_hosts = []
    remote_ports = []
    local_ports = []
    instance_names = []

    # Get all instances that need a tunnel
    env_config = pods_management.get_config()
    ssh_config = pods_management.get_ssh_config()

    instances_list = ssh_config['instances']

    for instance_key in instances_list:  # each instance in the ssh file
        # Add Instance Names
        add_element(instance_names, instances_list[instance_key]['instance_name'])
        # Add Remote Instance IP
        add_element(remote_hosts, instances_list[instance_key]['ip'])
        # Add Remote port the tunnel will be mapped to
        add_element(remote_ports, instances_list[instance_key]['private_port'])
        # Add Local port the tunnel will be mapped with
        add_element(local_ports, instances_list[instance_key]['local_port'])

    # Get SSH Tunnel information
    ssh_host = env_config['Bastion']['ip']
    ssh_port = int(env_config['Bastion']['port'])

    ssh_user, ssh_password, ssh_pkey = pods_management.get_ssh_credentials()

    if not os.path.exists(os.path.join(os.environ['OUTPUT'], 'ssh_tunnels')):
        os.makedirs(os.path.join(os.environ['OUTPUT'], 'ssh_tunnels'))

    for host, port, lport, instance_name in zip(remote_hosts, remote_ports, local_ports, instance_names):
        logging.info("An SSH Tunnel for " + instance_name + " will be created with local port " + str(lport))
        logging.info("Updating " + instance_name + " instance 'host:port' to 127.0.0.1:" + str(lport))

        tunnel_logger = logging.getLogger('paramiko.transport')
        tunnel_logger.propagate = False  # it will not log to console
        tunnel_logger.setLevel(logging.DEBUG)
        tunnel_file_logger = logging.FileHandler(os.path.join(os.environ['OUTPUT'], 'ssh_tunnels', 'ssh_tunnels_%s.log' % instance_name))
        tunnel_file_logger.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s| %(message)s'))
        tunnel_logger.addHandler(tunnel_file_logger)
        tunnel_logger = sshtunnel.create_logger(tunnel_logger)
        th = threading.Thread(target=_create_tunnel, args=(host, int(port), int(lport),
                                                           ssh_host, int(ssh_port), ssh_user, ssh_password, ssh_pkey,
                                                           tunnel_logger))
        th.start()
        time.sleep(0.2)
    time.sleep(10)


def add_element(data_list, element):
    if isinstance(element, list):
        data_list.extend(element)
    else: # Expected another type. Append to the list
        data_list.append(element)


def _create_tunnel(rem_host, rem_port, loc_port, ssh_host, ssh_port, ssh_user, ssh_password, ssh_pkey, tunnel_logger):
    try:
        with sshtunnel.open_tunnel(
            ssh_address=(ssh_host, ssh_port),
            ssh_host_key=None,
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            ssh_private_key=ssh_pkey,
            remote_bind_address=(rem_host, rem_port),
            local_bind_address=('127.0.0.1', loc_port),
            logger=tunnel_logger
        ) as server:
            logging.info("Local port opened: " + str(server.local_bind_port))
            while _is_main_thread_active():
                time.sleep(0.5)  # delays for 0.5 seconds, to keep thread alive
            else:
                server.stop()
    except Exception as e:
        logging.info("-----WARNING: Tunnel for %s could not be created-----" % ssh_host)
