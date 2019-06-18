# -*- coding: utf-8 -*-
import msgpack
import ast
from core_code.transaction import Transaction, \
    Input, \
    Output, \
    INPUTS_KEY, \
    OUTPUTS_KEY
from core_code.block import Block, BLOCK_KEY, TRANSACTIONS_KEY


VERSION_CODE = 1
BEST_HEIGHT_KEY = 'best_height'
ADDRESS_FROM_KEY = 'address_from'
GET_BLOCKS_CODE = 2
INV_CODE = 3
DATA_TYPE_KEY = 'data_type'
HASH_CODES_KEY = 'hash_codes'
HASH_CODE_KEY = 'hash_code'
GET_DATA_CODE = 4
BLOCK_MESSAGE_CODE = 5
TRANSACTION_MESSAGE_CODE = 6
BLOCK_NUMBER_KEY = 'number'
NONCE_KEY = 'nonce'
PREV_KEY = 'prev'
DIFFICULTY_KEY = 'difficulty'
TIME_STAMP_KEY = 'time_stamp'
GET_ADDRESSES_CODE = 7
ADDRESSES_CODE = 8
ADDRESSES_KEY = 'addresses'


class Error(object):
    """
    the object uses to alert
    the user of illegal message
    from another peer
    """
    def __init__(self, error):
        """
        constructor
        """
        self.error = error


class MessagesHandler(object):
    def __init__(self, message, is_packed):
        """
        constructor
        """
        self.message = message
        self.is_packed = is_packed

    def unpack_message(self):
        """
        the function unpacks the
        packed message
        """
        if self.is_packed:
            self.message = msgpack.unpackb(self.message,
                                           ext_hook=self.ext_hook)
            self.is_packed = False

    @staticmethod
    def ext_hook(code, data):
        """
        the function returns the instance
        from the data, the instance matches
        the code.
        :param code: the code that identifies
        the instance
        :param data: the string of data from the
        packed message
        :return: instance from the data
        """
        if code == VERSION_CODE:
            version_message = Version.unpack(data)
            return version_message
        if code == GET_BLOCKS_CODE:
            get_blocks_message = GetBlocks.unpack(data)
            return get_blocks_message
        if code == INV_CODE:
            inv_message = Inv.unpack(data)
            return inv_message
        if code == GET_DATA_CODE:
            get_data_message = GetData.unpack(data)
            return get_data_message
        if code == BLOCK_MESSAGE_CODE:
            block_message = BlockMessage.unpack(data)
            return block_message
        if code == TRANSACTION_MESSAGE_CODE:
            transaction_message = TransactionMessage.unpack(data)
            return transaction_message
        if code == GET_ADDRESSES_CODE:
            get_addresses_message = GetAddresses.unpack(data)
            return get_addresses_message
        if code == ADDRESSES_CODE:
            addresses_message = AddressesMessage.unpack(data)
            return addresses_message
        return Error('Wrong code is inserted')

    def pack(self):
        """
        the function packs the message
        """
        if not self.is_packed:
            self.message = self.message.pack()
            self.is_packed = True

    def change_message(self, message, is_packed):
        """
        the function changes the message
        that the message handler has
        :param message: the new message
        :param is_packed: whether the message is packed
        or not
        """
        self.message = message
        self.is_packed = is_packed


class Message(object):
    def __init__(self, code, address_from):
        self.code = code
        self.address_from = address_from

    def pack(self):
        """
        the function packs the
        message
        :returns: the packed message
        """
        return msgpack.packb(msgpack.ExtType(self.code,
                                             self.__str__()))

    def __str__(self):
        """
        the functions returns a string
        of the object in formation of
        dictionary for the packing
        :returns: string of the object
        """
        return str(self.__dict__)


class GetAddresses(Message):
    """
    The meaning of get blocks message is
    to ask "show me what addresses you have"
    """
    def __init__(self, address_from):
        """
        constructor
        """
        super(GetAddresses, self).__init__(GET_ADDRESSES_CODE, address_from)

    @classmethod
    def unpack(cls, data):
        """
        the function unpacks
        the packed get addresses
        :param data: the packed data
        :returns: the unpacked get addresses
        object
        """
        try:
            data = ast.literal_eval(data)
            try:
                address_from = data[ADDRESS_FROM_KEY]
                return cls(address_from)
            except KeyError as error:
                return Error(error)
        except ValueError as error:
            return Error(error)


class AddressesMessage(Message):
    """
    Transfer the known addresses
    """
    def __init__(self, address_from, addresses):
        """
        constructor
        """
        self.addresses = addresses
        super(AddressesMessage, self).__init__(ADDRESSES_CODE,
                                               address_from)

    @classmethod
    def unpack(cls, data):
        """
        the function unpacks
        the packed addresses message
        :param data: the packed data
        :returns: the unpacked get message
        object
        """
        try:
            data = ast.literal_eval(data)
            try:
                address_from = data[ADDRESS_FROM_KEY]
                addresses = data[ADDRESSES_KEY]
                return cls(address_from,
                           addresses)
            except KeyError as error:
                return Error(error)
        except ValueError as error:
            return Error(error)


