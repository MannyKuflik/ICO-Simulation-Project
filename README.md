<img src="https://travis-ci.org/MannyKuflik/ICO-Simulation-Project.svg?branch=master">

<h1><img src="https://en.bitcoin.it/w/images/en/2/29/BC_Logo_.png" height="22px"> ICO-Simulation-Project <img src="http://introtocrypto.com/wp-content/uploads/2017/08/ether@2x.png" height="22px" padding></h1>
By Lawrence Li and Emanuel Kuflik

<br/>

## Description
Simulates ICO investing Process. The simulation accomplishes this by sending up to several thousand testnet bitcion and rinkeby net ethereum transactions in order to test funactionalities like a Blockchain Watching Service.

<br/>

## Setup

### Easy Setup
To run, simply call:
<pre>$ docker run -p 4000:80 mannykuf/ico-simulator:v3</pre> 
in the command line. It'll run on localhost:4000

### Advanced Setup
If you want database integration you'll need to clone this repo onto your local machine and configure the variables in connect() in app.py to match the variables for a local Mysql Schema you set up. This can be done through [MySQLWorkbench](https://dev.mysql.com/downloads/workbench/?utm_source=tuicool).
Once it is configured, you can run it by calling:
<pre>$ sudo python app.py</pre>  
in the command line. It'll run on 0.0.0.0


<i> ENJOY :) </i>
