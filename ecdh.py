# RFC 5903 256-Bit Random ECP Group page 4
# NIST.SP.800-56Ar3 Key Pair Generation Using Extra Random Bits page 30
import sympy
import os

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

def is_on_curve(point):
    """Returns True if the given point lies on the elliptic curve."""
    if point is None:
        # None represents the point at infinity.
        return True

    x, y = point
    return (y**2 - x**3 + 3*x - group_b) % group_prime == 0 # (y^2 - x^3 + 3x - b) % p == 0


def point_neg(point):
    """Returns -point."""
    assert is_on_curve(point)

    if point is None:
        # -0 = 0
        return None

    x, y = point
    result = (x, -y % group_prime)
    assert is_on_curve(result)
    return result


def point_add(point1, point2):
    """Returns the result of point1 + point2 according to the group law."""
    assert is_on_curve(point1)
    assert is_on_curve(point2)

    if point1 is None:
        # 0 + point2 = point2
        return point2
    if point2 is None:
        # point1 + 0 = point1
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        # point1 + (-point1) = 0
        return None

    if x1 == x2:
        # This is the case point1 == point2.
        m = (3 * x1 * x1 + a) * sympy.mod_inverse(2 * y1, group_prime)
    else:
        # This is the case point1 != point2.
        m = (y1 - y2) * sympy.mod_inverse(x1 - x2, group_prime)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % group_prime,
              -y3 % group_prime)

    assert is_on_curve(result)
    return result


def scalar_mult(k, point):
    """Returns k * point computed using the double and point_add algorithm."""
    assert is_on_curve(point)

    if k % group_order == 0 or point is None:
        return None

    if k < 0:
        # k * point = -k * (-point)
        return scalar_mult(-k, point_neg(point))

    result = None
    addend = point

    while k:
        if k & 1:
            # Add.
            result = point_add(result, addend)

        # Double.
        addend = point_add(addend, addend)

        k >>= 1

    assert is_on_curve(result)
    return result


L = group_order.bit_length() + 64
c = int.from_bytes(os.urandom(max(s, L) // 8))
assert c > 0 and c < (pow(2, max(s, L)) - 1)
d = (c % (group_order - 1)) + 1
Q = scalar_mult(d, (gx, gy))
y_squared = pow(Q[1], 2, group_prime)
assert y_squared == ecurve.subs([(x, Q[0]),(b, group_b)]) % group_prime