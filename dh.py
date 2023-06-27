import random
from sympy import isprime
from datetime import datetime

def generate_private_key(p: int) -> int:
    return random.randint(1, p-1)

def round_up(value):
    decimal_part = value - int(value)
    if decimal_part >= 0.5:
        return int(value) + 1
    else:
        return int(value)

if __name__ == "__main__":
    BITS=1024
    while True:
        p = random.getrandbits(BITS)
        # Make sure the number is odd
        p |= 1
        # Make sure the number has the correct bit length
        p |= (1 << (BITS-1))
        if isprime(p):
            #print(f"Generated p: {p}")
            break

    while True:
        g = random.getrandbits(BITS)
        if g < p:
            #print(f"Generated g: {g}")
            break

start = datetime.now()
alice_secret = generate_private_key(p) # secret a
alice_public = pow(g, alice_secret, p) # public A = g^a mod p
alice_end = datetime.now()-start

bob_secret = generate_private_key(p)   # secret b
bob_public = pow(g, bob_secret, p)     # public B = g^b mod p

alice_shared = pow(bob_public, alice_secret, p) # shared key = B^a mod p = g^(ba) mod p
bob_shared = pow(alice_public, bob_secret, p)   # shared key = A^b mod p = g^(ab) mod p

assert alice_shared == bob_shared
#print('Two party diffie-hellman key exchange')
#print('Shared secret:', alice_shared)
#print('Shared secret:', bob_shared)

carol_secret = generate_private_key(p) # secret c
carol_public = pow(g, carol_secret, p) # public C = g^c mod p

g_a = pow(g, alice_secret, p) # g^a mod p (alice adds her secret to the mix)
g_ab = pow(g_a, bob_secret, p) # g^(ab) mod p (bob adds his secret to the mix)
carol_shared = pow(g_ab, carol_secret, p) # shared key = g^(abc) mod p (carol adds her secret to the mix)

g_c = pow(g, carol_secret, p) # g^c mod p (carol adds her secret to the mix)
g_ca = pow(g_c, alice_secret, p) # g^(ca) mod p (alice adds her secret to the mix)
bob_shared = pow(g_ca, bob_secret, p) # shared key = g^(cab) mod p (bob adds his secret to the mix)

g_b = pow(g, bob_secret, p) # g^b mod p (bob adds his secret to the mix)
g_bc = pow(g_b, carol_secret, p) # g^(bc) mod p (carol adds her secret to the mix)
alice_shared = pow(g_bc, alice_secret, p) # shared key = g^(bca) mod p (alice adds her secret to the mix)

assert carol_shared == bob_shared == alice_shared
#print('Three party diffie-hellman key exchange')
#print('Shared secret:', carol_shared)
#print('Shared secret:', bob_shared)
#print('Shared secret:', alice_shared)

print(f"Alice duration {round_up(alice_end.total_seconds()*1000)}ms")
print(f"Complete duration {round_up((datetime.now()-start).total_seconds()*1000)}ms")