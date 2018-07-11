from bit.network.services import NetworkAPI, BitpayAPI, InsightAPI
from bit.transaction import calc_txid
from bit import PrivateKeyTestnet
from bit.network.meta import Unspent
import requests
import traceback

import random 
import time

ntwrk = NetworkAPI()

def BTC_process(destination, priv_wif, fee, amnt):
    tx = None
    key = None
    outputs = None
    url = None
    payload = None
    res = None
    txid = None

    key = PrivateKeyTestnet(priv_wif)
    
    for i in range(100):
        try:
            url = 'https://testnet.blockexplorer.com/api/addr/' + key.address + '/utxo'
            res = requests.get(url)
            if res.ok:
                data = res.json()[0]
                v = int(float(data['amount']) * (10**8))
                unspents = [Unspent(v, data['confirmations'], data['scriptPubKey'], data['txid'], data['vout'])]
                outputs = [(destination, amnt, 'mbtc')]
                tx = key.create_transaction(outputs, fee=fee, unspents=unspents)
                url = 'https://testnet.blockexplorer.com/api/tx/send'
                payload = {'rawtx': tx}
                res = requests.post(url, data=payload)
 
                if res.ok:
                    txid = res.json()['txid']
                    break
                else:
                    print('failed to broadcast, restarting...')
                    time.sleep(2)
                    if i > 1:
                        txid = 'fail'
                        break
            else:
                print('failed to get unspents, restarting...')
                time.sleep(2)
                if i > 1:
                    txid = 'fail'
                    break
        except:
            print('error, restarting...')
            time.sleep(2)
            if i > 1:
                txid = 'fail'
                break
    return txid
