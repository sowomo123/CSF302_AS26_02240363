from Q4 import binary_matrix_exp

def fibonacci_mod(n, m):
    if n < 0:
        raise ValueError("n must be non-negative")
    if m <= 0:
        raise ValueError("Modulus must be positive")

    Q = [[1, 1], [1, 0]]
    result = binary_matrix_exp(Q, n, m)

    return result[1][0]


for n in [0, 1, 5, 10, 363]:
    print(f"F({n}) mod 363 =", fibonacci_mod(n, 363))
