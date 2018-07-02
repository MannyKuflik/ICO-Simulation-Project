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

xpub = 'xpub....'
Factory = TransactionFactory(xpub)

for i in range(0,5000):
    address =  address = Factory.getETHAddr(i)
    print(address)




XPUB_btc = "xpub...."

# index_btc = 0
wallet_account0_btc = BIP32Node.from_hwif(XPUB_btc)
wallet_btc = wallet_account0_btc.subkey(0)

def gen_btc(index):
    new_node = wallet_btc.subkey(index)
    address = new_node.address()
    return address

for i in range(0,5000):
    address = gen_btc(i)
    print(address)