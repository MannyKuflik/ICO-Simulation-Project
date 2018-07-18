import pytest
from unittest import TestCase
from unittest.mock import patch
import BTCtrans
# from BTCtrans import round_sig, create_transaction, failed_broadcast

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

#bitcoin variables
key = PrivateKeyTestnet('92b82iRG1kDJqXgdQx9D1sVskdg5ShXD6f7ggWoP5wLJas65U1j')
url = 'https://testnet.blockexplorer.com/api/addr/' + key.address + '/utxo'
res = requests.get(url)
destination = ['mpqX5Dfy89zLrVFbo6JDkdH4NTcRKbFebK', 'mgYPRGum3A7Rsb2eP93vDGwyWjguRbK4ns']
destsamnts = []
BTCS = []
fee = 5

def mock_create_transaction(destination, destsamnts, key, fee=5):
    data = {'address': 'mnQCmXfohuwBKjXtSKoHbxcZmQmveCdXtk', 'txid': 'dbbfbf43d47b12913dff041e2770eec236b0aec7ea6df071f4f7a1fe0b1c6526', 'vout': 1, 'scriptPubKey': '76a9144b820d01817f597d072a333776f4d672499ed57388ac', 'amount': 4.59801327, 'satoshis': 459801327, 'confirmations': 0, 'ts': 1531728453}
    v = int(float(data['amount']) * (10**8))
    unspents = [Unspent(v, data['confirmations'], data['scriptPubKey'], data['txid'], data['vout'])]
    outputs = []
    for x in destination:
        amnt = 500
        amount = BTCtrans.round_sig((amnt/1000), 4) 
        outputs.append((x, amnt, 'mbtc'))
        destsamnts.append((x, amount))

    tx = key.create_transaction(outputs, fee=fee, unspents=unspents)
    return tx

class TestBitcoin(TestCase):

    def test_round_sig():
        assert BTCtrans.round_sig(1234560, 4) == 1235000
        assert BTCtrans.round_sig(0.000456, 2) == 0.00046

    def test_create_transaction():
        assert mock_create_transaction(destination, destsamnts, key, fee=5) == '010000000126651c0bfea1f7f471f06deac7aeb036c2ee70271e04ff3d91127bd443bfbfdb010000008b48304502210086b9842ccb485378f3ef7a0627e8cbde4c2100258f6d677ef5b96259f467be2c022048c341b2d158ab61ef08ed62ca9a04f204b76cd4c07dbff898e1ae2792cf804e0141049b3249d74128dd68277a63c11cb09956dcc167904e8a6993779abaa416fbff22f5558d59c17aa836013b8a43c425aacfc19b96011cebc85fd1e7a7a390a23636ffffffff0380f0fa02000000001976a914663bfb4ddb23d714258cf9e7c868da5aade7a31e88ac80f0fa02000000001976a9140b3d83be5c38c473c2aefc14095284d0dc6555f288ac3b1c7215000000001976a9144b820d01817f597d072a333776f4d672499ed57388ac00000000'

    # def test_success_broadcast():
    #     BTCS = []
    #     txid = 'a6ba7075d42e8a3b6f40437c08e6c2480da522725dad4fdc482c5b4f49dfabe6'
    #     for x in range(len(destination)):
    #         BTCS.append(BTC(destsamnts[x][0], destsamnts[x][1], txid))
    #     assert BTCS[-1].txid == 'a6ba7075d42e8a3b6f40437c08e6c2480da522725dad4fdc482c5b4f49dfabe6'

    def test_failed_broadcast():
        assert BTCtrans.failed_broadcast(11, ['mpqX5Dfy89zLrVFbo6JDkdH4NTcRKbFebK', 'mgYPRGum3A7Rsb2eP93vDGwyWjguRbK4ns'], [])
    
    @patch('BTCtrans.broadcast')
    def test_addtoBTCS(self, mock_broadcast):
        mock_broadcast.return_value = 12 #(<Response [200]>, [('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 2.9e-07), ('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 4.33e-07), ('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 3.53e-07), ('mzrhmQRGKMCgx3o1PYY4DcHW5FgZPFZk9N', 2.83e-07), ('mpYCitAEcTYXr6ayqjvioxFngBW8MhM48U', 1.94e-07)], True)
        x = BTCtrans.addtoBTCS
        print(x)

if __name__ == "__main__":
    # TestBitcoin.test_round_sig()
    # TestBitcoin.test_create_transaction()
    # TestBitcoin.test_failed_broadcast()
    TestBitcoin.test_addtoBTCS()
