import mpmath

# A.1.  ffdhe2048 for TLS FFC
# The 2048-bit group has registry value 256 and is calculated from the following formula:
# The modulus is:

mpmath.mp.dps = 100000  # Set the desired decimal precision
p = mpmath.power(2, 2048) - mpmath.power(2, 1984) + (mpmath.floor(mpmath.power(2, 1918) * mpmath.e) + 560316) * mpmath.power(2, 64) - 1
q = (p-1)/2
g = 2

p_bit_length = int(p).bit_length()
q_bit_length = int(q).bit_length()

print(p_bit_length)
print(q_bit_length)