import eth_utils
from pycoin.key.BIP32Node import BIP32Node
import time
from models import BTCError, ETHError

def getETHAddr(index, wallet_eth):
    new_node = wallet_eth.subkey(index)
    sec = new_node.sec(use_uncompressed=True)
    address = eth_utils.keccak(sec[1:]).hex()[24:]
    address = "0x" + address
    checksum_address = eth_utils.to_checksum_address(address)
    return checksum_address

def gen_btc(index, wallet_btc):
    new_node = wallet_btc.subkey(index)
    address = new_node.address()
    return address

# xpub_btc = "tpubDAK3K7sXsKqVs6XNCnBUZQVj2Yy5Sc98XV4Sy9xVfTcaGv8AGm4x585DUYpbBx61zURUoyFsJWAokuZY8Edm5PqJ9wza7i4pxVPKCttKjZH"
# xpub_eth = 'xpub6EPXZc2brBKKFUNH3bxcg17g5mi5Uo5YmHHe2j1dWqqzV5WEN8dQYWXSvFpXz1PNrW9G8de6qoPun3Eiz4qKmaLXmViVYEHmrXRF6JbQXUE'


# def full_wallets(btc_num, eth_num, xpub_eth):
#     Factory = TransactionFactory(xpub_eth)
#     v1 = eth_num
#     eth_addrs = []
#     for i in range(0,v1):
#         address = address = Factory.getETHAddr(i)
#         eth_addrs.append(address)
#     print('got dat Eth boy')
# # index_btc = 0
#     v2 = btc_num
#     btc_addrs = []
#     for i in range(0,v2):
#         btc_addrs.append(gen_btc(i))
#     print("Serving up some BTC B-style brovis")

#     return (btc_addrs, eth_addrs)

def full_wallets(btc_num, eth_num, xpub_btc, xpub_eth):
    try: 
        wallet_account0_btc = BIP32Node.from_hwif(xpub_btc)
        wallet_btc = wallet_account0_btc.subkey(0)
    except:
        print('invalid btc xpub')
        raise BTCError
        # return
    try: 
        node = BIP32Node.from_hwif(xpub_eth)
        wallet_eth = node.subkey(0)
    except: 
        print('invalid eth xpub')
        raise ETHError
        # return

    eth_addrs = []
    btc_addrs = []
    for i in range(eth_num):
        eth_addrs.append(getETHAddr(i, wallet_eth))
    print('got dat Eth boy')    
    for i in range(btc_num):
        btc_addrs.append(gen_btc(i, wallet_btc))
    print("Serving up some BTC B-style brovis")
    return (btc_addrs, eth_addrs)
