# -*- coding: utf-8 -*-
import socket
import time
from core_code.logger import Logging

COMMUNICATION_PORT = 2500
LENGTH_SEPARATION_CHAR = '$'


class NodeClient:
    """
    the client part of the
    node. the client is used for
    sending messages to all of the
    known nodes
    """
    def __init__(self, logger, known_nodes):
        """
        constructor
        """
        self.logger = logger
        self.known_nodes = known_nodes
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, message):
        """
        the function sends the message
        to all known nodes
        """
        for node_address in self.known_nodes:
            try:
                self.client_socket.connect((node_address, COMMUNICATION_PORT))
                self.logger.info(
                    'sending message to the known nodes- '+message)
                message = \
                    str(len(message)) \
                    + LENGTH_SEPARATION_CHAR \
                    + message
            except socket.error:
                self.known_nodes.remove(node_address)
            finally:
                self.client_socket.close()
                self.client_socket = \
                    socket.socket(socket.AF_INET, socket.SOCK_STREAM)


n = NodeClient(Logging('123').logger, ['127.0.0.1'])
while True:
    n.send('1234')
    print 'sent'
