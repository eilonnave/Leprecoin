# -*- coding: utf-8 -*-
import socket
from core_code.logger import Logging
import threading

COMMUNICATION_PORT = 2500
LENGTH_SEPARATION_CHAR = '$'

# ToDo: implement check connection
# ToDo: implement lock


class NodeClient:
    """
    the client part of the
    node. the client is used for
    sending messages to all of the
    known nodes and to a specific
    one
    """
    def __init__(self, logger, known_nodes):
        """
        constructor
        """
        self.logger = logger
        self.known_nodes = known_nodes
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()

    def send_to_all(self, message):
        """
        the function sends the message
        to all known nodes
        :param message: the message to send
        """
        self.logger.info('Acquiring lock')
        self.lock.acquire()
        self.logger.info(
            'Sending message to the known nodes- ' + message)
        for node_address in self.known_nodes:
            self.send(message, node_address)
        self.logger.info('Releasing lock')
        self.lock.release()

    def send(self, message, node_address):
        """
        the functions sends the specific
        node the message according to the length
        protocol
        :param message: the message to send
        :param node_address: the address of the node
        to send
        """
        try:
            self.client_socket.connect((node_address,
                                        COMMUNICATION_PORT))
            self.logger.info(
                'Sending message- ' +
                message +
                ' to- '+node_address)
            message = \
                str(len(message)) \
                + LENGTH_SEPARATION_CHAR \
                + message
            self.client_socket.send(message)
        except socket.error:
            self.logger.info(
                'Node address- ' +
                node_address +
                ' disconnected')
        finally:
            self.client_socket.close()
            self.client_socket = \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def check_connections(self):
        """
        the function checks that the
        known nodes are still connected.
        if not it removes them from the
        list
        """
        self.lock.acquire()
        pass
