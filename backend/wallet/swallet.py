from wallet.wallet import Wallet
import os
from bitcoinlib.wallets import Wallet, wallet_create_or_open
from bitcoinlib.db import Db
import requests
from core.utils.jprint import jprint
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty, DictProperty
from kivy.lang import Builder

db_name = "./local.sqlite3"
Db(db_uri=db_name, password=None)

# from bitcoinlib.services.bitcoind import BitcoindClient

# base_url = "http://gnulnx:bc@192.168.86.118:8333"
# bdc = BitcoindClient(base_url=base_url)
# txid = "e0cee8955f516d5ed333d081a4e2f55b999debfff91a49e8123d20f7ed647ac5"
# rt = bdc.getrawtransaction(txid)
# print("Raw: %s" % rt)
# input()


class Header(AnchorLayout):
    pass


class MainScreen(Screen):
    pass


class DashboardScreen(Screen):
    def __init__(self, *args, **kwargs):
        print("INIT Dashboard")
        return super().__init__(*args, **kwargs)


class SendScreen(Screen):
    pass


class ReceiveScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class MainApp(App):
    kv_directory = "templates"
    passphrase = None
    wallet = None

    data = DictProperty({"wallet": "dingus", "name": "john"})

    def build(self):

        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(DashboardScreen(name="dashboard"))
        self.sm.add_widget(SendScreen(name="send"))
        self.sm.add_widget(ReceiveScreen(name="receive"))

        return self.sm

    def set_passphrase(self, instance, value):
        self.passphrase = value
        print(self.passphrase)

    def create_wallet(self, instance):
        resp = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        bpi = resp.json()
        self.price = bpi["bpi"]["USD"]["rate_float"]

        self.wallet = Wallet.create(
            name="Reserve Wallet",
            witness_type="segwit",
            keys=self.passphrase,
            network="bitcoin",
            db_uri=db_name,
            # Use this to match password to wassabi wallet with password
            # password="gnulnx",
        )
        WalletKeys = self.wallet.get_keys(number_of_keys=10)
        print("Top 10 addresses for thii wallet")
        for k in WalletKeys:
            print(k.address, k.balance())

        # Have to call scan to update transactions
        # self.wallet.scan()
        self.wallet.info()

        balance = float(self.wallet.balance(as_string=True).split()[0])
        self.balance = "${:,.2f}".format(self.price * balance)
        self.total = "${:,.2f}".format(self.price * balance)

        print("BTC Balance: %s" % balance)
        print("Current BTC Price: %s" % self.price)
        print("Current USD Value: ${:,.2f}".format(self.price * balance))
        print("Public Master: %s" % self.wallet.public_master())
        jprint(self.wallet.public_master().__dict__)

        self.data["wallet"] = self.wallet
        self.sm.current = "dashboard"


if __name__ == "__main__":
    os.system(f"rm -f {db_name}")
    MainApp().run()

# Test passphrase:
# ugly puppy animal monster sudden betray green tree girl garbage planet face
# cat doll already tribe helmet present maximum increase song club wrist rabbit
