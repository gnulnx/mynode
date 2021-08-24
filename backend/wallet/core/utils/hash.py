import hashlib
import hexdump
import math  # noqa
import numbers  # noqa
import base58  # noqa


def bytes_to_hex(_str):
    if isinstance(_str, bytes):
        return hexdump.dump(_str, sep="")
    else:
        raise ValueError(f"{_str} must be bytes")


def binary_hash(_str, algo="sha256"):
    if isinstance(_str, str):
        _str = hexdump.restore(_str.upper())
    elif isinstance(_str, bytes):
        _str = hexdump.restore(bytes_to_hex(_str))

    if algo == "sha256":
        h = hashlib.sha256(_str)
        return h.hexdigest().upper()
    elif algo == "ripemd160":
        h = hashlib.new("ripemd160")
        h.update(hexdump.restore(_str))
        return h.hexdigest().upper()


def hash160(_str):
    h = hashlib.new("ripemd160")
    h.update(hexdump.restore(_str.upper()))
    return h.hexdigest().upper()


def plain_hash(_str):
    if not isinstance(_str, bytes):
        _str = _str.upper().encode("utf-8")
    return hashlib.sha256(_str).hexdigest().upper()


def double_hash(key: str, binary=True) -> str:
    """
    Same results as double_sha256 when binary=True

    :param string: String to be hashed

    :return str
    """
    hash_func = binary_hash if binary else plain_hash
    return hash_func(hash_func(key))


def hexdump_sha256(hex_str, digest=True):
    """
    :hex_str - a hashed string like: 600FFE422B4E00731A59557A5CCA46CC183944191006324A447BDB2D98D4B408
    :digest - when True return h.digest() which is the bytes representation.  Otherwise return the hexdigest() str.
    """
    sha = hashlib.sha256(hexdump.restore(hex_str))
    if digest:
        return sha.digest()
    else:
        return sha.hedigest().upper()


def sha256_ripemd_double_hash(hex_str: str, digest=True) -> str:
    h = hashlib.new("ripemd160")
    h.update(hexdump_sha256(hex_str))
    if digest:
        return h.digest()
    else:
        return h.hexdigest().upper()
