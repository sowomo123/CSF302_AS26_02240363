from Q1 import matrix_multiply
from Q2 import identity_matrix

def naive_matrix_exp(A, n, m):
    if n < 0:
        raise ValueError("Exponent must be non-negative")
    if m <= 0:
        raise ValueError("Modulus must be positive")

    result = identity_matrix(len(A))

    for _ in range(n):
        result = matrix_multiply(result, A, m)

    return result


A = [[1, 2], [3, 4]]
print(naive_matrix_exp(A, 3, 363))
