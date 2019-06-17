# -*- coding: utf-8 -*-
import socket
from core_code.logger import Logging
import threading

COMMUNICATION_PORT = 2500
LENGTH_SEPARATION_CHAR = '$'


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
        self.client_socket.setblocking(0)
        self.lock = threading.Lock()

    def send_to_all(self, message):
        """
        the function sends the message
        to all known nodes
        :param message: the message to send
        """
        self.logger.info('Acquiring lock')
        self.logger.info(
            'Sending message to the known nodes- ' + message)
        for node_address in self.known_nodes:
            self.send(message, node_address)
        self.logger.info('Releasing lock')

    def send(self, message, node_address):
        """
        the functions sends the specific
        node the message according to the length
        protocol
        :param message: the message to send
        :param node_address: the address of the node
        to send
        """
        self.lock.acquire()
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
                ' is not connected')
            if node_address in self.known_nodes:
                self.known_nodes.remove(node_address)
        finally:
            self.client_socket.close()
            self.client_socket = \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.lock.release()

    def check_connections(self):
        """
        the function checks that the
        known nodes are still connected.
        if not it removes them from the
        list
        """
        self.lock.acquire()
        addresses = []
        for address in self.known_nodes:
            addresses.append(address)
        for address in addresses:
            try:
                self.client_socket.connect((address,
                                            COMMUNICATION_PORT))
                self.logger.info(
                    'Check connection to- ' +
                    address)
            except socket.error:
                self.logger.info(
                    'Node address- ' + address +
                    ' disconnected')
                self.known_nodes.remove(address)
            finally:
                self.client_socket.close()
                self.client_socket = \
                    socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.lock.release()
