# A secure and efficient conference key distribution system
# Mike Burmester & Yvo Desmedt 

from diffiehellman import DiffieHellman
from datetime import datetime
import sympy

def round_up(value):
    decimal_part = value - int(value)
    if decimal_part >= 0.5:
        return int(value - decimal_part + 1)
    else:
        return int(value)

start = datetime.now()
# automatically generate two key pairs
parameters = DiffieHellman(group=14, key_bits=540)
g = 2
p = parameters._prime

# Each player computes public keys
parameters.generate_private_key()
M1_secret = parameters._private_key
M1_public = pow(g, M1_secret, p) # g^ta1
M1_inverse = sympy.mod_inverse(M1_public, p) # 1/(g^ta1)

parameters.generate_private_key()
M2_secret = parameters._private_key
M2_public = pow(g, M2_secret, p) # g^ta2
M2_inverse = sympy.mod_inverse(M2_public, p) # 1/(g^ta2)

parameters.generate_private_key()
M3_secret = parameters._private_key
M3_public = pow(g, M3_secret, p) # g^ta3
M3_inverse = sympy.mod_inverse(M3_public, p) # 1/(g^ta3)

parameters.generate_private_key()
M4_secret = parameters._private_key
M4_public = pow(g, M4_secret, p) # g^ta4
M4_inverse = sympy.mod_inverse(M4_public, p) # 1/(g^ta4)

X1_dv = (M2_public*M4_inverse) % p # g^(ta2-ta4)
X2_dv = (M3_public*M1_inverse) % p # g^(ta3-ta1)
X3_dv = (M4_public*M2_inverse) % p # g^(ta4-ta2)
X4_dv = (M1_public*M3_inverse) % p # g^(ta1-ta3)

# Each player computes gadgets
X1 = pow(X1_dv, M1_secret, p) # X[4,1,2] g^ta1*ta2-ta4*ta1
X2 = pow(X2_dv, M2_secret, p) # X[1,2,3] g^ta2*ta3-ta1*ta2
X3 = pow(X3_dv, M3_secret, p) # X[2,3,4] g^ta3*ta4-ta2*ta3
X4 = pow(X4_dv, M4_secret, p) # X[3,4,1] g^ta3*ta1-ta3*ta3

member_count = 4
M1_sk = pow(M4_public, member_count*M1_secret, p) * pow(X1, member_count-1, p) * pow(X2, member_count-2, p) * X3 % p
M2_sk = pow(M1_public, member_count*M2_secret, p) * pow(X2, member_count-1, p) * pow(X3, member_count-2, p) * X4 % p
M3_sk = pow(M2_public, member_count*M3_secret, p) * pow(X3, member_count-1, p) * pow(X4, member_count-2, p) * X1 % p
M4_sk = pow(M3_public, member_count*M4_secret, p) * pow(X4, member_count-1, p) * pow(X1, member_count-2, p) * X2 % p

assert M1_sk == M2_sk == M3_sk == M4_sk

print(f"Complete duration {round_up((datetime.now()-start).total_seconds()*1000)}ms")