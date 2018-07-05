from bit.network.services import NetworkAPI
from bit import PrivateKeyTestnet

import random 

# ntwrk = NetworkAPI()
# money = ntwrk.get_balance_testnet('myuUCjnJxRmCm6aC2gpmY2nyGGS29PApRx')
# print(money) 
# key = PrivateKeyTestnet('93NUtNNeKfpPZTtB6dEBxjPhBBs8ksYZnHh26RuB8Xe9QUychy6')
# print(key)
# amount = float(random.randrange(1, 500))/100
# print(amount)
# dest = 'mrHXbzTszNWhav7egmfXVktopTBMotS4mp'
# outputs = [(dest, amount, 'mbtc')]
# unspents = ntwrk.get_unspent_testnet('myuUCjnJxRmCm6aC2gpmY2nyGGS29PApRx')
# print("UNSPENTS: ", unspents)
# tx = key.create_transaction(outputs, fee=8500, unspents=unspents)
# print("TRANSACTION: ", tx)
# stx = ntwrk.broadcast_tx_testnet(tx)
# print("SUCCESS!")
# key.send(outputs, fee=8500, unspents=unspents)

def BTC_process(destination, priv_wif, fee, amnt):
    ntwrk = NetworkAPI()
    f = fee
    dest = destination
    key = PrivateKeyTestnet(priv_wif)
    org = key.address
    unspents = ntwrk.get_unspent_testnet(org)
    outputs = [(dest, amnt, 'mbtc')]
    key.send(outputs, fee=f, unspents=unspents)
    receipt = ntwrk.get_transactions_testnet(dest)
    return receipt

    #amnt = float(random.randrange(1, 500))/100
    # tx = key.create_transaction(outputs, fee=f, unspents=unspents)
    # ntwrk.broadcast_tx_testnet(tx)

# ntwrk = NetworkAPI()
# key = PrivateKeyTestnet('92o2cgzAv9RyGhDQLrDDLHno8DHHEb5FPY8pnYNkWgkSYQEc9Ki')
# org = key.address
# unspents = ntwrk.get_unspent_testnet(org)
# outputs = [('mpGm1eUmVWVAM27dpD6WjkVNQuNCrwR8Sc', 8, 'mbtc'), ('mmekyaYocFPw19vApBnmoUWPU58XNayrtR', 10, 'mbtc'), ('msJtqyzj6vZzG2HHyaoYN5W2ZmT9w8n1Tf', 12, 'mbtc'), ('mpXbsqMUenCkukLjv4mWrrRQTNdeZQZHk7', 14, 'mbtc'), ('n3k4NfuwrjLb2NNk5vGbT2FcDss3VQPXWf', 16, 'mbtc')]
# key.send(outputs, fee=5000, unspents=unspents)
# print('DONE')
# receipt = ntwrk.get_transactions_testnet('mpGm1eUmVWVAM27dpD6WjkVNQuNCrwR8Sc')
# tx1 = receipt[-1]
# receipt2 = ntwrk.get_transactions_testnet('mmekyaYocFPw19vApBnmoUWPU58XNayrtR')
# tx2 = receipt2[-1]
# print(tx1, '/n', tx2)

# dest = 'n1THoWEzKuFvBxGYq74BVTTPFJ79zDyR8e'
# priv = '93NUtNNeKfpPZTtB6dEBxjPhBBs8ksYZnHh26RuB8Xe9QUychy6'
# fee = 5000
# num = 5
# BTC_process(dest, priv, fee, num)
# print("Done")


# def get_unspent_testnet(cls, address)
# def broadcast_tx_testnet(cls, tx_hex)
# def create_transaction or send(self, outputs, fee=None, leftover=None, combine=True, message=None, unspents=None):