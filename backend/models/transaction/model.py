from server import bitcoin
from wallet.core.utils.jprint import jprint
from wallet.core.utils.hash import *
from wallet.core.utils.encoding import *
import models.transaction.utils as tx_utils
import json


class Transaction:
    def __init__(self, tx="", txid=None, parent=None):
        """
        Two way's to instantiate a Transaction object.
        1) Pass in a txid.  This will use getrawtransaction to fetch the transaction record.
        2) Pass in a transaction record.  Likley from getblock 2 which returns all the transaction
           objects so we don't have to iterate over them and pass in the ids'.
           getblock 2 is much faster than getblock 1 followed by getrawtransaction loop.
        """

        if txid:
            self.txid = txid
            self.tx = bitcoin.getrawtransaction(txid, True)
        elif tx:
            self.tx = tx
            self.txid = self.tx["txid"]

        self.coinbase = False
        self.parent = parent

        # Input address/value
        self.inputs = []
        # Output address/value
        self.outputs = []

        # Record any errors during processing
        self.errors = []

        self.process_transaction()

    def output(self):
        return {"inputs": self.inputs, "outputs": self.outputs}

    def formated(self):
        return {
            "data_type": "txn",
            "tx": self.tx,
            "coinbase": self.coinbase,
            "inputs": self.inputs,
            "outputs": self.outputs,
        }

    def __str__(self):
        return self.txid
        return json.dumps(self.output(), indent=4, sort_keys=True, default=str)

    def process_transaction(self):
        try:
            if not self.parent:
                self.process_vin()
            self.process_vout()
        except Exception as e:
            self.errors.append({"exception": str(e)})
            jprint(self.errors)

    def process_vin(self):

        for vin in self.tx["vin"]:
            if "coinbase" in vin:
                self.coinbase = True
                # TODO Do you need something in the inputs here?
                continue

            outnum = vin["vout"]
            txid2 = Transaction(txid=vin["txid"], parent=self)
            self.inputs.append(txid2.outputs[outnum])

    def process_vout(self):
        for vout in self.tx["vout"]:
            script_type = vout["scriptPubKey"]["type"]
            value = vout["value"]
            if script_type == "pubkey":
                address = self.address_from_pubkey(vout["scriptPubKey"])
                self.outputs.append({"address": address, "value": value})

            elif script_type == "pubkeyhash":
                address = self.address_from_pybkeyhash(vout["scriptPubKey"])
                self.outputs.append({"address": address, "value": value})

            else:
                msg = {"message": f"script_type: {script_type} is not implemented yet"}
                if self.parent:
                    self.parent.errors.append(msg)
                else:
                    self.errors.append(msg)
                raise NotImplementedError(script_type)

    def address_from_pubkey(self, scriptpubkey):
        # P2Pk
        return tx_utils.address_from_pubkey(scriptpubkey)

    def address_from_pybkeyhash(self, scriptpubkey):
        # P2PKH
        return tx_utils.address_from_pubkeyhash(scriptpubkey)
