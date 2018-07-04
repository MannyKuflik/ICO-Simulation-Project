from flask import Flask, render_template
from redis import Redis, RedisError
from BTCtrans import BTC_process
from ETHtrans import send_eth
# from GenAddrs import full_wallets
import os
import socket  
import random

# Connect to Redis
redis = Redis(host="redis", port=6379)

app = Flask(__name__)

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
        amount = amnt/1000
        dest = 'mrHXbzTszNWhav7egmfXVktopTBMotS4mp'
        fee = 8000
        tx = BTC_process(destination=dest, priv_wif='93NUtNNeKfpPZTtB6dEBxjPhBBs8ksYZnHh26RuB8Xe9QUychy6', fee=fee)
        btcfl = ""
    except:
        tx = "unable to make transaction"
        amount = "unable to make transaction"
        dest = "unable to make transaction"
        btcfl = "(Failed)"

    try:
        val = random.randint(10000, 10000000)
        ethamount = val / (10**18)
        from_address = '0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129'
        to_address = '0x6F544455D57caA0787A5200DA1FC379fc00B5Da5'
        priv_key = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
        ethtx = send_eth(from_address, to_address, val, priv_key)
        ethfl = ''
    except:
        ethtx = "unable to make transaction"
        val = "unable to make transaction"
        to_address = "unable to make transaction"
        ethfl = "(Failed)"

    html = "<b>BTC Wallets:</b> {btcs}<br/><br/>" \
           "<b>ETH Wallets:</b> {eths}<br/><br/>" \
           "<b>Hostname:</b> {hostname}<br/><br/>" \
           "<h2><u>BTC Transaction Details</u>{btcfl}</h2><br/>"\
           "<table><tr><th>Address</th><th>Amount</th><th>TX</th></tr><tr><td>{dest}</td><td>{amount}</td><td>{tx}</td></tr></table>"\
           "<b>Destination Address:</b> <details>{dest}</details><br/>" \
           "<b>Amount:</b> <details>{amount} BTC</details><br/>" \
           "<b>TX:</b> <details>{tx}</details><br/><br/>" \
           "<h2><u>ETH Transaction Details</u>{ethfl}</h2><br/>"\
           "<b>Destination Address:</b> <details>{to_address}</details><br/>" \
           "<b>Amount:</b> <details>{ethamount} ETH</details><br/>" \
           "<b>TX:</b> <details>{ethtx}</details><br/><br/>" \
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
    app.run(host='0.0.0.0', port=80)