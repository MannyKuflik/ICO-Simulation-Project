from flask import Flask, render_template
from BTCtrans import BTC_process
from ETHtrans import send_eth
from GenAddrs import full_wallets, xpub_eth, XPUB_btc
from web3 import Web3, HTTPProvider, utils
import mysql.connector  
from concurrent.futures import  ProcessPoolExecutor                                                               

from multiprocessing import Pool, Process

import os
import json
import socket  
import random
import time
from math import log10, floor
from models import BTC, ETH



app = Flask(__name__)                                                                                                  

def round_sig(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def btctrans(dest, priv):
    try: 
        fee = 5
        BTCS = BTC_process(destination=dest, priv_wif=priv, fee=fee)
        return BTCS
    except:
        print('failed attempt')
        raise

def ethtrans(to_address, nonce):
    try:
        val = random.randint(10000, 10000000)
        ethamount = round_sig((val / (10**18)), 4)
        from_address = '0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129'
        priv_key = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
        ethtx = send_eth(from_address, to_address, val, priv_key, nonce)
        bit = ETH(to_address, ethamount, ethtx)
        return bit
    except:
        print('failed attempt') 
        raise

def hellob(btcs):
    btc_privs = ['92b82iRG1kDJqXgdQx9D1sVskdg5ShXD6f7ggWoP5wLJas65U1j','93S6gfCcC9KeAJnH4Cihm1ohn6MoY5kW5JDBt9Jwg6DS6Y2WBii','92j5cnHrUQfehM8RE7mNwqFquPipj1ixvv6aTk1eDfcEvGQvhN7','92fxKDXkF97ku9PaSEcz3vKmyeTc9gQZCHFrGJVFGGJ5LkpSxQM',
        '93GtNodSaZEu3KzcvP7r5MnP2yU4GnC4WJRhxYAvmW8sroU7TLW', '93W3HKzWurB7a8YuBvfPXf2hTWipGWKCjrTkDPHKkk8T7jHZ2pf','92csoy33Do1Bzj91T74Bb7kPLUYUTRJDSSGwj1JyWUmUETiCYJy', '92woUn35UNvzhCtj6Kp3koNy9Gct92MksEQ43Bsc26TSxnT7FSd',
        '92jX4Yp7XmFNPpEkcTmQCygzdTGy5szu2Dcq8heocqynjZW9PyN', '93RfEtgM8njvTqfwfrigVsNZ42ofBDUZyzgwDBfnGuqtHHXNd9f', '92tfmyNZX5UFjUqXKSAWF58wg8ADnYFmLXmdrBxUrKv6nJ3oZnj','92iCLBsggkXXD5WTKZjSJExtuCVkXcBuHuzfCkgtLMnfnUwSiVk',
        '93PQRd4MJCScu3qQff5BWRzq31THYTvSdu72N72yuW3djP7DUQi', '92oQSweDxMtw8vLbtpBrZhBrGT1zVqt4wftub12BVBoxpBgLLjD', '93Fa3gbRTaRu27agcVb2nSNEr7tHVfAea4bE29bjhPAwWo9NCPC', '92tEjSkiBkoPCY3Yv6fdbk1kVToXCpmR3J35Ani3fWmja4aqqY8', 
        '92n9L6a18VHqnRbSSJBGghVr824D3BYBkY2uXZ3zdNvsQfrFEcm', '92cSm5MgrkwA2GQvhrBAvcDyUtTHzyLCpxjrcTmJNRXRXvRobuF', '931k5SpzC5nU72fME3kjXSbxpgytsSvTXnecNRqz6kNTyxHbTWP', '93QHiDUX5rakPKTNaD78A2Hn3CgMjsTWGuCwd6MjnosCs85QjTw']
    bcnt = 0
    btc_trans = []
    # for i in range(len(btcs)):
    while(bcnt < len(btcs)):
        blist = []
        n = random.randint(1, 10)
        if (bcnt + n) > len(btcs):
            n = len(btcs) - bcnt
        for x in range(n):
            blist.append(random.choice(btcs))
        btrans = btctrans(blist, btc_privs[bcnt % len(btc_privs)])
        btc_trans.extend(btrans)
        bcnt = bcnt + n
        print("BTC No.", bcnt)
    print('BTC DONE')
    return btc_trans

def helloe(eths):
    web3 = Web3(HTTPProvider('https://rinkeby.infura.io/UVgPTn3TgFMB0KhHUlif'))
    nonce = web3.eth.getTransactionCount('0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129')
    ecnt = 0
    eth_trans = []

    for i in range(len(eths)):
        etrans = ethtrans(random.choice(eths), nonce + ecnt)
        eth_trans.append(etrans)
        ecnt = ecnt+1
        print("ETH No.", ecnt)
    print('ETH DONE')
    return eth_trans

def run_simul(eths, btcs):
    with ProcessPoolExecutor(max_workers=2) as executor:
        e = executor.submit(helloe, eths)
        b = executor.submit(hellob, btcs)
    return ( b.result(), e.result())

@app.route("/")
def hello():
    try:
        xpub_b = "tpubDAK3K7sXsKqVs6XNCnBUZQVj2Yy5Sc98XV4Sy9xVfTcaGv8AGm4x585DUYpbBx61zURUoyFsJWAokuZY8Edm5PqJ9wza7i4pxVPKCttKjZH"
        xpub_e = 'xpub6EPXZc2brBKKFUNH3bxcg17g5mi5Uo5YmHHe2j1dWqqzV5WEN8dQYWXSvFpXz1PNrW9G8de6qoPun3Eiz4qKmaLXmViVYEHmrXRF6JbQXUE'    
        wallets = full_wallets(0, 50, xpub_e, xpub_b) 
        btcs = wallets[0]
        eths = wallets[1]
        results = run_simul(eths, btcs)
        btc_trans = results[0]
        eth_trans = results[1]
    except:
        raise
    # master_priv = '93CvyqZUTsVtNeWLfne7ZbpnG5npHXrabHL3ifmPPXvCjW5DxV4'

    #connect to MySQL database
    config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'port': '3306',
            'database': 'BROVIS'
        }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    for trans in btc_trans:
        cursor.execute("INSERT INTO bitcoin "
                   "(address, amount, txhash, xpub) "
                   "VALUES ('%s', '%s', '%s', '%s') " % (trans.address, trans.amount, trans.txhash, XPUB_btc)
                   )
        connection.commit()
    for trans in eth_trans:
        cursor.execute("INSERT INTO ethereum "
                   "(address, amount, txhash, xpub) "
                   "VALUES ('%s', '%s', '%s', '%s') " % (trans.address, trans.amount, trans.txhash, xpub_eth)
                   )
        connection.commit()
    
    cursor.close()
    connection.close()

    return render_template('home.html', hostname=socket.gethostname(), btcs=btcs, eths=eths, btc_trans=btc_trans, eth_trans=eth_trans)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, use_reloader=False, debug=True)

