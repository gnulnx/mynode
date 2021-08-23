import segno
import subprocess
from core.utils.wallet import (
    create_passphrase,
    private_key_from_passphrase,
    compute_wif,
    wif_to_private_key,
    private_key_to_address,
    create_public_keys,
)
from core import jprint, info, warn, error  # noqa
from .exceptions import PassphraseUnhashable, WalletRestoreError


class Wallet:
    private_key = None
    public_key = None
    wif = None
    wifc = None
    qr_code_path = None

    # The 12 word pass phrase associated with this wallet.
    # Can be used to initialize private/public keys
    passphrase = None

    @classmethod
    def new(cls, language="english", strength=128, *args, **kwargs):
        try:
            passphrase = create_passphrase(language=language, strength=strength)
            w = Wallet(passphrase=passphrase, **kwargs)

            warn(
                "This is your passphrase.  Write this down and store it some place safe."
            )
            warn("If you loose this phrase you will loose the contents of your wallet.")
            info(f"{w.passphrase}")
            # print("Address: %s" % w.address)
            # print("Public Key: %s" % w.public_key)
            # print("Passphrase: %s" % w.passphrase)
            # print("private_key: %s" % w.private_key)
            # print("wif: %s" % w.wif)
            return w
        except PassphraseUnhashable:
            pass

    @classmethod
    def restore(cls, passphrase=None, private_key=None, **kwargs):
        """
        Restore  a wallet from a passphrase or a private key.
        Private key can be Hex, WIF, or WIFC.
        Format will be auto detected and printed to the console
        """
        if passphrase:
            return Wallet(passphrase=passphrase)

        if private_key:
            try:
                # Check if private_key is in hex format
                int(private_key, 16)
                info("restoring wallet from hex format")
                return Wallet(private_key=private_key, **kwargs)
            except ValueError:
                if private_key[0] in ["5", "9"]:
                    # Check if private_key is in WIF format.
                    # 5 is for mainnet.  9 is for testnet
                    info("restoring wallet from WIF format")
                    return Wallet(wif=private_key, **kwargs)
                elif private_key[0] in ["L", "K", "c"]:
                    # Check if private_key is in WIFC format.
                    # L/K are mainnet.  c is testnet
                    info("restoring wallet from WIFC format")
                    return Wallet(wifc=private_key, **kwargs)

            raise WalletRestoreError(
                f"Private key: {private_key} can not be imported\n"
            )

        raise WalletRestoreError("restore requires either passphrase or private_key")

    def __init__(
        self,
        passphrase=None,
        private_key=None,
        wif=None,
        wifc=None,
        initial_hashes=1,
        testnet=False,
        *args,
        **kwargs,
    ):
        self.testnet = testnet

        if passphrase:
            self.passphrase = passphrase
            self.private_key = private_key_from_passphrase(
                self.passphrase, initial_hashes
            )
        elif private_key:
            self.private_key = private_key
        elif wif:
            self.wif = wif
            self.private_key = wif_to_private_key(wif)
        elif wifc:
            self.wifc = wifc
            self.private_key = wif_to_private_key(self.wifc, compressed=True)

        if not self.wif:
            self.wif = compute_wif(self.private_key, binary=True)

        if not self.wifc:
            self.wifc = compute_wif(self.private_key, compressed=True, binary=True)

        # Need to double check this section
        if wif_to_private_key(self.wif) != self.private_key:
            raise PassphraseUnhashable

        if wif_to_private_key(self.wifc, compressed=True) != self.private_key:
            raise PassphraseUnhashable

        if "test" not in kwargs:
            self.create_qr_code()
            # subprocess.call(["open", "./wallet_qr.png"])

    def __str__(self):
        self.details(show=True)
        return "wifc: %s" % self.wifc

    def public_key(self, compressed=True):
        if compressed:
            return create_public_keys(self.private_key)[0]
        else:
            return create_public_keys(self.private_key)[1]

    def address(self, compressed=True):
        if compressed:
            return private_key_to_address(self.private_key, testnet=self.testnet)[0]
        else:
            return private_key_to_address(self.private_key, testnet=self.testnet)[1]

    def details(self, show=False):
        details = {
            "passphrase": self.passphrase,
            "wif": self.wif,
            "wifc": self.wifc,
            "private_key": self.private_key,
            "public_key:": self.public_key(),
            "address": self.address(),
            "uncomp_public_key": self.public_key(compressed=False),
            "uncomp_address": self.address(compressed=False),
        }
        if show:
            jprint(details)
            return
        return details

    def create_qr_code(self, output="wallet_qr.png", compressed=True):
        self.qr_code_path = output
        print("self.qr_code_path: %s" % self.qr_code_path)
        qr = segno.make((self.address(compressed=compressed)))
        qr.save(self.qr_code_path, scale=10)
