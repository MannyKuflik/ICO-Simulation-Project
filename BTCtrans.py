from bit.network.services import NetworkAPI, BitpayAPI, InsightAPI
from bit.transaction import calc_txid
from bit import PrivateKeyTestnet
from bit.network.meta import Unspent
import requests
import traceback
from math import log10, floor

import random 
import time
from models import BTC, ETH

# s = requests.Session()
# a = requests.adapters.HTTPAdapter(max_retries=100, pool_connections = 100, pool_maxsize = 1000)
# s.mount('https://', a)

def round_sig(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)


def get_something(key, retry=100):
    try:
        url = 'https://testnet.blockexplorer.com/api/addr/' + key.address + '/utxo'
        res = requests.get(url)
        if res.ok:
            return res
        raise Exception() 
    except:
        print('failed to get unspents, restarting...')
        time.sleep(2)
        if retry != 0:
            return get_something(key, retry=100)
        retry -=  1


def get_something2(tx, retry=100):
    url = 'https://testnet.blockexplorer.com/api/tx/send'
    payload = {'rawtx': tx}
    try:
        res = requests.post(url, data=payload)
        if res.ok:
            return res
        raise Exception()
    except:
        print('failed to broadcast, restarting...')
        time.sleep(2)
        if retry != 0:
            return get_something2(tx, retry=100)
        retry -=  1

def get_something3(destination, key):
    res = {get_something(key, retry=100)}

    # print('Unspents success')
    data = res.json()[0]
    v = int(float(data['amount']) * (10**8))
    unspents = [Unspent(v, data['confirmations'], data['scriptPubKey'], data['txid'], data['vout'])]
    outputs = []
    for x in destination:
        amnt = float(random.randrange(1, 500))/1000000
        amount = round_sig((amnt/1000), 4) 
        outputs.append((x, amnt, 'mbtc'))
        destsamnts.append((x, amount)) 
    tx = key.create_transaction(outputs, fee=fee, unspents=unspents)
    return tx


def get_something4(tx):
    res2 = res = get_something2(tx)
    txid = res.json()['txid']
    for x in range(len(destination)):
        BTCS.append(BTC(destsamnts[x][0], destsamnts[x][1], txid))
    return BTCS

def BTC_process(destination, priv_wif, fee):
    tx = None
    key = None
    outputs = None
    url = None
    payload = None
    res = None
    txid = None
    destsamnts = [] 
    BTCS = []

    key = PrivateKeyTestnet(priv_wif)
    
    tx = get_something3(destination, key)
    # print('transaction created')

    
    BTCS = get_something4(tx)
    # print("broadcast success")

    return BTCS
