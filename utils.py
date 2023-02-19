import binascii
from hashlib import sha256 as H
import nacl.signing
import nacl.encoding
import json

def convert_hex(data: bytes):
    return binascii.hexlify(data).decode('ascii')

def hash(data):
    return H(data.encode('utf-8')).hexdigest()

def sign(message, signing_key):
    signing_key = nacl.signing.SigningKey(signing_key, encoder=nacl.encoding.HexEncoder)
    signed = signing_key.sign(message.encode('utf-8'))
    # Convert the signature to a hexadecimal string with no prefix
    signature_hex = signed.signature.hex()
    return signature_hex

def verify_sig(public_key, message, signature):
    """
    Verifies the signature of a message using a given public key.

    :param public_key: The public key to use for signature verification.
    :param message: The message that was signed.
    :param signature: The signature to verify.
    :return: True if the signature is valid, False otherwise.
    """
    try:
        pubkey_bytes = nacl.encoding.HexEncoder.decode(public_key)

        # Create a VerifyKey object from the public key bytes
        verify_key = nacl.signing.VerifyKey(pubkey_bytes)
        sig = bytes.fromhex(signature)

        verify_key.verify(message.encode('utf-8'), sig)
        return True
    except nacl.exceptions.BadSignatureError:
        return False

def keypair():
    signing_key = nacl.signing.SigningKey.generate()
    verifying_key = signing_key.verify_key
    keypair = {
        'prikey': signing_key.encode(encoder=nacl.encoding.HexEncoder).decode('utf-8'),
        'pubkey': verifying_key.encode(encoder=nacl.encoding.HexEncoder).decode('utf-8')
    }
    return keypair

# keypairs = []

# for i in range(10):
#     keypairs.append(keypair())

# if __name__ == "__main__":
#     with open('input/keypair.json', 'w') as f:
#         json.dump(keypairs, f)