from flask import Flask, render_template
from BTCtrans import BTC_process
from ETHtrans import send_eth
from GenAddrs import full_wallets, xpub_eth, XPUB_btc
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
import cProfile


app = Flask(__name__)

def round_sig(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)

# @retry
def btctrans(dest, priv):
    try: 
        amnt = float(random.randrange(1, 500))/1000000
        amount = round_sig((amnt/1000), 4) 
        fee = 5
        txhash = BTC_process(destination=dest, priv_wif=priv, fee=fee, amnt=amnt) 
        if txhash is 'fail':
            bit = BTC('Failed to send to ' + dest, 'N/A', 'Failed Tx')
            return bit
        if txhash is not None: 
            bit = BTC(dest, amount, txhash)
            return bit
    except:
        print('failed attempt')
        raise

    
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
        priv_key = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
        ethtx = send_eth(from_address, to_address, val, priv_key, nonce)
        bit = ETH(to_address, ethamount, ethtx)
        if bit is not None: return bit
        else:
            time.sleep(2)
            ethtrans(to_address, nonce) 
    except:
        print('failed attempt') 
        raise
        # time.sleep(2)
        # ethtrans(to_address, nonce) 

        # ethtx = "unable to make transaction"
        # val = "unable to make transaction"
        # to_address = "unable to make transaction"
        # ethfl = "(Failed)"
        # raise
        # return ETH('fail', 'N/A', 'fail')

@app.route("/")
def hello():
    try:
        web3 = Web3(HTTPProvider('https://rinkeby.infura.io/UVgPTn3TgFMB0KhHUlif'))
        nonce = web3.eth.getTransactionCount('0xde055eCaB590E0E7f2Cb06445dd6272fb7D65129') 
        bcnt = 0
        btc_privs = ['92b82iRG1kDJqXgdQx9D1sVskdg5ShXD6f7ggWoP5wLJas65U1j','93S6gfCcC9KeAJnH4Cihm1ohn6MoY5kW5JDBt9Jwg6DS6Y2WBii','92j5cnHrUQfehM8RE7mNwqFquPipj1ixvv6aTk1eDfcEvGQvhN7','92fxKDXkF97ku9PaSEcz3vKmyeTc9gQZCHFrGJVFGGJ5LkpSxQM',
        '93GtNodSaZEu3KzcvP7r5MnP2yU4GnC4WJRhxYAvmW8sroU7TLW', '93W3HKzWurB7a8YuBvfPXf2hTWipGWKCjrTkDPHKkk8T7jHZ2pf','92csoy33Do1Bzj91T74Bb7kPLUYUTRJDSSGwj1JyWUmUETiCYJy', '92woUn35UNvzhCtj6Kp3koNy9Gct92MksEQ43Bsc26TSxnT7FSd',
        '92jX4Yp7XmFNPpEkcTmQCygzdTGy5szu2Dcq8heocqynjZW9PyN', '93RfEtgM8njvTqfwfrigVsNZ42ofBDUZyzgwDBfnGuqtHHXNd9f', '92tfmyNZX5UFjUqXKSAWF58wg8ADnYFmLXmdrBxUrKv6nJ3oZnj','92iCLBsggkXXD5WTKZjSJExtuCVkXcBuHuzfCkgtLMnfnUwSiVk',
        '93PQRd4MJCScu3qQff5BWRzq31THYTvSdu72N72yuW3djP7DUQi', '92oQSweDxMtw8vLbtpBrZhBrGT1zVqt4wftub12BVBoxpBgLLjD', '93Fa3gbRTaRu27agcVb2nSNEr7tHVfAea4bE29bjhPAwWo9NCPC', '92tEjSkiBkoPCY3Yv6fdbk1kVToXCpmR3J35Ani3fWmja4aqqY8', 
        '92n9L6a18VHqnRbSSJBGghVr824D3BYBkY2uXZ3zdNvsQfrFEcm', '92cSm5MgrkwA2GQvhrBAvcDyUtTHzyLCpxjrcTmJNRXRXvRobuF', '931k5SpzC5nU72fME3kjXSbxpgytsSvTXnecNRqz6kNTyxHbTWP', '93QHiDUX5rakPKTNaD78A2Hn3CgMjsTWGuCwd6MjnosCs85QjTw']
        bcnt = 0
        ecnt = 0
        wallets = full_wallets(5, 3) 
        btcs = wallets[0]
        eths = wallets[1] 
        ethfl = ""
        btcfl = ""
    except:
        web3 = None
        nonce = None
        btc_privs = []
        btcs = []
        eths = []
        ecnt = 0
        bcnt = 0
        ethfl = "SYSTEM FAILURE"
        btcfl = "SYSTEM FAILURE"

    btc_trans = []
    eth_trans = []
    master_priv = '93CvyqZUTsVtNeWLfne7ZbpnG5npHXrabHL3ifmPPXvCjW5DxV4'


    if (len(btcs) >= len(eths)):
        l = len(btcs)
        print("Length:", l)
    else:
        l = len(eths)
        # print("Length:", l)
    
    for x in range(l):
        if (x < len(eths)):
            etrans = ethtrans(random.choice(eths), nonce + ecnt)
            eth_trans.append(etrans)
            ecnt = ecnt+1
            print("ETH No.", ecnt)
        if (x < len(btcs)):
            btrans = btctrans(random.choice(btcs), btc_privs[bcnt % len(btc_privs)])
            btc_trans.append(btrans)
            bcnt = bcnt + 1
            print("BTC No.", bcnt)
    print('Done.')



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
    # cursor.execute('SELECT address, amount, txhash FROM bitcoin')
    # cursor.execute('SELECT address, amount, txhash FROM ethereum')
    # results = [[address, amount, txhash] for (address, amount, txhash) in cursor]

    # return json.dumps({'data': connect()})

    return render_template('home.html', hostname=socket.gethostname(), btcs=btcs, eths=eths, btc_trans=btc_trans, eth_trans=eth_trans, btcfl=btcfl, ethfl=ethfl)
    # return html.format(hostname=socket.gethostname(), btcs=btcs, eths=eths, visits=visits, dest=dest, amount=amount, tx=tx, btcfl=btcfl, to_address=to_address, ethamount=ethamount, ethtx=ethtx, ethfl=ethfl)
    # pk=pk, ad=ad, sk=sk, Bpk=Bpk, Bsk=Bsk, Badd=Badd,
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, use_reloader=False, debug=True)