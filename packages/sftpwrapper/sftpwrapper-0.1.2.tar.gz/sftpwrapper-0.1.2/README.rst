sftpwrapper
===========

Overview
--------
A python program that facilitates uploading and downloading of files to/from an SFTP server

Install It
----------
From PyPI ::

    $ pip install sftpwrapper



Code Example
------------
    from sftpwrapper import SftpWrapper

    remote_connection = SftpWrapper(host, port)
    remote_connection.host_connect(user, password)
    upload_good = remote_connection.upload_stuffs(csv_name, remote + csv_name)
    remote_connection.host_disconnect()

Dependencies
------------
* paramiko

License
--------
MIT