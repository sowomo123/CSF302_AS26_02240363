
def identity_matrix(n):
    if n <= 0:
        raise ValueError("Dimension must be positive")

    I = [[0] * n for _ in range(n)]

    for i in range(n):
        I[i][i] = 1

    return I


print(identity_matrix(3))
