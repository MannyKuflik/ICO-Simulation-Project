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

def BTC_process(destination, priv_wif, fee):
    ntwrk = NetworkAPI() #define netwrok class from bit
    f = fee # assign variables
    dest = destination # assign variables
    key = PrivateKeyTestnet(priv_wif) # get key from inputed private_key wif
    origin = key.address
    amnt = float(random.randrange(1, 500))/100 # generate random amount for transaction
    unspents = ntwrk.get_unspent_testnet(origin) # get unspent BTC from origin adress
    outputs = [(dest, amnt, 'mbtc')] # define tuple to use as outputs: [(Address_to_send_to, Amount, Currency)]
    tx = key.create_transaction(outputs, fee=f, unspents=unspents) # generate signed transaction
    receipt = ntwrk.get_transactions_testnet(dest)
    # ntwrk.broadcast_tx_testnet(tx) # broadcast tx to network
    ## alternativley key.send() takes the same arguments as key.create_transaction(), 
    # but it creates the signed transaction and broadcasts it in a single step
    # ex: >>> key.send(outputs, fee=f, unspents=unspents)
    return receipt
# def get_unspent_testnet(cls, address)
# def broadcast_tx_testnet(cls, tx_hex)
# def create_transaction or send(self, outputs, fee=None, leftover=None, combine=True, message=None, unspents=None):