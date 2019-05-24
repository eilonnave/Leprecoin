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
    the server is used for replying
    and receiving messages
    """
    def __init__(self, logger):
        """
        constructor
        """
        # create the socket
        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)
        self.logger = logger
        # the requests from the server
        # the node will handle them in another class
        self.requests = []
        try:
            # binding and listening
            self.is_closed = False
            self.server_socket.bind((SERVER_IP, COMMUNICATION_PORT))
            logger.info('Listening on port ' + str(COMMUNICATION_PORT))
            self.server_socket.listen(LISTEN_SIZE)
            # initialize the lists for
            # the usage of the server
            self.messages_to_send = []
            self.open_clients_sockets = []
            self.send_sockets = []
            self.readable = []
            self.writable = []
            self.exceptional = []
        except socket.error as err:
            self.logger.error('Could not open node- ' + str(err))
            self.server_socket.close()
            self.is_closed = True

    def run(self):
        """
        the function runs the server
        """
        while True:
            self.readable, self.writable, self.exceptional = select.select(
                [self.server_socket] +
                self.open_clients_sockets,
                self.send_sockets,
                self.open_clients_sockets)
            self.handle_exception_sockets()
            self.handle_read_sockets()
            self.handle_write_sockets()

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
            if current_socket in self.writable:
                self.writable.remove(current_socket)

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
                    if length == 0:
                        self.disconnect_connection(current_socket)
                    else:
                        self.requests.append(
                            (self.receive_message(length, current_socket),
                             current_socket))
                except socket.error as err:
                    self.logger.error('received socket error ' + str(err))
                    self.disconnect_connection(current_socket)

    def handle_write_sockets(self):
        """
        the function handles the socket which are ready
        to write to
        """
        for current_socket in self.writable:
            for message in self.messages_to_send:
                if current_socket is message[0]:
                    current_socket.send(message[1])
                    self.messages_to_send.pop(self.messages_to_send.index(message))
                    self.send_sockets.pop(
                        self.send_sockets.index(message[0]))

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
        for message in self.messages_to_send:
            if message[0] is client_socket:
                self.messages_to_send.remove(message)
        for current_socket in self.send_sockets:
            if current_socket is client_socket:
                self.send_sockets.remove(client_socket)

    def add_message_to_send(self, client_socket, message):
        """
        the function adds the message and the client_socket
        to the matching lists
        :param client_socket: the client socket
        :param message: message to send
        """
        self.send_sockets.append(client_socket)
        # add the length description
        # according to the protocol
        message = \
            str(len(message)) \
            + LENGTH_SEPARATION_CHAR \
            + message
        self.messages_to_send.append((client_socket, message))


s = NodeServer(Logging('123').logger)
s.run()
