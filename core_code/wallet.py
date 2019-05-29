# -*- coding: utf-8 -*-
from core_code.crypto_set import CryptoSet
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, RIPEMD160
from core_code.transaction import Transaction, \
    Input, Output, UnspentOutput

COMPARE_KEYS_MESS = 'compare'
GENERATE_NUMBER = 2048


class Wallet(CryptoSet):
    def __init__(self, private_key, block_chain_db, logger):
        """
        constructor
        """
        super(Wallet, self).__init__(private_key)
        self.address = self.find_address(self.public_key)
        self.block_chain_db = block_chain_db
        self.unspent_outputs = []
        self.update_unspent_outputs()
        self.balance = 0
        self.update_balance()
        self.transactions = []
        self.update_transactions()
        self.logger = logger
        self.logger.info(
            "Address- "
            ""+self.address+' is in the system')

    @classmethod
    def new_wallet(cls, block_chain, logger):
        """
        factory method
        """
        logger.info("Creating new wallet")
        private_key = RSA.generate(GENERATE_NUMBER)
        """
        load the private key to the file using pickle
        """
        return cls(private_key, block_chain, logger)

    def can_unlock_output(self, transaction_output):
        """
        the function checks if the wallet
        can unlock the output
        :param transaction_output: an output from a transaction
        :returns: true if the output can be unlocked
        otherwise false
        """
        unlock_address = transaction_output.address
        if unlock_address != self.address:
            return False
        return True

    def is_unspent_output(self, transaction_to_check, output_index):
        """
        the function checks if the given output
        was spent by going throw the block_chain
        :param transaction_to_check: a transaction that contains the
        output to check
        :param output_index: the index of the output
        inside the transaction
        :returns: false if the output was spent
        and true otherwise
        """
        # go throw all the inputs in the block chain
        # and checks weather they use the output
        for block in self.block_chain_db.chain:
            for transaction in block.transactions:
                for transaction_input in transaction.inputs:
                    if transaction_input.transaction_id == \
                            transaction_to_check.transaction_id:
                        if transaction_input.output_index == output_index:
                            return False
        return True

    def update_balance(self):
        """
        the function calculate and
        updates the wallet's balance
        """
        self.update_unspent_outputs()
        balance = 0
        for unspent_output in self.unspent_outputs:
            balance += unspent_output.output.value
        self.balance = balance

    def update_unspent_outputs(self):
        """
        the function finds all the unspent
        outputs which belongs to the wallet
        and updates it
        """
        unspent_outputs = []

        # go throw all the outputs in the block chain
        for block in self.block_chain_db.chain:
            for transaction in block.transactions:
                output_index = 0
                for transaction_output in transaction.outputs:
                    can_unlock = self.can_unlock_output(transaction_output)
                    if can_unlock and self.is_unspent_output(
                            transaction, output_index):
                        unspent_outputs.append(UnspentOutput(
                            transaction_output,
                            transaction.transaction_id,
                            output_index))
                    output_index += 1

        self.unspent_outputs = unspent_outputs

    def create_transaction(self, amount, recipient_address):
        """
        the functions creates transaction which
        contains the amount of coins to send
        the recipient address, the function implements
        the transaction in the block chain
        :param amount: the amount to send
        :param recipient_address: the address to send the
        coins to
        :returns: true if there is enough money to the
        transaction if so it returns the transaction itself also,
         and false otherwise
        """
        # checks weather there is enough money
        # to the transaction
        if amount > self.balance:
            self.logger.info(self.address+'- not enough money to send')
            return False, None

        # creates the new transaction
        new_transaction = Transaction([], [])
        sending_amount = 0
        change = 0
        for unspent_output in self.unspent_outputs:
            # creating the proof
            data_to_sign = unspent_output.transaction_id
            data_to_sign += recipient_address
            data_to_sign = self.hash(data_to_sign).hexdigest()
            data_to_sign += str(amount)
            data_to_sign = self.hash(data_to_sign)
            signature = self.sign(data_to_sign)
            proof = [signature, self.public_key]
            new_transaction.add_input(Input(
                unspent_output.transaction_id,
                unspent_output.output_index,
                proof))
            sending_amount += unspent_output.output.value
            if sending_amount >= amount:
                change = sending_amount - amount
                sending_amount = amount
        new_transaction.add_output(
            Output(sending_amount,
                   recipient_address))

        # add change if it is needed
        if change > 0:
            new_transaction.add_output(Output(change, self.address))

        # distributes the transaction
        self.logger.info(self.address+" is sending "+str(
            amount)+" LPC to "+recipient_address)
        self.block_chain_db.add_transaction(new_transaction)
        return True, new_transaction

    def update_transactions(self):
        """
        the function updates the list of the wallet
        transactions
        """
        self.transactions = []
        for block in self.block_chain_db.chain:
            for transaction in block.transactions:
                output = transaction.outputs[0]
                if output.address == self.address:
                    self.transactions.append(transaction)
                # check if the transaction is not coin base
                if transaction.inputs[0].proof[1] is not '':
                    if self.equals_public_keys(
                            transaction.inputs[0].proof[1]):
                        self.transactions.append(transaction)

    @staticmethod
    def find_address(public_key):
        """
        the function calculates the address
        of the owner of the public key
        :param public_key: public key object
        :return: the wallet address of the owner
        """
        return RIPEMD160.new(
            SHA256.new(
                public_key.exportKey()).hexdigest()
        ).hexdigest()

    def equals_public_keys(self, public_key):
        """
        the function check if the given
        public key is equals to the wallet's
        public key
        :param public_key: the key to compare
        with
        :return: true if the keys are the same
        and false otherwise
        """
        e1 = self.encrypt(
            public_key,
            COMPARE_KEYS_MESS)
        e2 = self.encrypt(self.public_key, COMPARE_KEYS_MESS)
        if self.decrypt(e1) == self.decrypt(e2):
            return True
        else:
            return False

    def mine(self):
        """
        mines new block in the
        block chain
        """
        self.block_chain_db.\
            add_new_block_to_db(self.address)
