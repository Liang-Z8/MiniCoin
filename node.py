import json
import threading
import queue
import hashlib
import random
import time
from transaction import Transaction
from block import Block
from utils import *

#number of nodes
n = 10

block_chanels = []
mem_pool = []
chain_chanels = []

keypairs = []
with open('input/keypair.json', 'r') as f:
        keypairs = json.load(f)

for i in range(n):
    block_chanels.append(queue.Queue())
    mem_pool.append(queue.Queue())
    chain_chanels.append([])

class Node(threading.Thread):
    def __init__(self, n, keys):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        self.n =n

        #create keypair
        # keys = keypair()
        self.prikey = keys['prikey']
        self.pubkey = keys['pubkey']

        self.input = {}

        self.chain = []
        self.blockqueue = []
        self.chainqueue = []

    def get_input(self):
        input = []
        for i in range(0,len(self.chain)):
            i = len(self.chain) - i -1
            for output in self.chain[i].tx.outputs:
                if output['pubkey'] == self.pubkey:
                    it = {
                        "number": self.chain[i].tx.number,
                        "output": output
                    }
                    input.append(it)
                    break
            break
        self.input = input
            
    def mining(self):
        while not mem_pool[self.n]:
            tx = mem_pool[self.n].get()
            if self.valid_tx(tx):
                self.tx_broadcast(tx)
                prev_hash = hash(self.chain[-1].to_json())
                blc = Block(tx, prev_hash)
                blc.proof_of_work()
                self.chain.append(blc)
                self.block_broadcast(blc)

    def valid_tx(self, tx: Transaction):
        #Ensure the transaction is not already on the blockchain
        if self.exist_number(tx.number): return False
        
        input_sum = 0
        output_sum = 0
        #Ensure the transaction is validly structured:
        for ipt in tx.inputs:

            # not a double-spend(achieved by reversed local blockchain)
            for b in reversed(self.chain):

                #each number in the input exists as a transaction already on the blockchain
                if b.tx.number == ipt['number']:

                    #each output in the input actually exists in the named transaction
                    if ipt["output"] not in b.tx.outputs: return False

                    #each output in the input has the same public key, and that key can verify the signature on this transaction
                    pk = ipt['output']['pubkey']
                    message = {
                        "input": b.tx.inputs,
                        "output": b.tx.outputs
                    }
                    message = json.dumps(message)
                    if not verify_sig(pk, message, b.tx.signature): return False
            
            input_sum += ipt["output"]["value"]

        for opt in tx.outputs:
            output_sum += opt["value"]
        if input_sum != output_sum: return False
        
        return True

    def valid_block(self, block: Block):
        if block in self.chain:
            return False

        if block.prev_hash != hash(self.chain[-1].to_json()):
            return False

        data = f"{block.tx}{block.prev_hash}{block.nonce}".encode('utf-8')
        hash_result = hashlib.sha256(data).hexdigest()
        if int(hash_result, 16) > 0x07FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF or hash_result != block.pow:
            return False
        
        #Ensure the transaction is valid
        if not self.valid_tx(block.tx): return False

        return True

    def exist_number(self, number):
        for b in self.chain:
            if b.tx.number == number:
                return True
        return False

    def output(self):
        number = str(self.n)

        with open(f'output/node{number}.json', "w") as file:
            j = []
            for b in self.chain:
                j.append(b.to_json_ob())
            json.dump(j,file)

    def block_broadcast(self, block):
        global n
        global block_chanels

        p = []
        for i in range(1,3):
            p.append((self.n + i) % (n-1))
        
        for i in p:
            block_chanels[i].put(block)

    def block_listen(self):
        global n
        global block_chanels

        p = []
        for i in range(0, 1):
            if self.n - i < 0:
                p.append(n - i)
            p.append(self.n - i)
        
        for i in p:
            while not block_chanels[i].empty():
                block = block_chanels.get()
                if self.valid_block(block):
                    self.chain.append(block)
                    self.block_broadcast(block)
    
    def tx_broadcast(self, tx):
        global n
        global block_chanels

        p = []
        for i in range(1,3):
            p.append((self.n + i) % (n-1))
        
        for i in p:
            mem_pool[i].put(tx)

    def chain_listen(self):
        global n
        global chain_chanels

        for chain in chain_chanels[self.n]:
            if len(chain) <= self.chain:
                continue

            for i in range(1,len(chain)):
                block = chain[i]
                if block.prev_hash != hash(chain[i-1].to_json()):
                    continue

                data = f"{block.tx}{block.prev_hash}{block.nonce}".encode('utf-8')
                hash_result = hashlib.sha256(data).hexdigest()
                if int(hash_result, 16) > 0x07FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF or hash_result != block.pow:
                    continue
                
                #Ensure the transaction is valid
                if not self.valid_tx(block.tx): continue

            self.chain = chain

    def chain_broadcast(self):
        global n
        global chain_chanels

        p = []
        for i in range(1,3):
            p.append((self.n + i) % (n-1))

        for i in p:
            chain_chanels[i].append(self.chain)

    def run(self):
        i = 0
        while i < 100:
            if i % 3 ==0:
                self.chain_listen()
                self.block_broadcast
            self.block_listen()
            time.sleep(random.random())
            self.output()

class Mining_Node(Node):
    def run(self):
        i = 0
        while i < 100:
            if i % 4 ==0:
                self.chain_listen()
                self.chain_broadcast
            self.block_listen()
            self.mining()
            time.sleep(random.random())
            self.output()

class Malicious_Node(Node):

    def run(self):
        i = 0
        while i < 100:
            if i % 5 ==0:
                self.chain_listen()
                self.chain_broadcast
            self.block_listen()
            self.mining()
            time.sleep(random.random())
            self.output()