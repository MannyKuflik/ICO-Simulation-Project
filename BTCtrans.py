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

def round_sig(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def send_transaction(res, destination, key, destsamnts, fee):
    trans = create_transaction(res, destination, destsamnts, key, fee)
    tx = trans[0]
    destsamnts = trans[1] 
    url = 'https://testnet.blockexplorer.com/api/tx/send'
    payload = {'rawtx': tx}
    res2 = requests.post(url, data=payload)
    print(res2)
    return (res2, destsamnts)

def create_transaction(res, destination, destsamnts, key, fee):
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
    return (tx, destsamnts)

def broadcast(destination, key, destsamnts, fee):
    url = 'https://testnet.blockexplorer.com/api/addr/' + key.address + '/utxo'
    res = requests.get(url)
    if res.ok:
        s = send_transaction(res, destination, key, destsamnts, fee)
        res2 = s[0]
        destsamnts = s[1]
        return (res2, destsamnts, True)

def success_broadcast(res2, destination, BTCS, destsamnts):
    txid = res2.json()['txid']
    for x in range(len(destination)):
        BTCS.append(BTC(destsamnts[x][0], destsamnts[x][1], txid))

def failed_broadcast(i, destination, BTCS):
    time.sleep(2)
    if i > 10:
        for x in range(len(destination)):
            BTCS.append(BTC('Fail', 'N/A', 'Fail'))
        return True

def addtoBTCS(destination, key, destsamnts, fee, BTCS):    
    for i in range(100):
        try:
            s = broadcast(destination, key, destsamnts, fee)
            res2 = s[0]
            destsamnts = s[1]
            if s[2]:
                if res2.ok:
                    success_broadcast(res2, destination, BTCS, destsamnts)
                    break
                else:
                    print('failed to broadcast, restarting...')
                    if failed_broadcast(i, destination, BTCS):
                        break
            else:
                print('failed to get unspents, restarting...')
                if failed_broadcast(i, destination, BTCS):
                    break
        except:
            print('error, restarting...')
            if failed_broadcast(i, destination, BTCS):
                break
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
    BTCS = addtoBTCS(destination, key, destsamnts, fee, BTCS)
    return BTCS
