class BTC:
    def __init__(self, address, amount, txhash):
        self.address = address
        self.amount = amount
        self.txhash = txhash

class ETH:
    def __init__(self, address, amount, txhash):
        self.address = address
        self.amount = amount
        self.txhash = txhash

class BTCError(ValueError):
    pass

class ETHError(ValueError):
    pass

class apiErr(ValueError):
    pass
    
class enetErr(ValueError):
    pass

class bnetErr(ValueError):
    pass