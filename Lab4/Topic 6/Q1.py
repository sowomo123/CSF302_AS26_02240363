
def naive_mod_exp(a, b, m):
    if m <= 0:
        raise ValueError("Modulus must be positive")
    if b < 0:
        raise ValueError("Exponent must be non-negative")

    result = 1 % m

    for _ in range(b):
        result = (result * a) % m

    return result


print("Naive result:", naive_mod_exp(363, 5, 7))
