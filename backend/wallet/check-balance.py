import os, sys
from wallet import Wallet


if __name__ == '__main__':
    address = sys.argv[1]
    w2 = Wallet.restore(private_key=address, test=True)

    uncomp_address = w2.details()['uncomp_address']
    print(uncomp_address)
    os.system(f"bx fetch-balance -f json {uncomp_address}")
