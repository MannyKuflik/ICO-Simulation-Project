from flask import Flask, render_template
from redis import Redis, RedisError
from BTCtrans import BTC_process
from ETHtrans import send_eth
# from GenAddrs import full_wallets
import os
import socket  
import random
from math import log10, floor

# Connect to Redis
redis = Redis(host="redis", port=6379)

app = Flask(__name__)

def round_sig(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)

@app.route("/")
def hello(): 

    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"
    try:
        #wallets = full_wallets(3, 3)
        btcs = []#wallets[0]
        eths = []#wallets[1]
    except:
        btcs = []
        eths = []

    try: 
        amnt = float(random.randrange(1, 500))/100
        amount = round_sig((amnt/1000), 4) 
        dest = 'mrHXbzTszNWhav7egmfXVktopTBMotS4mp'
        fee = 8000
        tx = BTC_process(destination=dest, priv_wif='93NUtNNeKfpPZTtB6dEBxjPhBBs8ksYZnHh26RuB8Xe9QUychy6', fee=fee)
        btx = tx[0]
        btcfl = ""
    except:
        tx = "unable to make transaction"
        amount = "N/A"
        dest = "unable to make transaction"
        btcfl = "(Failed)"

    try:
        val = random.randint(10000, 10000000)
        ethamount = round_sig((val / (10**18)), 4)
        from_address = '0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129'
        to_address = '0x6F544455D57caA0787A5200DA1FC379fc00B5Da5'
        priv_key = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
        ethtx = '0x33ac3ff5141e01cedef866e7fb64152c978e0a7a2eff0f6d8105f3b21bc3fe45'#send_eth(from_address, to_address, val, priv_key)
        ethfl = ''
    except:
        ethtx = "unable to make transaction"
        val = "unable to make transaction"
        to_address = "unable to make transaction"
        ethfl = "(Failed)"


#Testing
    class Row:
        def __init__(self, address, amount, txhash):
            self.address = address
            self.amount = amount
            self.txhash = txhash
    

    return render_template('home.html',arr=arr, hostname=socket.gethostname(), btcs=btcs, eths=eths, visits=visits, dest=dest, amount=amount, tx=btx, btcfl=btcfl, to_address=to_address, ethamount=ethamount, ethtx=ethtx, ethfl=ethfl)
    # return html.format(hostname=socket.gethostname(), btcs=btcs, eths=eths, visits=visits, dest=dest, amount=amount, tx=tx, btcfl=btcfl, to_address=to_address, ethamount=ethamount, ethtx=ethtx, ethfl=ethfl)
    # pk=pk, ad=ad, sk=sk, Bpk=Bpk, Bsk=Bsk, Badd=Badd,

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)