class Version(Message):
    """
    The purpose of version message is
    to check if the node contains the
    updated block_chain - the longest
    in the system
    """
    def __init__(self, best_height, address_from):
        """
        constructor
        """
        self.best_height = best_height
        super(Version, self).__init__(VERSION_CODE, address_from)

    @classmethod
    def unpack(cls, data):
        """
        the function unpacks
        the packed version
        :param data: the packed data
        :returns: the unpacked version
        object
        """
        try:
            data = ast.literal_eval(data)
            try:
                best_height = data[BEST_HEIGHT_KEY]
                address_from = data[ADDRESS_FROM_KEY]
                return cls(best_height, address_from)
            except KeyError as error:
                return Error(error)
        except ValueError as error:
            return Error(error)


class GetBlocks(Message):
    """
    The meaning of get blocks message is
    to ask "show me what blocks you have"
    """
    def __init__(self, address_from, hash_code):
        """
        constructor
        """
        super(GetBlocks, self).__init__(GET_BLOCKS_CODE, address_from)
        # hash code of the node's latest block
        self.hash_code = hash_code

    @classmethod
    def unpack(cls, data):
        """
        the function unpacks
        the packed get blocks
        :param data: the packed data
        :returns: the unpacked get blocks
        object
        """
        try:
            data = ast.literal_eval(data)
            try:
                address_from = data[ADDRESS_FROM_KEY]
                hash_code = data[HASH_CODE_KEY]
                return cls(address_from, hash_code)
            except KeyError as error:
                return Error(error)
        except ValueError as error:
            return Error(error)


class Inv(Message):
    """
    The purpose of inv message is to
    show other nodes what blocks or
    transactions current node has
    """
    def __init__(self, address_from, data_type, hash_codes):
        """
        constructor
        """
        self.data_type = data_type
        self.hash_codes = hash_codes
        super(Inv, self).__init__(INV_CODE, address_from)

    @classmethod
    def unpack(cls, data):
        """
        the function unpacks
        the packed inv
        :param data: the packed data
        :returns: the unpacked inv
        object
        """
        try:
            data = ast.literal_eval(data)
            try:
                address_from = data[ADDRESS_FROM_KEY]
                data_type = data[DATA_TYPE_KEY]
                hash_codes = data[HASH_CODES_KEY]
                return cls(address_from,
                           data_type,
                           hash_codes)
            except KeyError as error:
                return Error(error)
        except ValueError as error:
            return Error(error)


class GetData(Message):
    """
    The purpose of get data message is to
    request a certain block or transaction
    """
    def __init__(self, address_from, data_type, hash_code):
        """
        constructor
        """
        self.data_type = data_type
        self.hash_code = hash_code
        super(GetData, self).__init__(GET_DATA_CODE,
                                      address_from)

    @classmethod
    def unpack(cls, data):
        """
        the function unpacks
        the packed get data
        :param data: the packed data
        :returns: the unpacked get data
        object
        """
        try:
            data = ast.literal_eval(data)
            try:
                address_from = data[ADDRESS_FROM_KEY]
                data_type = data[DATA_TYPE_KEY]
                hash_code = data[HASH_CODE_KEY]
                return cls(address_from,
                           data_type,
                           hash_code)
            except KeyError as error:
                return Error(error)
        except ValueError as error:
            return Error(error)


class BlockMessage(Message):
    """
    Transfer of block data
    """
    def __init__(self, address_from, block):
        """
        constructor
        """
        self.block = block
        super(BlockMessage, self).__init__(BLOCK_MESSAGE_CODE,
                                           address_from)

    @classmethod
    def unpack(cls, data):
        """
        the function unpacks
        the packed block message
        :param data: the packed data
        :returns: the unpacked block message
        object
        """
        try:
            data = ast.literal_eval(data)
            try:
                address_from = data[ADDRESS_FROM_KEY]
                serialized_block = ast.literal_eval(data[BLOCK_KEY])
                transactions_dict_list = []
                for transaction in data[TRANSACTIONS_KEY]:
                    transactions_dict_list.append(ast.literal_eval(transaction))
                transactions = []
                for transaction in transactions_dict_list:
                    inputs = []
                    outputs = []
                    serialized_inputs = transaction[INPUTS_KEY]
                    serialized_outputs = transaction[OUTPUTS_KEY]
                    for serialized_input in serialized_inputs:
                        # convert the string to tuple
                        serialized_input = ast.literal_eval(serialized_input)
                        inputs.append(Input.deserialize(serialized_input))
                    for serialized_output in serialized_outputs:
                        serialized_output = ast.literal_eval(serialized_output)
                        outputs.append(Output.deserialize(serialized_output))
                    transactions.append(Transaction(inputs, outputs))
                block = Block.deserialize(serialized_block, transactions)
                return cls(address_from,
                           block)
            except KeyError as error:
                return Error(error)
        except ValueError as error:
            return Error(error)

    def __str__(self):
        """
        the functions returns a string
        of the block message in formation of
        dictionary for the packing
        :returns: string of the object
        """
        transactions = []
        for transaction in self.block.transactions:
            transactions.append(transaction.__str__())
        str_dict = {ADDRESS_FROM_KEY: self.address_from,
                    BLOCK_KEY: str(self.block.serialize()),
                    TRANSACTIONS_KEY: transactions}
        return str(str_dict)


