# -*- coding: utf-8 -*-
from core_code.wallet import Wallet
from core_code.miner import Miner
from core_code.logger import Logging
from core_code.database import BlockChainDB
import unittest
from GUI.ui_runner import UiRunner


class Tests(unittest.TestCase):
    def setUp(self):
        """
        set up the logger 
        """
        self.logger = Logging('test1').logger

    def test1(self):
        """
        tests wallets without p2p network,
        the test is using common database
        for all wallets
        """
        self.logger.info('Test 1 starts')
        self.block_chain_db = BlockChainDB(self.logger, 'test1.db')

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
        first_balance = miner.wallet.get_balance()
        self.assertGreater(first_balance, 0)

        # transfer from the miner to wallet1
        # and mine the new block
        self.assertTrue(miner.wallet.create_transaction(miner.wallet.balance,
                                                        wallet1.address))
        miner.mine()

        # check the new balances
        self.assertEqual(wallet1.get_balance(), first_balance)
        second_balance = miner.wallet.get_balance()
        self.assertGreater(second_balance, 0)

        # creates new transactions from the miner
        # and wallet1 to wallet2 and mine the new block
        wallet1.create_transaction(wallet1.get_balance(), wallet2.address)
        miner.wallet.create_transaction(second_balance, wallet2.address)
        miner.mine()

        # check the new balances
        self.assertEqual(wallet2.get_balance(),
                         (first_balance+second_balance))
        self.assertGreater(miner.wallet.get_balance(), 0)

        # create new transaction that demands change
        # and mine the new block
        wallet2.create_transaction(first_balance+1, wallet1.address)
        miner.mine()

        # check the balances
        self.assertEqual(wallet2.get_balance(), second_balance - 1)
        self.assertFalse(wallet2.create_transaction(
            second_balance, wallet1.address))
        self.assertEqual(wallet1.get_balance(), first_balance+1)

        w2 = Wallet.new_wallet(self.block_chain_db, self.logger)
        UiRunner(wallet1.private_key, self.logger, self.block_chain_db).run()
        miner.mine()
        UiRunner(w2.private_key, self.logger, self.block_chain_db).run()
        UiRunner(wallet1.private_key, self.logger, self.block_chain_db).run()
        self.block_chain_db.close_connection()
        self.logger.info('Finish successfully test 1')


if __name__ == '__main__':
    unittest.main()
