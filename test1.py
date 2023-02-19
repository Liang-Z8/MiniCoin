import nacl.hash
message = b'This is a message to be hashed'
hash_func = nacl.hash.sha256
hasher = hash_func(message, encoder=nacl.encoding.HexEncoder)
print(hasher.decode())