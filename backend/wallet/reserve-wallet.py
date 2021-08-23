#!/usr/bin/env python
#
# Reserve Wallet
# usage:  ./reserve-wallet
# At prompt enter your passphase.  It will take a few moments, but you should see your wallet details.

import uuid
from bitcoinlib.wallets import Wallet, wallet_create_or_open
import requests
from core.utils.jprint import jprint

resp = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
bpi = resp.json()
price = bpi["bpi"]["USD"]["rate_float"]

print("enter passphrase")
passphrase = str(input())
print("please wait while we setup wallet and fetch info...")

w = wallet_create_or_open(
    uuid.uuid4().hex, witness_type="segwit", keys=passphrase, network="bitcoin"
)
# WalletKeys = w.get_keys(number_of_keys=10)
# print("Top 10 addresses for thii wallet")
# for k in WalletKeys:
#     print(k.address, k.balance())

# Have to call scan to update transactions
w.scan()
w.info()

balance = float(w.balance(as_string=True).split()[0])
print("BTC Balance: %s" % balance)
print("Current BTC Price: %s" % price)
print("Current USD Value: ${:,.2f}".format(price * balance))
