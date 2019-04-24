# -*- coding: utf-8 -*-
from wallet import Wallet
from miner import Miner
from logger import Logger
from database import BlockChainDB


def test1():
    """
    tests wallets without p2p network,
    the test is using common database
    for all wallets
    """
    logger = Logger('test1')
    logger.info('Test 1 starts')
    block_chain_db = BlockChainDB(logger)

    # creates two wallets in the system
    wallet1 = Wallet.new_wallet(block_chain_db, logger)
    wallet2 = Wallet.new_wallet(block_chain_db, logger)

    # check that their initial value is 0
    assert wallet1.balance == 0
    assert wallet2.balance == 0

    # creates the miner in the system
    wallet3 = Wallet.new_wallet(block_chain_db, logger)
    miner = Miner(wallet3)

    # mine the genesis block and check the miner balance
    miner.mine()
    first_balance = miner.wallet.get_balance()
    assert first_balance > 0

    # transfer from the miner to wallet1
    # and mine the new block
    assert miner.wallet.create_transaction(miner.wallet.balance, wallet1.address)
    miner.mine()

    # check the new balances
    assert wallet1.get_balance() == first_balance
    second_balance = miner.wallet.get_balance()
    assert second_balance > 0

    # creates new transactions from the miner
    # and wallet1 to wallet2 and mine the new block
    wallet1.create_transaction(wallet1.get_balance(), wallet2.address)
    miner.wallet.create_transaction(second_balance, wallet2.address)
    miner.mine()

    # check the new balances
    assert wallet2.get_balance() == (first_balance+second_balance)
    assert miner.wallet.get_balance() > 0

    # create new transaction that demands change
    # and mine the new block
    wallet2.create_transaction(first_balance+1, wallet1.address)
    miner.mine()

    # check the balances
    assert wallet2.get_balance() == second_balance - 1
    assert not wallet2.create_transaction(second_balance, wallet1.address)

    logger.info('Finish successfully test 1')
    block_chain_db.close_connection()


if __name__ == '__main__':
    test1()