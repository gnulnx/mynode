from backend.wallet.core.utils.hash import sha256_ripemd_double_hash, double_hash
from backend.wallet.core.utils.encoding import base58_encode_hex_str


def address_from_pubkey(scriptpubkey):
    # P2Pk
    asm = scriptpubkey["asm"].split()[0]
    h = sha256_ripemd_double_hash(asm, False)
    key = "00" + h
    checksum = double_hash(key, binary=True)[:8]
    return base58_encode_hex_str(key + checksum)


def address_from_pubkeyhash(scriptpubkey):
    h = scriptpubkey["asm"].split()[2]
    key = "00" + h
    checksum = double_hash(key, binary=True)[:8]
    return base58_encode_hex_str(key + checksum)
