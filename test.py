from block import Block
from transaction import Transaction
import json
import secrets
from utils import *

l = []
genesis = Block(0, '')
l.append(genesis)
with open('input/transaction.json', 'r') as f:
    txs = json.load(f)
for tx in txs:
    btx = Transaction(tx['input'], tx['output'], secrets.token_bytes(32).hex())
    prev_hash = hash(l[-1].to_json())
    block = Block(btx, prev_hash)
    l.append(block)
# print(genesis.to_json)
with open("output/genesis_block.json", "w") as file:
    j = []

    for b in l:
        j.append(b.to_json_ob())
    
    json.dump(j,file)
    
