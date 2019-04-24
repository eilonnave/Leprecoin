# -*- coding: utf-8 -*-
import os
import pickle


REFERENCES_FILE = 'references.pickle'
DEFAULT_DB_DIR = 'c:'
DEFAULT_BCK_REFERENCE = 'c://bck.db'
SECONDARY_BCK_REFERENCE = '.bck.db'
BLOCK_CHAIN_KEY = 'bck'
DEFAULT_UTXO_REFERENCE = 'utxo.db'
SECONDARY_UTXO_REFERENCE = '.utxo.db'
UNSPENT_OUTPUTS_KEY = 'utxo'


class References:
    def __init__(self):
        """
        constructor
        """
        # check if there is references database
        if not os.path.isfile(REFERENCES_FILE):
            self.create_references()
        else:
            # load the dictionary
            with open(REFERENCES_FILE, 'rb') as handle:
                self.dict = pickle.load(handle)

    def create_references(self):
        """
        create the references file and the
        references dict
        """
        self.dict = {BLOCK_CHAIN_KEY: DEFAULT_BCK_REFERENCE,
                     UNSPENT_OUTPUTS_KEY: DEFAULT_UTXO_REFERENCE}
        # check if the defaults dir exist:
        if not os.path.isdir(DEFAULT_DB_DIR):
            self.dict[BLOCK_CHAIN_KEY] = SECONDARY_BCK_REFERENCE
            self.dict[UNSPENT_OUTPUTS_KEY] = SECONDARY_UTXO_REFERENCE
        # dump the dict to the file
        print self.dict
        with open(REFERENCES_FILE, 'wb') as handle:
            pickle.dump(self.dict, handle,
                        protocol=pickle.HIGHEST_PROTOCOL)

    def get_block_chain_reference(self):
        """
        returns the block chain reference
        """
        return self.dict[BLOCK_CHAIN_KEY]

    def get_unspent_outputs_reference(self):
        """
        returns the unspent outputs reference
        """
        return self.dict[UNSPENT_OUTPUTS_KEY]


