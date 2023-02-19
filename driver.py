from node import *

with open('./input/Genesis.json', 'r') as f:
    tx = json.load(f)
    tx = Transaction(tx['input'], tx['output'], '')
    for i in range(n):
        mem_pool[i].put(tx)

n0 = Mining_Node(0, keypairs[0])
n1 = Mining_Node(1, keypairs[1])
n2 = Mining_Node(2, keypairs[2])
n3 = Node(3, keypairs[3])
n4 = Node(4, keypairs[4])
n5 = Node(5, keypairs[5])
n6 = Node(6, keypairs[6])
n7 = Node(7, keypairs[7])

n0.start()
n1.start()
n3.start()
n4.start()
n5.start()
n6.start()
n7.start()

n0.join()
n1.join()
n2.join()
n3.join()
n4.join()
n5.join()
n6.join()
n7.join()
