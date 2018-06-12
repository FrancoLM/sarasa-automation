import paramiko
import logging
import os
from features.steps.utils.remote_connection.remote_connection_base import RemoteConnection

# Monkeypatch Fix for Paramiko bug
# Refer to
#     http://stackoverflow.com/questions/30801725/paramiko-nameerror-global-name-descriptor-is-not-defined
# for more information
try:
    from paramiko._winapi import SECURITY_DESCRIPTOR
    import ctypes.wintypes


    def descriptor_fix(self, value):
        self._descriptor = value
        self.lpSecurityDescriptor = ctypes.addressof(value)
except ValueError:
    import ctypes

SECURITY_DESCRIPTOR.descriptor = descriptor_fix


class SSHClient(RemoteConnection):

    def __init__(self, ip, port, ssh_user, login_param, is_password_auth=True, default_target_os='posix'):
        self.ip = ip
        self.port = int(port)
        self.ssh_user = ssh_user
        self.login_param = login_param
        self.is_password_auth = is_password_auth
        self.__login()
        self.default_target_os = default_target_os  # posix for Unix. nt for Windows

    def __login(self):
        self.session = paramiko.SSHClient()
        try:
            self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self.is_password_auth:
                self.session.connect(self.ip, port=self.port, username=self.ssh_user, password=self.login_param)
            else:  # Use key
                # pk = paramiko.RSAKey(filename=self.login_param)
                self.session.connect(self.ip, port=self.port, username=self.ssh_user, key_filename=self.login_param)

            logging.info("Logged to %s via SSH as user %s" % (self.ip, self.ssh_user))
        except Exception as e:
            logging.info("Could not connect to %s: %s" % (self.ip, e))
            raise

    def copy_file(self, local_file_path, remote_dest_path="."):
        sftp = self.session.open_sftp()
        path, filename = os.path.split(local_file_path)
        try:
            sftp.put(local_file_path, remote_dest_path + "/" + filename)
        except Exception as e:
            logging.info("Could not copy %s: %s" % (local_file_path, e))
        finally:
            sftp.close()

    def retrieve_file(self, remote_file_path, local_dest_path, local_file_name):
        sftp = self.session.open_sftp()
        try:
            sftp.get(remote_file_path, local_dest_path + os.sep + local_file_name)
        except Exception as e:
            logging.info("Could not Retrieve %s: %s" % (remote_file_path, e))
        finally:
            sftp.close()

    def copy_dir_recursive(self, local_folder_path, dest_path="."):
        # TODO: method is work in progress. Hasn't been tested
        sftp = self.session.open_sftp()
        os.chdir(os.path.split(local_folder_path)[0])
        parent = os.path.split(local_folder_path)[1]
        for walker in os.walk(parent):
            try:
                sftp.mkdir(os.path.join(dest_path, walker[0]))
            except:
                pass
            for file in walker[2]:
                sftp.put(os.path.join(walker[0], file), os.path.join(dest_path, walker[0], file))

    def send_command(self, command):
        try:
            stdin, stdout, stderr = self.session.exec_command(command)
        except:
            self.__login()
            stdin, stdout, stderr = self.session.exec_command(command)
        return stdin, stdout, stderr

    def send_command_background(self, command):
        prefix = "nohup "
        background = " > /dev/null 2>&1 &"
        bg_command = prefix + command + background
        stdin, stdout, stderr = self.session.exec_command(bg_command + " &")
        return stdin, stdout, stderr

    def close_session(self):
        self.session.close()

    def get_process_pid(self, process):
        cmd = """ps aux | grep "%s" | grep -v grep | awk '{print $2}'""" % process
        _, stdout, _ = self.session.exec_command(cmd)
        output = stdout.read()
        process_list = output.rstrip().strip("\n")
        if type(process_list) is not str:
            # More than one process match
            raise Exception("Error. Could not obtain a matching process PID. %s" % (
                "No process found." if len(process_list) == 0 else
                "More than one process found."))
        else:
            return output

    def terminate_process(self, process_id, terminate_method='-9'):
        return self.send_command('kill %s %s' % (terminate_method, str(process_id)))

    def is_file(self, file, path):
        cmd_file_exists = '[ -f {0} ] && echo "{1} Exists" || echo "{1} Not Found"'.format(path + '/' + file, file)
        file_exists = False
        try:
            _, stdout, _ = self.send_command(cmd_file_exists)
        except:
            self.__login()
            _, stdout, _ = self.send_command(cmd_file_exists)
        output = stdout.read()
        if "Exists" in output:
            file_exists = True
        return file_exists
