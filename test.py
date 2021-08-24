from backend.wallet.core.utils.jprint import jprint
from server import bitcoin
from backend.wallet.core.utils.hash import *
from backend.wallet.core.utils.encoding import *
from backend.models.transaction import Transaction

txid = "6f7cf9580f1c2dfb3c4d5d043cdbb128c640e3f20161245aa7372e9666168516"
txn = Transaction(txid)
print(txn)
# print(txid)
# print(txn.uuid)
# print("Inputs")
# jprint(txn.inputs)
# print("Outputs")
# jprint(txn.outputs)
print("back from transaction init")
