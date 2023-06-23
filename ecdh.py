# RFC 5903
import math
import sympy
import os

s = 128
p = pow(2, 256) - pow(2, 224) + pow(2, 192) + pow(2, 96) - 1
group_prime = int.from_bytes(bytes.fromhex('FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF'), byteorder='big')
assert p == group_prime

x, b = sympy.symbols('x, b')
ecurve = x**3 - 3*x + b

group_b = int.from_bytes(bytes.fromhex('5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B'), byteorder='big')
group_order = int.from_bytes(bytes.fromhex('FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551'), byteorder='big')
gx = int.from_bytes(bytes.fromhex('6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296'), byteorder='big')
gy = int.from_bytes(bytes.fromhex('4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5'), byteorder='big')

L = group_order.bit_length() + 64
c = int.from_bytes(os.urandom(max(s, L) // 8))
d = (c % (group_order - 1)) + 1
Q = (d*gx,d*gy)
y_squared = pow(Q[1],2)
print(f"y_squared: {y_squared}")
print(f"public key: {ecurve.subs([(x, Q[0]),(b, group_b)])}")
#assert ecurve.subs([(x, Q[0]),(b, group_b)]) == y_squared