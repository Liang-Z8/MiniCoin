import hashlib
import secrets
import json
from transaction import Transaction

class Block:
    def __init__(self, tx: Transaction, prev_hash: str):
        # if not prev_hash:
        #     with open('./input/Genesis.json', 'r') as f:
        #         tx = json.load(f)
        #     self.tx = Transaction(tx['input'], tx['output'], secrets.token_bytes(32).hex())
        #     self.prev_hash = secrets.token_bytes(32).hex()
        #     self.nonce = 0
        #     self.pow = secrets.token_bytes(32).hex()
        #     return

        self.tx = tx
        self.prev_hash = prev_hash
        self.nonce = 0
        self.pow = 0x07FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    def __repr__(self):
        return f"Block(tx={self.tx}, prev={self.prev_hash}, nonce={self.nonce}, pow={self.pow})"

    def to_json_ob(self):
        data = {
            'tx': self.tx.to_json_ob(),
            'prev': self.prev_hash,
            'nonce': self.nonce,
            'pow': self.pow
            }
        return data
    
    def to_json(self):
        return json.dumps(self.to_json_ob())

    def proof_of_work(self):
        target = 0x07FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        while True:
            data = f"{self.tx}{self.prev_hash}{self.nonce}".encode('utf-8')
            hash_result = hashlib.sha256(data).hexdigest()
            if int(hash_result, 16) <= target:
                self.pow = hash_result
                return
            else:
                self.nonce += 1
