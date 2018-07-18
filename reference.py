from bit.network.services import NetworkAPI, BitpayAPI, InsightAPI
from bit.transaction import calc_txid
from bit import PrivateKeyTestnet
from bit.network.meta import Unspent
import requests
import traceback
from math import log10, floor
from BTCtrans import *

import random 
import time
from models import BTC, ETH

from flask import Flask, render_template, request
from BTCtrans import BTC_process
from ETHtrans import send_eth
from GenAddrs import full_wallets
from web3 import Web3, HTTPProvider, utils
import mysql.connector  

import sha3
from ecdsa import SigningKey, SECP256k1

from concurrent.futures import  ProcessPoolExecutor                                                               

from multiprocessing import Pool, Process

import os
import json
import socket  
import random
import time
from math import log10, floor
from models import BTC, ETH, BTCError, ETHError, apiErr, bnetErr, enetErr


key = PrivateKeyTestnet('92b82iRG1kDJqXgdQx9D1sVskdg5ShXD6f7ggWoP5wLJas65U1j')
url = 'https://testnet.blockexplorer.com/api/addr/' + key.address + '/utxo'
res = requests.get(url)
destination = ['mpqX5Dfy89zLrVFbo6JDkdH4NTcRKbFebK', 'mgYPRGum3A7Rsb2eP93vDGwyWjguRbK4ns']
BTCS = []

# data = {'address': 'mnQCmXfohuwBKjXtSKoHbxcZmQmveCdXtk', 'txid': 'dbbfbf43d47b12913dff041e2770eec236b0aec7ea6df071f4f7a1fe0b1c6526', 'vout': 1, 'scriptPubKey': '76a9144b820d01817f597d072a333776f4d672499ed57388ac', 'amount': 4.59801327, 'satoshis': 459801327, 'confirmations': 0, 'ts': 1531728453}
# v = int(float(data['amount']) * (10**8))
# unspents = [Unspent(v, data['confirmations'], data['scriptPubKey'], data['txid'], data['vout'])]
# print(unspents)
# outputs = []
# for x in destination:
#     amnt = 500
#     # amount = round_sig((amnt/1000), 4) 
#     outputs.append((x, amnt, 'mbtc'))
#     # destsamnts.append((x, amount))

# tx = key.create_transaction(outputs, fee=5, unspents=unspents)
# print(tx)

# # trans = create_transaction(res, destination, destsamnts, key, fee)
# tx = '0100000001c5f4293e60fce5145fb1be9a706e54f16c377a4762741b8c34b9a20ce9b21989010000008a47304402201eec14aee12231bea803a35a3b5a014caa21f2bf537eb7a672c805e7bb4002360220661368ebc8ee47d16aa486f65c09dc68257642cc0705271c3f9845509ac4bcc50141049b3249d74128dd68277a63c11cb09956dcc167904e8a6993779abaa416fbff22f5558d59c17aa836013b8a43c425aacfc19b96011cebc85fd1e7a7a390a23636ffffffff0314000000000000001976a914663bfb4ddb23d714258cf9e7c868da5aade7a31e88ac14000000000000001976a9140b3d83be5c38c473c2aefc14095284d0dc6555f288ac08d3681b000000001976a9144b820d01817f597d072a333776f4d672499ed57388ac00000000'
# # destsamnts = trans[1] 
# url = 'https://testnet.blockexplorer.com/api/tx/send'
# payload = {'rawtx': tx}
# res2 = requests.post(url, data=payload)
# print(res2)

# data = {'address': 'mnQCmXfohuwBKjXtSKoHbxcZmQmveCdXtk', 'txid': 'dbbfbf43d47b12913dff041e2770eec236b0aec7ea6df071f4f7a1fe0b1c6526', 'vout': 1, 'scriptPubKey': '76a9144b820d01817f597d072a333776f4d672499ed57388ac', 'amount': 4.59801327, 'satoshis': 459801327, 'confirmations': 0, 'ts': 1531728453}
# v = int(float(data['amount']) * (10**8))
# unspents = [Unspent(amount=459801327, confirmations=0, script='76a9144b820d01817f597d072a333776f4d672499ed57388ac', txid='dbbfbf43d47b12913dff041e2770eec236b0aec7ea6df071f4f7a1fe0b1c6526', txindex=1)]
# outputs = []
# for x in destination:
#     amnt = 500
#     # amount = round_sig((amnt/1000), 4) 
#     outputs.append((x, amnt, 'mbtc'))
#     # destsamnts.append((x, amount))

# tx = key.create_transaction(outputs, fee=5, unspents=unspents)
# print(tx)

# txid = 'a6ba7075d42e8a3b6f40437c08e6c2480da522725dad4fdc482c5b4f49dfabe6'
# for x in range(len(destination)):
#     BTCS.append(BTC(destsamnts[x][0], destsamnts[x][1], txid))

# for i in range(100):
#     try:
#         s = (Response [200], [('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 2.9e-07), ('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 4.33e-07), ('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 3.53e-07), ('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 2.83e-07), ('mpYCitAEcTYXr6ayqjvioxFngBW8MhM48U', 1.94e-07)], True)

#         res2 = s[0]
#         print(res2.ok)
#         destsamnts = s[1]
#         if s[2]:
#             # if res2.ok:
#             success_broadcast(res2, destination, BTCS, destsamnts)
#             break
#             # else:
#             #     print('failed to broadcast, restarting...')
#             #     if failed_broadcast(i, destination, BTCS):
#             #         break
#         else:
#             print('failed to get unspents, restarting...')
#             if failed_broadcast(i, destination, BTCS):
#                 break
#     except:
#         print('error, restarting...')
#         if failed_broadcast(i, destination, BTCS):
#             break
# print(BTCS)

keccak = sha3.keccak_256()
private = SigningKey.from_string(bytes().fromhex('3287c305f2036501677331d11871fddfa4bda29cb6e0938a6b05b2ad0144106a'), curve=SECP256k1)
public = private.get_verifying_key().to_string()
keccak.update(public)
address = "0x{}".format(keccak.hexdigest()[24:])
x = Web3.toChecksumAddress(address)