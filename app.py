from flask import Flask
from redis import Redis, RedisError
from ETHgen import sk, pk, ad 
from BTCtrans import BTC_process
from GenAddrs import full_wallets
import os
import socket  
import random

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello(): 
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    try:
        wallets = full_wallets(50, 75)
        btc_addrs = wallets[0]
        eth_addrs = wallets[1]
    except:
        btc_addrs = []
        eth_addrs = []

    try: 
        amnt = float(random.randrange(1, 500))/100
        amount = amnt
        dest = 'mrHXbzTszNWhav7egmfXVktopTBMotS4mp'
        fee = 8000
        tx = BTC_process(destination=dest, priv_wif='93NUtNNeKfpPZTtB6dEBxjPhBBs8ksYZnHh26RuB8Xe9QUychy6', fee=fee)
        fl = ""
    except:
        tx = "unable to make transaction"
        amount = "unable to make transaction"
        dest = "unable to make transaction"
        fl = "(Failed)"

    html = "<b>Hostname:</b> {hostname}<br/><br/>" \
           "<h2><u>ETH Wallet Details</u></h2><br/>"\
           "<b>Public Key:</b> <details>{pk}</details><br/>" \
           "<b>Private Key:</b> <details>{sk}</details><br/>" \
           "<b>Address:</b> <details>{ad}</details><br/><br/>" \
           "<h2><u>BTC Transaction Details</u>{fl}</h2><br/>"\
           "<b>Destination Address:</b> <details>{dest}</details><br/>" \
           "<b>Amount:</b> <details>{amount} mbtc</details><br/>" \
           "<b>TX:</b> <details>{tx}</details><br/><br/>" \
        #    "<h2><u>BTC Wallet Details</u></h2><br/>"\
        #    "<b>Public Key:</b> {Bpk}<br/>" \
        #    "<b>Private Key:</b> {Bsk}<br/>" \
        #    "<b>Address:</b> {Badd}<br/><br/>" \
        #    "<b>Visits:</b> {visits}"
    return html.format(pk=pk, ad=ad, sk=sk, hostname=socket.gethostname(), visits=visits, dest=dest, amount=amount, tx=tx, fl=fl)
    #Bpk=Bpk, Bsk=Bsk, Badd=Badd,

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)