class TransactionMessage(Message):
    """
    Transfer of transaction data
    """
    def __init__(self, address_from, transaction):
        """
        constructor
        """
        self.transaction = transaction
        super(TransactionMessage, self).__init__(
            TRANSACTION_MESSAGE_CODE,
            address_from)

    @classmethod
    def unpack(cls, data):
        """
        the function unpacks
        the packed transaction message
        :param data: the packed data
        :returns: the unpacked transaction
        message object
        """
        try:
            data = ast.literal_eval(data)
            try:
                address_from = data[ADDRESS_FROM_KEY]
                inputs = []
                outputs = []
                serialized_inputs = data[INPUTS_KEY]
                serialized_outputs = data[OUTPUTS_KEY]
                for serialized_input in serialized_inputs:
                    # convert the string to tuple
                    serialized_input = ast.literal_eval(serialized_input)
                    inputs.append(Input.deserialize(serialized_input))
                for serialized_output in serialized_outputs:
                    serialized_output = ast.literal_eval(serialized_output)
                    outputs.append(Output.deserialize(serialized_output))
                return cls(address_from,
                           Transaction(inputs, outputs))
            except KeyError as error:
                return Error(error)
        except ValueError as error:
            return Error(error)

    def __str__(self):
        """
        the functions returns a string
        of the transaction message in formation of
        dictionary for packing the
        transaction
        :returns: string of the object
        """
        str_dict = ast.literal_eval(self.transaction.__str__())
        str_dict[ADDRESS_FROM_KEY] = self.address_from
        return str(str_dict)


if __name__ == '__main__':
    v = Version(1, '1')
    msg_handler = MessagesHandler(v, False)
    msg_handler.pack()
    assert type(msg_handler.message) is str
    msg_handler.unpack_message()
    assert type(msg_handler.message) is Version
    assert msg_handler.message.best_height \
        == v.best_height
    assert msg_handler.message.address_from \
        == v.address_from

    g = GetBlocks('2', '123')
    msg_handler = MessagesHandler(g, False)
    msg_handler.pack()
    assert type(msg_handler.message) is str
    msg_handler.unpack_message()
    assert type(msg_handler.message) is GetBlocks
    assert msg_handler.message.address_from \
        == g.address_from
    assert msg_handler.message.hash_code == \
        g.hash_code

    i = Inv('1', 'transaction', ['1', '12'])
    msg_handler = MessagesHandler(i, False)
    msg_handler.pack()
    assert type(msg_handler.message) is str
    msg_handler.unpack_message()
    assert type(msg_handler.message) is Inv
    assert msg_handler.message.address_from \
        == i.address_from
    assert msg_handler.message.data_type \
        == i.data_type
    assert msg_handler.message.hash_codes \
        == i.hash_codes

    g = GetData('1', 'transaction', '1')
    msg_handler = MessagesHandler(g, False)
    msg_handler.pack()
    assert type(msg_handler.message) is str
    msg_handler.unpack_message()
    assert type(msg_handler.message) is GetData
    assert msg_handler.message.address_from \
        == g.address_from
    assert msg_handler.message.data_type \
        == g.data_type
    assert msg_handler.message.hash_code \
        == g.hash_code

    inputs_list = [Input('123', 0, ['123', '']), Input('1234', 1, ['1234', ''])]
    outputs_list = [Output(12, '123'), Output(13, '1234')]
    t = TransactionMessage('1', Transaction(inputs_list, outputs_list))
    msg_handler = MessagesHandler(t, False)
    msg_handler.pack()
    assert type(msg_handler.message) is str
    msg_handler.unpack_message()
    assert type(msg_handler.message) is TransactionMessage
    assert msg_handler.message.address_from \
        == t.address_from

    b = BlockMessage('1', Block(0, '0', [t.transaction, t.transaction]))
    msg_handler = MessagesHandler(b, False)
    msg_handler.pack()
    assert type(msg_handler.message) is str
    msg_handler.unpack_message()
    assert type(msg_handler.message) is BlockMessage
    assert msg_handler.message.address_from \
        == b.address_from

    g = GetAddresses('123')
    msg_handler = MessagesHandler(g, False)
    msg_handler.pack()
    assert type(msg_handler.message) is str
    msg_handler.unpack_message()
    assert type(msg_handler.message) is GetAddresses
    assert msg_handler.message.address_from \
        == g.address_from

    a = AddressesMessage('123', ['123', '12', '1234'])
    msg_handler = MessagesHandler(a, False)
    msg_handler.pack()
    assert type(msg_handler.message) is str
    msg_handler.unpack_message()
    assert type(msg_handler.message) is AddressesMessage
    assert msg_handler.message.address_from \
        == a.address_from
    assert msg_handler.message.addresses \
        == a.addresses



