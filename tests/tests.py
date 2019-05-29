# -*- coding: utf-8 -*-
from core_code.wallet import Wallet
from core_code.miner import Miner
from core_code.logger import Logging
from core_code.database import BlockChainDB
from core_code.node import Node
import unittest


class Tests(unittest.TestCase):
    def setUp(self):
        """
        set up the logger and the data base
        """
        self.logging = Logging('tests')
        self.logger = self.logging.logger
        self.block_chain_db = BlockChainDB(self.logger,
                                           'tests.db')

    def tearDown(self):
        """
        tear down the logger handler
        """
        self.logging.remove_handler()

    def test1(self):
        """
        tests wallets without p2p network,
        the test is using common database
        for all wallets
        """
        self.logger.info('Test 1 starts')

        # creates two wallets in the system
        wallet1 = Wallet.new_wallet(self.block_chain_db, self.logger)
        wallet2 = Wallet.new_wallet(self.block_chain_db, self.logger)

        # check that their initial value is 0
        self.assertEqual(wallet1.balance, 0)
        self.assertEqual(wallet2.balance, 0)

        # creates the miner in the system
        wallet3 = Wallet.new_wallet(self.block_chain_db, self.logger)

        # mine the genesis block and check the miner balance
        wallet3.mine()
        wallet3.update_balance()
        first_balance = wallet3.balance
        self.assertGreater(first_balance, 0)

        # transfer from the miner to wallet1
        # and mine the new block
        self.assertTrue(wallet3.create_transaction(wallet3.balance, wallet1.address)[0])
        wallet3.mine()

        # check the new balances
        wallet1.update_balance()
        wallet3.update_balance()
        self.assertEqual(wallet1.balance, first_balance)
        second_balance = wallet3.balance
        self.assertGreater(second_balance, 0)

        # creates new transactions from the miner
        # and wallet1 to wallet2 and mine the new block
        wallet1.create_transaction(wallet1.balance, wallet2.address)
        wallet3.create_transaction(second_balance, wallet2.address)
        wallet3.mine()

        # check the new balances
        wallet1.update_balance()
        wallet3.update_balance()
        wallet2.update_balance()
        self.assertEqual(wallet2.balance,
                         (first_balance+second_balance))
        self.assertGreater(wallet3.balance, 0)

        # create new transaction that demands  a
        # change to return
        # and mine the new block
        wallet2.create_transaction(first_balance+1.5, wallet1.address)
        wallet3.mine()

        # check the balances
        wallet2.update_balance()
        wallet3.update_balance()
        wallet1.update_balance()
        self.assertEqual(wallet2.balance, second_balance - 1.5)
        self.assertFalse(wallet2.create_transaction(
            second_balance, wallet1.address)[0])
        self.assertEqual(wallet1.balance, first_balance+1.5)
        self.block_chain_db.close_connection()
        self.logger.info('Finish successfully test 1')

    def test2(self):
        """
        test the communication protocol
        """
        self.logger.info('Test 2 starts')
        self.node = Node(self.logger,
                         self.block_chain_db)
        self.node.update_chain()
        self.logger.info('Finish successfully test 2')
        while True:
            self.node.handle_messages()


if __name__ == '__main__':
    unittest.main()
