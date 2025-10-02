BLOCK_SIZE = 16

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

a_block = b'a' * BLOCK_SIZE

cypher_text = a_block * 2
print("Cypher text za vnesti:", cypher_text.hex())

plain_text = bytes.fromhex(input("Vnesi, kar je bilo vrnjeno: "))

print("Cypher text", cypher_text)
print("Plain text", plain_text)

comes_out = byte_xor(plain_text[BLOCK_SIZE:], a_block)

# ugotoviti moramo, s čim je bilo to xorano
print("\na = b ^ c\n")
print("a =", plain_text[:BLOCK_SIZE])
print("b =", comes_out)
print("c =", "?\n")
print(plain_text[:BLOCK_SIZE],"=",comes_out,"^","?","\n\n")

print("c = b ^ a\n")
solution = byte_xor(comes_out, plain_text[:BLOCK_SIZE])
print("c =", solution,"\n\n")

# print as string
print("REŠITEV (če ni navaden string, je nekaj narobe):\n\n" + solution.decode(), "\n")
