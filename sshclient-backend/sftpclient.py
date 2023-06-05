import paramiko
from typing import Tuple
from ClientException import InitException, NoConnectionException


URL = Tuple[str, int]


class SftpClient:
    def __init__(self, url: URL = None, transport: paramiko.Transport = None):
        try:
            if url is None and transport is None:
                raise InitException('SftpClient: missing parameters')
            if url is not None and transport is not None:
                raise InitException('SftpClient: parameters conflicts')
        except InitException as e:
            print(e)
        else:
            # url 比 transport 具有更高的优先级
            if url is not None:
                self.transport = paramiko.Transport((url[0], url[1]))
            else:
                self.transport = transport
            self.sftp = None

    def __del__(self):
        self.close()

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



