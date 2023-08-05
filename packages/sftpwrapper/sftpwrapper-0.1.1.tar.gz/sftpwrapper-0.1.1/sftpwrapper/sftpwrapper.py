import paramiko


class SftpWrapper:
    def __init__(self, host, port, logging=False):
        """
        :param host: Host IP address
        :param port: Host port for SFTP communication
        :param logging: Pass True parameter here to enable logging
        """
        self.host = host
        self.port = port
        self.sftp = None
        self.transport = None
        if logging:
            paramiko.util.log_to_file('./tmp/paramiko.log')

    def host_connect(self, username, password):
        self.transport = paramiko.Transport((self.host, self.port))
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def upload_stuffs(self, local_path, remote_path):
        """
        Upload file to remote machine.
        :param local_path: This is the path for the file on your LOCAL machine, where python is called from
        :param remote_path: This is the path for the file on your REMOTE machine, will default to PWD
        :return: Returns paramiko.sftp_attr.SFTPAttributes object
        """
        try:
            return self.sftp.put(local_path, remote_path)
        except:
            return None

    def download_stuffs(self, local_path, remote_path):
        """
        Download file from remote machine.
        :param local_path: This is the path for the file on your LOCAL machine, where python is called from
        :param remote_path: This is the path for the file on your REMOTE machine, will default to PWD
        :return:
        """
        self.sftp.get(remote_path, local_path)

    def list_stuffs(self, remote_path='.'):
        """
        List contents of the remote path.
        :param remote_path: This is the path for the file on your REMOTE machine, will default to PWD
        :return: list containing the names of entries in a given path
        """
        return self.sftp.listdir(remote_path)

    def change_directory(self, path=None):
        """
        Navigate to a different path on the remote machine.
        :param path: This is the path on your REMOTE machine, will default to None
        """
        self.sftp.chdir(path=path)

    def host_disconnect(self):
        self.transport.close()
        self.sftp.close()
