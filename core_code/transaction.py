# -*- coding: utf-8 -*-
from Crypto.Hash import *


UN_SPENT_OUTPUTS_TABLE_NAME = 'utxo'
TRANSACTIONS_TABLE_NAME = 'transactions'
INPUTS_TABLE_NAME = 'inputs'
OUTPUTS_TABLE_NAME = 'outputs'
TRANSACTION_STRUCTURE = '(transaction_id integer, ' \
                        'block_number integer)'
# the transaction_number in the input and output
# serialization refers to the transaction id (hash)
OUTPUT_STRUCTURE = '(value integer, ' \
                   'address text, ' \
                   'transaction_number text)'
INPUT_STRUCTURE = '(transaction_id text, ' \
                  'output_index integer, ' \
                  'proof text, ' \
                  'transaction_number text)'


class Transaction:
    def __init__(self, inputs, outputs):
        """
        constructor
        """
        self.inputs = inputs
        self.outputs = outputs
        self.transaction_id = self.hash_transaction()

    def add_input(self, transaction_input):
        """
        the function adds the input
        to the transaction and updates the id
        """
        self.inputs.append(transaction_input)
        self.transaction_id = self.hash_transaction()

    def add_output(self, transaction_output):
        """
        the function adds the output
        to the transaction and updates the id
        """
        self.outputs.append(transaction_output)
        self.transaction_id = self.hash_transaction()

    def hash_transaction(self):
        """
        the function hashes the transaction's id
        :returns: the hashed id
        """
        transaction_hash = ''

        # hash the inputs
        if len(self.inputs) != 0:
            transaction_hash = self.inputs[0].hash_input()
            for transaction_input in self.inputs[1:]:
                transaction_hash += transaction_input.hash_input()
                transaction_hash = SHA256.new(transaction_hash).hexdigest()

        # hash the outputs
        if len(self.outputs) == 0:
            return transaction_hash
        for transaction_output in self.outputs:
            transaction_hash += transaction_output.hash_output()
            transaction_hash = SHA256.new(transaction_hash).hexdigest()

        return transaction_hash

    def serialize(self, block_number):
        """
        the function serializes the transaction
        :param block_number: the block number which the
        transaction belongs to
        :returns: the serialized transaction
        """
        return self.transaction_id, block_number

    @classmethod
    def deserialize(cls, inputs, outputs):
        """
        the function deserializes the transaction
        from the given lists
        :param inputs: list of the transaction's
        inputs
        :param outputs: list of the transaction's
        outputs
        :returns: the deserialized object
        """
        inputs = inputs
        outputs = outputs
        return cls(inputs, outputs)


class Output:
    def __init__(self, value, address):
        """
        constructor
        """
        self.value = value
        # address which belongs to the wallet that can use the output
        self.address = address

    def hash_output(self):
        """
        the function hashes the input
        :returns: the hash code of the
        input
        """
        return SHA256.new(self.to_string()).hexdigest()

    def to_string(self):
        """
        the function converts the outputs to a string
        :returns: the output's string
        """
        output_string = str(self.value)
        output_string += self.address
        return output_string

    def serialize(self, transaction_number):
        """
        the function serializes the output
        :param transaction_number: the transaction number which the
        output belongs to
        :returns: the serialized output
        """
        return self.value, \
            self.address, \
            transaction_number

    @classmethod
    def deserialize(cls, serialized_output):
        """
        the function deserializes the output
        from the given list
        :param serialized_output: the serialized output
        :returns: the deserialized output
        """
        value = serialized_output[0]
        address = serialized_output[1]
        return cls(value, address)


class Input:
    def __init__(self, transaction_id, output_index, proof):
        """
        constructor
        """
        self.transaction_id = transaction_id
        self.output_index = output_index
        # the proof is the tuple that contains the signature and the public key
        self.proof = proof

    def hash_input(self):
        """
        the function hashes the input
        :returns: the hash code of the
        input
        """
        return SHA256.new(self.to_string()).hexdigest()

    def to_string(self):
        """
        the function converts the input to a string
        :returns: the input's string
        """
        input_string = self.transaction_id
        input_string += str(self.output_index)
        input_string += str(self.proof)
        return input_string

    def serialize(self, transaction_number):
        """
        the function serializes the input
        :param transaction_number: the transaction number which the
        input belongs to
        :returns: the serialized input
        """
        return self.transaction_id, \
            self.output_index, \
            str(self.proof),\
            transaction_number

    @classmethod
    def deserialize(cls, serialized_input):
        """
        the function deserializes the input
        from the given list
        :param serialized_input: the serialized input
        :returns: the deserialized input
        """
        transaction_id = str(serialized_input[0])
        output_index = serialized_input[1]
        proof = serialized_input[2]
        return cls(transaction_id, output_index, proof)


class UnspentOutput:
    def __init__(self, output, transaction_id, output_index):
        """
        constructor
        """
        self.output = output
        self.transaction_id = transaction_id
        self.output_index = output_index