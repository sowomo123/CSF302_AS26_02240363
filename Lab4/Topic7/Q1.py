
def matrix_multiply(A, B, m):
    if m <= 0:
        raise ValueError("Modulus must be positive")

    n = len(A)

    if n == 0 or any(len(row) != n for row in A):
        raise ValueError("A must be a non-empty square matrix")

    if len(B) != n or any(len(row) != n for row in B):
        raise ValueError("B must be a square matrix of the same size")

    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]

            C[i][j] %= m

    return C


A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]

print(matrix_multiply(A, B, 363))
