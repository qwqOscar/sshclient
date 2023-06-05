import paramiko
from paramiko import sftp


class NoConnectionException(Exception):
    def __init__(self, error: str):
        super().__init__(self)
        self.error = error

    def __str__(self):
        return repr(self.error)


class SftpClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sftp = None
        self.transport = paramiko.Transport((host, port))

    def warning(func):
        def wrapper(self, *args, **kwargs):
            try:
                if not self.transport.is_active():
                    raise NoConnectionException('SFTP client has no connection.')
            except NoConnectionException as e:
                print(e)
            else:
                func(self, *args, **kwargs)
        return wrapper

    def connect(self, user: str, pwd: str):
        if not self.sftp:
            self.transport.connect(username=user, password=pwd)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def list_files(self, path: str):
        ...

    @warning
    def upload(self, lp: str, rp: str):
        self.sftp.put(lp, rp)

    @warning
    def download(self, lp: str, rp: str):
        self.sftp.get(rp, lp)

    def close(self):
        self.transport.close()
        self.sftp = None



