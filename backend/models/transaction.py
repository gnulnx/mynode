from backend.server import bitcoin
from backend.wallet.core.utils.jprint import jprint
from backend.wallet.core.utils.hash import *
from backend.wallet.core.utils.encoding import *
import uuid
import json


class Transaction:
    def __init__(self, txid, parent=None):
        self.uuid = uuid.uuid4()

        self.tx = bitcoin.getrawtransaction(txid, True)
        self.coinbase = False
        self.parent = parent

        # Input address/value
        self.inputs = []
        # Output address/value
        self.outputs = []

        self.process_transaction()

    def output(self):
        return {"inputs": self.inputs, "outputs": self.outputs}

    def __str__(self):
        return json.dumps(self.output(), indent=4, sort_keys=True, default=str)

    def process_transaction(self):
        self.process_vin()
        self.process_vout()

    def process_vin(self):
        for vin in self.tx["vin"]:
            if "coinbase" in vin:
                self.coinbase = True
                continue
            # jprint(vin)
            txid2 = Transaction(vin["txid"], parent=self)

    def process_vout(self):
        for vout in self.tx["vout"]:
            script_type = vout["scriptPubKey"]["type"]
            value = vout["value"]
            if script_type == "pubkey":
                address = self.address_from_pubkey(vout["scriptPubKey"])
                if self.parent:
                    self.parent.inputs.append({"address": address, "value": value})
                    print(f"Adding: {address} to {self.uuid}")
                else:
                    self.outputs.append({"address": address, "value": value})

            elif script_type == "pubkeyhash":
                address = self.address_from_pybkeyhash(vout["scriptPubKey"])
                if self.parent:
                    self.parent.input.append({"address": address, "value": value})
                else:
                    self.outputs.append({"address": address, "value": value})

            else:
                raise NotImplementedError(script_type)

    def address_from_pubkey(self, scriptpubkey):
        # P2Pk
        asm = scriptpubkey["asm"].split()[0]
        h = sha256_ripemd_double_hash(asm, False)
        key = "00" + h
        checksum = double_hash(key, binary=True)[:8]
        return base58_encode_hex_str(key + checksum)

    def address_from_pybkeyhash(self, scriptpubkey):
        h = scriptpubkey["asm"].split()[2]
        key = "00" + h
        checksum = double_hash(key, binary=True)[:8]
        return base58_encode_hex_str(key + checksum)
