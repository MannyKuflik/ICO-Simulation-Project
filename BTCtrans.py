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

#~~~~~~~~MULTIPLE OUTPUTS TEST~~~~~~~~~
# dests = ['n2f8do8bCGtgQgkCv43efBsnvjV181x6a4','n2f8do8bCGtgQgkCv43efBsnvjV181x6a4','mgDryTfWY7PBBV1DH8vkFr2KHMHduwzct4']
# print(BTC_process(dests, '93NUtNNeKfpPZTtB6dEBxjPhBBs8ksYZnHh26RuB8Xe9QUychy6', 5))

#~~~~~~~~ORIGINAL CODE~~~~~~~~~
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

#~~~~~~~~~~~~~~FAUCET FILLING SCRIPT~~~~~~~~~~~~~~~~~~
# dest = 'mooc3xfCXBEkkcnpTJfSiD66PghEJ2moG4'
# priv = '93CvyqZUTsVtNeWLfne7ZbpnG5npHXrabHL3ifmPPXvCjW5DxV4'
# fee = 5000
# num = 50000
# BTC_process(dest, priv, fee, num)
# print("Done")

# def get_unspent_testnet(cls, address)
# def broadcast_tx_testnet(cls, tx_hex)
# def create_transaction or send(self, outputs, fee=None, leftover=None, combine=True, message=None, unspents=None):