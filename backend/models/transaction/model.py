from server import bitcoin
from wallet.core.utils.jprint import jprint
from wallet.core.utils.hash import *
from wallet.core.utils.encoding import *
import models.transaction.utils as tx_utils
import uuid
import json


class Transaction:
    def __init__(self, txid, parent=None):
        self.uuid = uuid.uuid4()

        self.txid = txid
        self.tx = bitcoin.getrawtransaction(txid, True)
        # if not parent:
        #     print("Building New Transaction: %s" % txid)
        #     jprint(self.tx)
        #     input()
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
        # Set at begin/end.  A hack to stop infinite recurssion
        # if hasattr(self, "process_vin_called"):
        #     return

        # print("process_vin: %s" % len(self.tx["vin"]))
        # input()

        for vin in self.tx["vin"]:
            if "coinbase" in vin:
                self.coinbase = True
                # TODO Do you need something in the inputs here?
                continue

            outnum = vin["vout"]
            txid2 = Transaction(vin["txid"], parent=self)
            self.inputs.append(txid2.outputs[outnum])

        # print(self.inputs)
        # print("vins processed")
        # input()

        # setattr(self, "process_vin_called", True)

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
