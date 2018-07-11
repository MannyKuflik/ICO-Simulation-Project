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
    
    for i in range(100):
        try:
            url = 'https://testnet.blockexplorer.com/api/addr/' + key.address + '/utxo'
            res = requests.get(url)
            if res.ok:
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
                # print('transaction created')
                url = 'https://testnet.blockexplorer.com/api/tx/send'
                payload = {'rawtx': tx}
                res = requests.post(url, data=payload)
 
                if res.ok:
                    txid = res.json()['txid']
                    for x in range(len(destination)):
                        BTCS.append(BTC(destsamnts[x][0], destsamnts[x][1], txid))
                    # print("broadcast success")
                    break
                else:
                    print('failed to broadcast, restarting...')
                    time.sleep(2)
                    if i > 10:
                        for x in range(len(destination)):
                            BTCS.append(BTC('Fail', 'N/A', 'Fail'))
                        break
            else:
                print('failed to get unspents, restarting...')
                time.sleep(2)
                if i > 10:
                    for x in range(len(destination)):
                        BTCS.append(BTC('Fail', 'N/A', 'Fail'))
                    break
        except:
            print('error, restarting...')
            time.sleep(2)
            if i > 10:
                for x in range(len(destination)):
                    BTCS.append(BTC('Fail', 'N/A', 'Fail'))
                break
    return BTCS
