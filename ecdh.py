# RFC 5903 256-Bit Random ECP Group page 4
# NIST.SP.800-56Ar3 Key Pair Generation Using Extra Random Bits page 30
# https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/
# https://github.com/andreacorbellini/ecc/tree/master
#
# https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc
# https://github.com/mcxxmc/simple-implementation-ecc

import sympy
import os
import secrets
from tinyec.ec import SubGroup, Curve
from datetime import datetime

# Parameters and equation
s = 128
p = pow(2, 256) - pow(2, 224) + pow(2, 192) + pow(2, 96) - 1
group_prime = int.from_bytes(bytes.fromhex('FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF'), byteorder='big')
assert p == group_prime
x, b = sympy.symbols('x, b')
ecurve = x**3 - 3*x + b # y^2 = x^3 - 3 x + b
a = -3 # Because the general form is y^2 = x^3 + ax + b and above a is replaced with -3
group_b = int.from_bytes(bytes.fromhex('5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B'), byteorder='big')
group_order = int.from_bytes(bytes.fromhex('FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551'), byteorder='big')
gx = int.from_bytes(bytes.fromhex('6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296'), byteorder='big')
gy = int.from_bytes(bytes.fromhex('4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5'), byteorder='big')

field = SubGroup(p=group_prime, g=(gx, gy), n=group_order, h=1)
curve = Curve(a=-3, b=group_b, field=field, name='256-Bit Random ECP Group')

def round_up(value):
    decimal_part = value - int(value)
    if decimal_part >= 0.5:
        return int(value) + 1
    else:
        return int(value)

def generate_private_key():
    L = group_order.bit_length() + 64
    c = int.from_bytes(os.urandom(max(s, L) // 8))
    assert c > 0 and c < (pow(2, max(s, L)) - 1)
    return (c % (group_order - 1)) + 1

def verify(point):
    return pow(point.y, 2, group_prime) == ecurve.subs([(x, point.x),(b, group_b)]) % group_prime

start = datetime.now()
M1_secret = generate_private_key()
M1_public = M1_secret*curve.g
#assert verify(M1_public)

M2_secret = generate_private_key()
M2_public = M2_secret*curve.g
#assert verify(M2_public)

sk1 = M1_secret*M2_public
sk2 = M2_secret*M1_public
#assert sk1 == sk2

#print(f'sk1.x={sk1.x}, sk1.y={sk1.y}')
#print()
#print(f'sk2.x={sk2.x}, sk2.y={sk2.y}')

print(f"Complete duration {round_up((datetime.now()-start).total_seconds()*1000)}ms")