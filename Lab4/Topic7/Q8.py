from Q4 import binary_matrix_exp

def count_walks(A, k, start, end, m):
    n = len(A)

    if k < 0:
        raise ValueError("Number of edges must be non-negative")
    if m <= 0:
        raise ValueError("Modulus must be positive")
    if not (0 <= start < n and 0 <= end < n):
        raise ValueError("Invalid vertex index")

    powered = binary_matrix_exp(A, k, m)
    return powered[start][end]


A = [
    [0, 1, 0],
    [0, 0, 1],
    [0, 0, 0]
]

print("Walks of 2 edges from 0 to 2:",
      count_walks(A, 2, 0, 2, 363))

print("Walks of 1 edge from 0 to 2:",
      count_walks(A, 1, 0, 2, 363))
