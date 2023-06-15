import re
import socket
import time

import paramiko

import os
import sys
from typing import Tuple
from ClientException import InitException, NoConnectionException


URL = Tuple[str, int]

end_str=('# ', '$ ', '? ', '% ')
class Ssh2Client:
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
            self.__ssh = None
            self.__channel = None
            # 7-bit C1 ANSI sequences
            self.__ansi_escape = re.compile(r'''
                            \x1B  # ESC
                            (?:   # 7-bit C1 Fe (except CSI)
                            [@-Z\\-_]
                            |     # or [ for CSI, followed by a control sequence
                            \[
                            [0-?]*  # Parameter bytes
                            [ -/]*  # Intermediate bytes
                            [@-~]   # Final byte
                        )
                    ''', re.VERBOSE)
            self.color_pattern = r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))'

    def __del__(self):
        self.__close()

    def clear_irc_color(self, string):
        pattern = r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))'
        return re.sub(pattern, '', string)

    def connect(self, user: str, pwd: str) -> bool:
        self.__close()
        self.transport.connect(username=user, password=pwd)
        self.__ssh = paramiko.SSHClient()
        self.__ssh._transport = self.transport
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # self.__ssh.connect(self.__host, username=user, password=pwd, port=self.__port)
        if not self.__channel:
            self.__channel = self.__ssh.invoke_shell(term='xterm', width=4096, height=96)
            # time.sleep(0.020)
        return True

    def exec(self, cmd: str, timeout=30):
        if cmd.endswith('\n'):
            self.__channel.send(cmd)
        else:
            self.__channel.send(cmd + '\n')
        if cmd.strip().lower() == 'exit':
            return
        result = self.recv(timeout)
        begin_pos = result.find('\r\n')
        return result[begin_pos + 2:]

    def recv(self, timeout) -> str:
        result = ''
        out_str = ''
        max_wait_time = timeout * 1000
        self.__channel.settimeout(0.05)
        while max_wait_time > 0:
            try:
                out = self.__channel.recv(1024 * 1024).decode()
                if not out or out == '':
                    continue
                out_str = out_str + out

                match, result = self.__match(out_str)
                if match is True:
                    return result
                else:
                    max_wait_time -= 50
            except socket.timeout:
                max_wait_time -= 50

        raise Exception('recv data timeout')

    def __match(self, out_str: str) -> (bool, str):
        result = out_str
        # result = re.sub(self.color_pattern, '', result)
        # result = (re.compile(r'\x1b[^m]*m')).sub('', result)
        # result = self.__ansi_escape.sub('', result)
        for it in end_str:
            if result.find(it) != -1:
                return True, result
        return False, result

    def __close(self):
        if not self.__ssh:
            return
        self.__ssh.close()
        self.__ssh = None
