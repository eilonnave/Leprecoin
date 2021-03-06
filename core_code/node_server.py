# -*- coding: utf-8 -*-
import select
import socket
import time

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
        self.received_messages = []
        self.to_close = False
        self.clients_addresses = []
        try:
            # binding and listening
            self.server_socket.bind((SERVER_IP, COMMUNICATION_PORT))
            logger.info('Listening on port ' + str(COMMUNICATION_PORT))
            self.server_socket.listen(LISTEN_SIZE)
            # initialize the lists for
            # the usage of the server
            self.open_clients_sockets = []
            self.readable = []
            self.exceptional = []
            self.is_closed = False
        except socket.error as err:
            self.logger.info('Could not open node- ' + str(err))
            self.server_socket.close()
            self.is_closed = True

    def run(self):
        """
        the function runs the server
        """
        while not self.to_close and not self.is_closed:
            self.readable, self.exceptional = select.select(
                [self.server_socket] +
                self.open_clients_sockets,
                [],
                self.open_clients_sockets)[::2]
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
                self.clients_addresses.append((client_socket, client_address[0]))
            else:
                try:
                    client_address = ''
                    length = self.extract_pack_length(current_socket)
                    for client_tup in self.clients_addresses:
                        if client_tup[0] is current_socket:
                            client_address = client_tup[1]
                            break
                    if length != 0:
                        self.received_messages.append((
                            self.receive_message(length, current_socket), client_address))
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
        print "extract_pack_length = {0}".format(int(length[:-1]))
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
        data = client_socket.recv(length)
        bytes_read = len(data)
        while bytes_read < length:
            time.sleep(0.01)
            data += client_socket.recv(length-bytes_read)
            bytes_read = len(data)

        return data

    def disconnect_connection(self, client_socket):
        """
        the function disconnect properly connection
        with the client
        :param client_socket: the socket of the client
        """
        client_socket.close()
        index = -1
        for tup in self.clients_addresses:
            if tup[0] is client_socket:
                index = self.clients_addresses.index(tup)
                break
        self.clients_addresses.pop(index)
        self.open_clients_sockets.remove(client_socket)

    def get_received_messages(self):
        """
        the function returns all the messages
        that the server received in a new list
        :return: all the messages the the server
        received and that were not handled
        """
        received_messages = []
        for message in self.received_messages:
            received_messages.append(message)
        return received_messages

    def remove_message(self, message):
        """
        the function removes the given
        message from the received list
        :param message: the message to remove
        """
        index = -1
        i = 0
        for message_tup in self.received_messages:
            if message[0] is message_tup[0] and message[1] == message_tup[1]:
                index = i
                break
            i += 1
        self.received_messages.pop(index)
