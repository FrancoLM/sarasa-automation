class RemoteConnection():

    def __init__(self):
        raise NotImplementedError()

    def __login(self, is_password_auth):
        raise NotImplementedError()

    def copy_file(self, local_file_path, remote_dest_path="."):
        raise NotImplementedError()

    def retrieve_file(self, remote_file_path, local_dest_path, local_file_name):
        raise NotImplementedError()

    def send_command(self, command):
        raise NotImplementedError()

    def close_session(self):
        raise NotImplementedError()
