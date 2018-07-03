import eth_utils
from pycoin.key.BIP32Node import BIP32Node
from tqdm import tqdm

class TransactionFactory:
    def __init__(self, xpub):
        self.xpub = xpub
        node = BIP32Node.from_hwif(xpub)
        self.wallet_eth = node.subkey(0)

    def getETHAddr(self, index):
        new_node = self.wallet_eth.subkey(index)
        sec = new_node.sec(use_uncompressed=True)
        address = eth_utils.keccak(sec[1:]).hex()[24:]
        address = "0x" + address
        checksum_address = eth_utils.to_checksum_address(address)
        return checksum_address

def gen_btc(index):
    new_node = wallet_btc.subkey(index)
    address = new_node.address()
    return address

XPUB_btc = "tpubDAQgEY88bKm3x6MgnNeZbGqhS1D2ZsvZrG5MMnyVw9aXvWjq4oLiGSH2XXKXUq4YVtunYAiqkM2rKwRY9aU2Nin2Hf2pHco2rRuVXfkM93J"

wallet_account0_btc = BIP32Node.from_hwif(XPUB_btc)
wallet_btc = wallet_account0_btc.subkey(0)

def full_wallets(eth_num, btc_num):
    xpub_eth = 'xpub6EPXZc2brBKKFUNH3bxcg17g5mi5Uo5YmHHe2j1dWqqzV5WEN8dQYWXSvFpXz1PNrW9G8de6qoPun3Eiz4qKmaLXmViVYEHmrXRF6JbQXUE'
    Factory = TransactionFactory(xpub_eth)
    v1 = eth_num
    eth_addrs = []
    for i in range(0,v1):
        address = address = Factory.getETHAddr(i)
        eth_addrs.append(address)
    print('got dat Eth boy')
    print(eth_addrs)
# index_btc = 0
    v2 = btc_num
    btc_addrs = []
    for i in range(0,v2):
        btc_addrs.append(gen_btc(i))
    print("Serving up some BTC B-style brovis")
    print(btc_addrs)

    return (btc_addrs, eth_addrs)

full_wallets(50, 50)

