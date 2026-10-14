from Q1 import matrix_multiply
from Q2 import identity_matrix

def binary_matrix_exp(A, n, m):
    if n < 0:
        raise ValueError("Exponent must be non-negative")
    if m <= 0:
        raise ValueError("Modulus must be positive")

    result = identity_matrix(len(A))
    base = [[value % m for value in row] for row in A]

    while n > 0:
        if n & 1:
            result = matrix_multiply(result, base, m)

        base = matrix_multiply(base, base, m)
        n >>= 1

    return result


A = [[1, 2], [3, 4]]

print("Binary matrix result:")
print(binary_matrix_exp(A, 3, 363))
