# Communication-Efficient Group Key Agreement
# Yongdae Kim, Adrian Perrig and Gene Tsudik

from diffiehellman import DiffieHellman
from datetime import datetime

def round_up(value):
    decimal_part = value - int(value)
    if decimal_part >= 0.5:
        return int(value) + 1
    else:
        return int(value)

if __name__ == "__main__":
    start = datetime.now()
    parameters = DiffieHellman(group=14, key_bits=540)
    g = 2
    p = parameters._prime
    #checkpoint = datetime.now()
    #print(f"Initializing DH parameters took {round_up((checkpoint-start).total_seconds()*1000)}ms")

    # Members with their secret (private) and their blinded secret (public)
    parameters.generate_private_key() # Generate secret r1
    M1_r1  = parameters._private_key  #         secret r1=k1
    M1_br1 = pow(g, M1_r1, p)         # blinded secret br1=bk1 (public)
    parameters.generate_private_key() # Generate secret r2
    M2_r2  = parameters._private_key  #         secret r2
    M2_br2 = pow(g, M2_r2, p)         # blinded secret br2 (public)
    parameters.generate_private_key() # Generate secret r3
    M3_r3  = parameters._private_key  #         secret r3
    M3_br3 = pow(g, M3_r3, p)         # blinded secret br3 (public)
    parameters.generate_private_key() # Generate secret r4
    M4_r4  = parameters._private_key  #         secret r4
    M4_br4 = pow(g, M4_r4, p)         # blinded secret br4 (public)

    #checkpoint2 = datetime.now()
    #print(f"Generating secrets and blinded secrets took {round_up((checkpoint2-checkpoint).total_seconds()*1000)}ms")

    # M1 computes:
    k1  = M1_r1
    bk1 = M1_br1
    k2  = pow(M2_br2, M1_r1, p)
    k3  = pow(M3_br3, k2, p)
    k4  = pow(M4_br4, k3, p)
    group_key = k4

    # M2 computes:
    k2 = pow(bk1, M2_r2, p)
    bk2 = pow(g, k2, p)
    k3 = pow(M3_br3, k2, p)
    k4 = pow(M4_br4, k3, p)
    assert k4 == group_key

    # M3 computes:
    k3 = pow(bk2, M3_r3, p)
    bk3 = pow(g, k3, p)
    k4 = pow(M4_br4, k3, p)
    assert k4 == group_key

    # M4 computes:
    k4 = pow(bk3, M4_r4, p)
    bk4 = pow(g, k4, p)
    assert k4 == group_key

    #checkpoint3 = datetime.now()
    #print(f"Group key computation of all members took {round_up((checkpoint3-checkpoint2).total_seconds()*1000)}ms")
    print(f"Complete duration {round_up((datetime.now()-start).total_seconds()*1000)}ms")

