# -*- coding: utf-8 -*-
from core_code.wallet import Wallet
from core_code.miner import Miner
from core_code.logger import Logging
from core_code.database import BlockChainDB
from core_code.node import Node
import unittest


class Tests(unittest.TestCase):
    def test1(self):
        """
        tests wallets without p2p network,
        the test is using common database
        for all wallets
        """
        self.logger = Logging('test').logger
        self.block_chain_db = BlockChainDB(
            self.logger, 'test.db')
        self.logger.info('Test 1 starts')

        # creates two wallets in the system
        wallet1 = Wallet.new_wallet(self.block_chain_db, self.logger)
        wallet2 = Wallet.new_wallet(self.block_chain_db, self.logger)

        # check that their initial value is 0
        self.assertEqual(wallet1.balance, 0)
        self.assertEqual(wallet2.balance, 0)

        # creates the miner in the system
        wallet3 = Wallet.new_wallet(self.block_chain_db, self.logger)
        miner = Miner(wallet3)

        # mine the genesis block and check the miner balance
        miner.mine()
        miner.wallet.update_balance()
        first_balance = miner.wallet.balance
        self.assertGreater(first_balance, 0)

        # transfer from the miner to wallet1
        # and mine the new block
        self.assertTrue(miner.wallet.create_transaction(miner.wallet.balance,
                                                        wallet1.address))
        miner.mine()

        # check the new balances
        wallet1.update_balance()
        miner.wallet.update_balance()
        self.assertEqual(wallet1.balance, first_balance)
        second_balance = miner.wallet.balance
        self.assertGreater(second_balance, 0)

        # creates new transactions from the miner
        # and wallet1 to wallet2 and mine the new block
        wallet1.create_transaction(wallet1.balance, wallet2.address)
        miner.wallet.create_transaction(second_balance, wallet2.address)
        miner.mine()

        # check the new balances
        wallet1.update_balance()
        miner.wallet.update_balance()
        wallet2.update_balance()
        self.assertEqual(wallet2.balance,
                         (first_balance+second_balance))
        self.assertGreater(miner.wallet.balance, 0)

        # create new transaction that demands  a
        # change to return
        # and mine the new block
        wallet2.create_transaction(first_balance+1, wallet1.address)
        miner.mine()

        # check the balances
        wallet2.update_balance()
        miner.wallet.update_balance()
        wallet1.update_balance()
        self.assertEqual(wallet2.balance, second_balance - 1)
        self.assertFalse(wallet2.create_transaction(
            second_balance, wallet1.address))
        self.assertEqual(wallet1.balance, first_balance+1)
        self.block_chain_db.close_connection()
        self.logger.info('Finish successfully test 1')

    def test2(self):
        """
        test the communication protocol
        """
        wallet1 = Wallet.new_wallet(self.block_chain_db,
                                    self.logger)
        self.node = Node(self.logger, wallet1)
        self.node.update_chain()


if __name__ == '__main__':
    unittest.main()
