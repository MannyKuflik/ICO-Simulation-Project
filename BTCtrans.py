from bit.network.services import NetworkAPI, BitpayAPI, InsightAPI
from bit.transaction import calc_txid
from bit import PrivateKeyTestnet
from bit.network.meta import Unspent
import requests
import traceback

import random 
import time

ntwrk = NetworkAPI()

# def BTC_process(destination, priv_wif, fee, amnt):
#     tx = None
#     key = None
#     outputs = None
#     url = None
#     payload = None
#     res = None
#     txid = None

#     s = requests.Session()
#     a = requests.adapters.HTTPAdapter(max_retries=100, pool_connections = 100, pool_maxsize = 1000)
#     s.mount('https://', a)

#     key = PrivateKeyTestnet(priv_wif)
#     try:

#         url = 'https://testnet.blockexplorer.com/api/addr/' + key.address + '/utxo'

#         for i in range(100):
#             res = s.get(url)
#             if True:
#                 print('Unspents success')
#                 data2 = res.json()[0]
#                 v = int(float(data2['amount']) * (10**8))
#                 unspents = [Unspent(v, data2['confirmations'], data2['scriptPubKey'], data2['txid'], data2['vout'])]
#                 break  
#             else:
#                 # print('trying chain.so')
#                 url = 'https://chain.so/api/v2/get_tx_unspent/BTCTEST/' + key.address
#                 try:
#                     res = s.get(url)
#                     if res.ok:
#                         data = res.json()["data"]
#                         txs = data['txs'][0]
#                         v = int(float(txs['value']) * (10**8))  
#                         unspents = [Unspent(v, txs['confirmations'], txs['script_hex'], txs['txid'], txs['output_no'])] 
#                         print('chain.so unspents success')
#                         break
#                     else:
#                         print("couldn't get unspents, retrying...")
#                 except:
#                     print("u error")
#                 #         print('trying bit')
#                 #         try:
#                 #             unspents = key.get_unspents()
#                 #             print('bit unspents success')
#                 #             break
#                 #         except:
#                 #             print("couldn't get unspents, retrying...")
#                 time.sleep(5)
#     except:
#         print('Line 41, error getting unspents')
#         traceback.print_exc()
        
#     outputs = [(destination, amnt, 'mbtc')]

#     try:
#         tx = key.create_transaction(outputs, fee=fee, unspents=unspents)
#     except:
#         print("Line 55, error creating transaction")
#         traceback.print_exc()

#     url = 'https://testnet.blockexplorer.com/api/tx/send'

#     try:
#         for i in range(100):


#             payload = {'rawtx': tx}
#             res3 = s.post(url, data=payload)
#             if True:
#                 txid = res3.json()['txid']
#                 print("broadcast success")
#                 break
#             else:
#                 print('trying chain.so')
#                 url = 'https://chain.so/api/v2/send_tx/BTCTEST'
#                 try:
#                     payload = {'network': 'BTCTEST', 'tx_hex': tx}
#                     res = s.post(url, data=payload)
#                     if res.ok:
#                         print('broadcast chain.so success')
#                         info = res.json()["data"]
#                         txid = info["txid"]
#                         break
#                     else:
#                         print("couldn't broadcast, retrying...")
#                 except:
#                     print("b error")
#                 #     else:
#                 #         print('trying bit')
#                 #         try:
#                 #             ntwrk.broadcast_tx_testnet(tx)
#                 #             txid = calc_txid(tx)
#                 #             print('broadcast bit success')
#                 #             break
#                 #         except:
#                     print("couldn't broadcast, retrying...")
#                     time.sleep(5)
#     except:
#         print("Line 118, error broadcasting")
#         traceback.print_exc()
#     return txid


def BTC_process(destination, priv_wif, fee, amnt):
    tx = None
    key = None
    outputs = None
    url = None
    payload = None
    res = None
    txid = None

    # s = requests.Session()
    # a = requests.adapters.HTTPAdapter(max_retries=100, pool_connections = 100, pool_maxsize = 1000)
    # s.mount('https://', a)
    key = PrivateKeyTestnet(priv_wif)
    
    for i in range(100):
        try:
            url = 'https://testnet.blockexplorer.com/api/addr/' + key.address + '/utxo'
            res = requests.get(url)
            if res.ok:
                print('Unspents success')
                data = res.json()[0]
                v = int(float(data['amount']) * (10**8))
                unspents = [Unspent(v, data['confirmations'], data['scriptPubKey'], data['txid'], data['vout'])]
                outputs = [(destination, amnt, 'mbtc')]
                tx = key.create_transaction(outputs, fee=fee, unspents=unspents)
                print('transaction created')
                url = 'https://testnet.blockexplorer.com/api/tx/send'
                payload = {'rawtx': tx}
                res = requests.post(url, data=payload)

                if res.ok:
                    txid = res.json()['txid']
                    print("broadcast success")
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






#~~~~~~~ORIGINAL CODE~~~~~~~~~~~
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
 
#~~~~~~~~~~~~~BTC_PROCESSS V2~~~~~~~~~~~~~~~~~~
    # unspents = key.get_unspents()
    # org = key.address
    # unspents = ntwrk.get_unspent_testnet(org)
    # f = fee
    # dest = destination
    # outputs = [(dest, amnt, 'mbtc')]
    # txid = key.send(outputs, fee=f, unspents=unspents)
    # return txid

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