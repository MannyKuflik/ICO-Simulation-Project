from flask import Flask, render_template
from redis import Redis, RedisError
from BTCtrans import BTC_process
from ETHtrans import send_eth
from GenAddrs import full_wallets
import os
import socket  
import random

# Connect to Redis
redis = Redis(host='127.0.0.1', port=6379)

app = Flask(__name__)

def btctrans(dest):
    try: 
        amnt = float(random.randrange(1, 500))/100
        amount = amnt/1000
        #dest = 'mrHXbzTszNWhav7egmfXVktopTBMotS4mp'
        fee = 8000
        tx = BTC_process(dest, '93NUtNNeKfpPZTtB6dEBxjPhBBs8ksYZnHh26RuB8Xe9QUychy6', fee, amnt)
        btcfl = ""
        return tx
    except:
        tx = "unable to make transaction"
        amount = "unable to make transaction"
        dest = "unable to make transaction"
        btcfl = "(Failed)"

def ethtrans(to_address):
    try:
        val = random.randint(10000, 10000000)
        ethamount = val / (10**18)
        from_address = '0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129'
        #to_address = '0x6F544455D57caA0787A5200DA1FC379fc00B5Da5'
        priv_key = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
        ethtx = send_eth(from_address, to_address, val, priv_key)
        ethfl = ''
        return ethtx
    except:
        ethtx = "unable to make transaction"
        val = "unable to make transaction"
        to_address = "unable to make transaction"
        ethfl = "(Failed)"

#@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    try:
        wallets = full_wallets(10, 10)
        btc_addrs = wallets[0]
        eth_addrs = wallets[1]
    except:
        btc_addrs = []
        eth_addrs = []

    btc_trans = []
    eth_trans = []

    for address in btc_addrs:
        trans = btctrans(address)
        btc_trans.append(trans)

    for address in eth_addrs:
        trans = ethtrans(address)
        eth_trans.append(trans)
    
    print(btc_trans)
    print(eth_trans)

    # html = "<b>Redis Visits:</b> {visits}<br/><br/>" \
    #        "<b>Hostname:</b> {hostname}<br/><br/>" \
    #        "<h2><u>BTC Transaction Details</u>{btcfl}</h2><br/>"\
    #        "<b>Destination Address:</b> <details>{dest}</details><br/>" \
    #        "<b>Amount:</b> <details>{amount} BTC</details><br/>" \
    #        "<b>TX:</b> <details>{tx}</details><br/><br/>" \
    #        "<h2><u>ETH Transaction Details</u>{ethfl}</h2><br/>"\
    #        "<b>Destination Address:</b> <details>{to_address}</details><br/>" \
    #        "<b>Amount:</b> <details>{ethamount} ETH</details><br/>" \
    #        "<b>TX:</b> <details>{ethtx}</details><br/><br/>" \
        #    "<h2><u>ETH Wallet Details</u></h2><br/>"\
        #    "<b>Public Key:</b> <details>{pk}</details><br/>" \
        #    "<b>Private Key:</b> <details>{sk}</details><br/>" \
        #    "<b>Address:</b> <details>{ad}</details><br/><br/>" \
        #    "<h2><u>BTC Wallet Details</u></h2><br/>"\
        #    "<b>Public Key:</b> {Bpk}<br/>" \
        #    "<b>Private Key:</b> {Bsk}<br/>" \
        #    "<b>Address:</b> {Badd}<br/><br/>" \
        #    "<b>Visits:</b> {visits}"
    return render_template('home.html',hostname=socket.gethostname(), btcs=btcs, eths=eths, visits=visits, dest=dest, amount=amount, tx=tx, btcfl=btcfl, to_address=to_address, ethamount=ethamount, ethtx=ethtx, ethfl=ethfl)
    # return html.format(hostname=socket.gethostname(), btcs=btcs, eths=eths, visits=visits, dest=dest, amount=amount, tx=tx, btcfl=btcfl, to_address=to_address, ethamount=ethamount, ethtx=ethtx, ethfl=ethfl)
    # pk=pk, ad=ad, sk=sk, Bpk=Bpk, Bsk=Bsk, Badd=Badd,

if __name__ == "__main__":
    hello()
    #app.run(host='0.0.0.0', port=80)