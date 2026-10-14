
def binary_mod_exp(a, b, m):
    if m <= 0:
        raise ValueError("Modulus must be positive")
    if b < 0:
        raise ValueError("Exponent must be non-negative")

    result = 1 % m
    a = a % m

    while b > 0:
        if b % 2 == 1:
            result = (result * a) % m

        a = (a * a) % m
        b = b // 2

    return result


print("Binary result:", binary_mod_exp(363, 5, 7))
