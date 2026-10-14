# Q4: Comparing arithmetic vs bitwise operations in binary modular exponentiation

def binary_mod_exp_arithmetic(a, b, m):
    """Using arithmetic operations (%) and (//)"""
    if m <= 0:
        raise ValueError("Modulus must be positive")
    if b < 0:
        raise ValueError("Exponent must be non-negative")

    result = 1 % m
    a = a % m

    while b > 0:
        if b % 2 == 1:  # Check if odd using modulo
            result = (result * a) % m

        a = (a * a) % m
        b = b // 2  # Integer division

    return result


def binary_mod_exp_bitwise(a, b, m):
    """Using bitwise operations (&) and (>>=)"""
    if m <= 0:
        raise ValueError("Modulus must be positive")
    if b < 0:
        raise ValueError("Exponent must be non-negative")

    result = 1 % m
    a = a % m

    while b > 0:
        if b & 1:  # Check if odd using bitwise AND
            result = (result * a) % m

        a = (a * a) % m
        b >>= 1  # Right shift (divide by 2)

    return result


# Test both implementations
tests = [
    (363, 5, 7),
    (363, 10, 13),
    (2, 363, 17),
    (-363, 5, 11),
    (10, 0, 7)
]

print("Comparing Arithmetic vs Bitwise Operations:\n")
for a, b, m in tests:
    arithmetic = binary_mod_exp_arithmetic(a, b, m)
    bitwise = binary_mod_exp_bitwise(a, b, m)

    print(f"a={a}, b={b}, m={m}")
    print("Arithmetic:", arithmetic)
    print("Bitwise:", bitwise)
    print("Match:", arithmetic == bitwise)
    print()
