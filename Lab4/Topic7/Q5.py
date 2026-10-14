from Q3 import naive_matrix_exp
from Q4 import binary_matrix_exp

A = [[1, 2], [3, 4]]
B = [[1, 1], [1, 0]]
C = [[2, 0], [0, 2]]

tests = [
    (A, 3, 363),
    (B, 10, 17),
    (C, 5, 11),
    (B, 0, 7)
]

for matrix, exponent, modulus in tests:
    naive = naive_matrix_exp(matrix, exponent, modulus)
    binary = binary_matrix_exp(matrix, exponent, modulus)

    print("Matrix:", matrix)
    print("Exponent:", exponent)
    print("Naive:", naive)
    print("Binary:", binary)
    print("Match:", naive == binary)
    print()
