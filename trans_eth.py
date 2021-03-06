from typing import List, Dict
from flask import Flask
from web3 import Web3, HTTPProvider, utils

import json
import sys
import random
import time

app = Flask(__name__)


# FROM_ADDR = "0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129"
# TO_ADDR = "0x6F544455D57caA0787A5200DA1FC379fc00B5Da5"
# PRIV_KEY = "8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4"
# VAL = random.randint(10000, 10000000)

# web3 = Web3(HTTPProvider('https://rinkeby.infura.io/UVgPTn3TgFMB0KhHUlif'))

def construct_tx(from_addr, to_address, val, nonce, web3):
    if not web3.isChecksumAddress(to_address):
        return False
    unique = nonce
    txparams = {
        'nonce': unique,
        'chainId': 4,  # chainID for rinkeby
        'to': to_address,
        'data': '',
        'value': val, 
        'gas': 24000,
        'gasPrice': web3.eth.gasPrice
    }
    return txparams

def send_eth(from_addr, to_address, val, priv_key, nonce, web3):
    tx = construct_tx(from_addr, to_address, val, nonce, web3) # this generates the transaction dict
    
    web3.eth.enable_unaudited_features()

    signed_tx = web3.eth.account.signTransaction(tx, priv_key)  # this returns a blob of hexadecimal text

    transhash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)  # this broadcasts the tx and returns a transaction hash

    txid = transhash.hex()

    return txid
