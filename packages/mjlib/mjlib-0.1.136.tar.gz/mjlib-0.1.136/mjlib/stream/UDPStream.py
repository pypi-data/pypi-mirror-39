import select
from abc import ABC

import socket

from mjlib.stream import Stream


class UDPStream(Stream, ABC):
    def __init__(self, address="127.0.0.1", port=12345):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((address, port))

    def _get_sample(self):
        ready = select.select([self.sock], [], [], 1)
        if ready[0]:
            data, addr = self.sock.recvfrom(20000)
            try:
                modified_sentance = data.strip().decode('utf-8')  # 'ISO-8859-1'
                return modified_sentance
            except UnicodeDecodeError:
                print('got UnicodeDecodeError, skipping data')
