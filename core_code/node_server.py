# -*- coding: utf-8 -*-
import select
import socket
from core_code.logger import Logging

SERVER_IP = '0.0.0.0'
COMMUNICATION_PORT = 2500
LISTEN_SIZE = 5
READ_SIZE = 1024
LENGTH_SEPARATION_CHAR = '$'


class NodeServer:
    """
    the server part of a node.
    the server is used for
    messages from all the nodes that
    send one
    """
    def __init__(self, logger):
        """
        constructor
        """
        # create the socket
        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)
        self.logger = logger
        # the received messages
        # the node will handle them in another class
        self.received = []
        self.to_close = False
        try:
            # binding and listening
            self.is_closed = False
            self.server_socket.bind((SERVER_IP, COMMUNICATION_PORT))
            logger.info('Listening on port ' + str(COMMUNICATION_PORT))
            self.server_socket.listen(LISTEN_SIZE)
            # initialize the lists for
            # the usage of the server
            self.open_clients_sockets = []
            self.readable = []
            self.exceptional = []
        except socket.error as err:
            self.logger.error('Could not open node- ' + str(err))
            self.server_socket.close()
            self.is_closed = True

    def run(self):
        """
        the function runs the server
        """
        while not self.to_close:
            self.readable, [], self.exceptional = select.select(
                [self.server_socket] +
                self.open_clients_sockets,
                [],
                self.open_clients_sockets)
            self.handle_exception_sockets()
            self.handle_read_sockets()

    def handle_exception_sockets(self):
        """
        the function closes the connection with
        the sockets with the exceptions
        """
        for current_socket in self.exceptional:
            self.logger.info('handling exception socket')
            self.disconnect_connection(current_socket)
            if current_socket in self.readable:
                self.readable.remove(current_socket)

    def handle_read_sockets(self):
        """
        the function handles the sockets
        which are ready to read
        """
        for current_socket in self.readable:
            if current_socket is self.server_socket:
                client_socket, client_address = current_socket.accept()
                self.logger.info('received new connection from ' +
                                 str(client_address[0]) +
                                 ':' +
                                 str(client_address[1]))
                self.open_clients_sockets.append(client_socket)
            else:
                try:
                    length = self.extract_pack_length(current_socket)
                    if length != 0:
                        self.received.append(
                            self.receive_message(length, current_socket))
                    self.disconnect_connection(current_socket)

                except socket.error as err:
                    self.logger.error('received socket error ' + str(err))
                    self.disconnect_connection(current_socket)

    @staticmethod
    def extract_pack_length(client_socket):
        """
        the function receives the length of the
        message package from the client
        :param client_socket: the socket which the
        message is coming from
        :returns: the extracted length of the package
        """
        length = client_socket.recv(1)
        if length == '':
            return 0
        while length[-1] != LENGTH_SEPARATION_CHAR:
            length += client_socket.recv(1)
        return int(length[:-1])

    @staticmethod
    def receive_message(length, client_socket):
        """
        the function receives the packed message
        from the client
        :param length: the length of the
        packed message
        :param client_socket: the socket which
        the message coming from
        :return: the packed message
        """
        return client_socket.recv(length)

    def disconnect_connection(self, client_socket):
        """
        the function disconnect properly connection
        with the client
        :param client_socket: the socket of the client
        """
        client_socket.close()
        self.open_clients_sockets.remove(client_socket)
