from flask import Flask, render_template
from BTCtrans import BTC_process
from ETHtrans import send_eth
from GenAddrs import full_wallets
from web3 import Web3, HTTPProvider, utils
import os
import json
import socket  
import random
import mysql.connector
import time
from math import log10, floor
from models import BTC, ETH

from web3 import Web3, HTTPProvider, utils


app = Flask(__name__)

def round_sig(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)
    
def btctrans(dest, priv):
    try: 
        amnt = float(random.randrange(1, 500))/1000000
        #dest = 'mrHXbzTszNWhav7egmfXVktopTBMotS4mp'
        amount = round_sig((amnt/1000), 4) 
        fee = 5
        tx = BTC_process(destination=dest, priv_wif=priv, fee=fee, amnt=amnt) 
        txhash=tx[0] 
        bit = BTC(dest, amount, txhash)
        return bit
    except:
        print('failed attempt')
        btctrans(dest, priv)
    
        # tx = "unable to make transaction"
        # amount = "N/A"
        # dest = "unable to make transaction"
        # btcfl = "(Failed)"
        # raise
        # raise
        # return BTC('fail', 'N/A', 'fail')

def ethtrans(to_address, nonce):
    try:
        val = random.randint(10000, 10000000)
        ethamount = round_sig((val / (10**18)), 4)
        from_address = '0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129'
        #to_address = '0x6F544455D57caA0787A5200DA1FC379fc00B5Da5'
        priv_key = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
        ethtx = send_eth(from_address, to_address, val, priv_key, nonce)
        return ETH(to_address, ethamount, ethtx)
    except:
        print('failed attempt')
        ethtrans(to_address, nonce) 
        # ethtx = "unable to make transaction"
        # val = "unable to make transaction"
        # to_address = "unable to make transaction"
        # ethfl = "(Failed)"
        # raise
        # return ETH('fail', 'N/A', 'fail')

@app.route("/")
def hello():
    # try:
    #     visits = redis.incr("counter")
    # except RedisError:
    #     visits = "<i>cannot connect to Redis, counter disabled</i>"
    try:
        web3 = Web3(HTTPProvider('https://rinkeby.infura.io/UVgPTn3TgFMB0KhHUlif'))
        nonce = web3.eth.getTransactionCount('0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129') 
        bcnt = 0
        btc_privs = ['92b82iRG1kDJqXgdQx9D1sVskdg5ShXD6f7ggWoP5wLJas65U1j','93S6gfCcC9KeAJnH4Cihm1ohn6MoY5kW5JDBt9Jwg6DS6Y2WBii','92j5cnHrUQfehM8RE7mNwqFquPipj1ixvv6aTk1eDfcEvGQvhN7','92fxKDXkF97ku9PaSEcz3vKmyeTc9gQZCHFrGJVFGGJ5LkpSxQM',
        '93GtNodSaZEu3KzcvP7r5MnP2yU4GnC4WJRhxYAvmW8sroU7TLW', '93W3HKzWurB7a8YuBvfPXf2hTWipGWKCjrTkDPHKkk8T7jHZ2pf','92csoy33Do1Bzj91T74Bb7kPLUYUTRJDSSGwj1JyWUmUETiCYJy', '92woUn35UNvzhCtj6Kp3koNy9Gct92MksEQ43Bsc26TSxnT7FSd',
        '92jX4Yp7XmFNPpEkcTmQCygzdTGy5szu2Dcq8heocqynjZW9PyN', '93RfEtgM8njvTqfwfrigVsNZ42ofBDUZyzgwDBfnGuqtHHXNd9f']
        count = 0
        wallets = full_wallets(25, 25)
        btcs = wallets[0]
        eths = wallets[1]
        ethfl = ""
        btcfl = ""
    except:
        btcs = []
        eths = []

    print(btcs)
    print(eths)
    btc_trans = []
    eth_trans = []

    for address in eths:
        trans = ethtrans(address, nonce + count)
        eth_trans.append(trans)
        count = count+1
        print(count)

    print(eth_trans)


    for address in btcs:
        trans = btctrans(address, btc_privs[bcnt % 10])
        if trans is not None: btc_trans.append(trans)
        else: btctrans(address, btc_privs[bcnt % 10])
        bcnt = bcnt + 1
        print(bcnt)
    
    print(btc_trans)

    config = {
            'user': 'root',
            'password': 'HorcruX8!',
            'host': 'localhost',
            'port': '3306',
            'database': 'BROVIS'
        }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    for trans in btc_trans:
        cursor.execute("INSERT INTO bitcoin "
                   "(address, amount, txhash) "
                   "VALUES ('%s', '%s', '%s') " % (trans.address, trans.amount, trans.txhash)
                   )
        connection.commit()
    for trans in eth_trans:
        cursor.execute("INSERT INTO ethereum "
                   "(address, amount, txhash) "
                   "VALUES ('%s', '%s', '%s') " % (trans.address, trans.amount, trans.txhash)
                   )
        connection.commit()
    # cursor.execute('SELECT address, amount, txhash FROM bitcoin')
    # cursor.execute('SELECT address, amount, txhash FROM ethereum')
    # results = [[address, amount, txhash] for (address, amount, txhash) in cursor]
    cursor.close()
    connection.close()

    #data = 'Hello World'
    #return json.dumps({'data': connect()})

    return render_template('home.html', hostname=socket.gethostname(), btcs=btcs, eths=eths, btc_trans=btc_trans, eth_trans=eth_trans, btcfl=btcfl, ethfl=ethfl)
    # return html.format(hostname=socket.gethostname(), btcs=btcs, eths=eths, visits=visits, dest=dest, amount=amount, tx=tx, btcfl=btcfl, to_address=to_address, ethamount=ethamount, ethtx=ethtx, ethfl=ethfl)
    # pk=pk, ad=ad, sk=sk, Bpk=Bpk, Bsk=Bsk, Badd=Badd,
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80)