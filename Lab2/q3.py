import random

# Use 363 as the maximum value for matrix elements
MAX_VALUE = 363


def create_matrix(n):
    matrix = []

    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.randint(1, MAX_VALUE))
        matrix.append(row)

    return matrix


def display_matrix(matrix):
    for row in matrix:
        print(row)


def matrix_multiply(A, B):
    n = len(A)

    # Result matrix filled with 0
    C = [[0 for j in range(n)] for i in range(n)]

    steps = 0

    for i in range(n):
        for j in range(n):
            for k in range(n):

                C[i][j] += A[i][k] * B[k][j]

                # Count multiplication and addition
                steps += 2

    return C, steps


# Main program
print("===== SQUARE MATRIX MULTIPLICATION =====")

n = int(input("Enter matrix size (2, 4, 8, 16, ...): "))

# Check whether n is a power of 2
if n > 0 and (n & (n - 1)) == 0:

    A = create_matrix(n)
    B = create_matrix(n)

    print("\nMatrix A:")
    display_matrix(A)

    print("\nMatrix B:")
    display_matrix(B)

    C, steps = matrix_multiply(A, B)

    print("\nResultant Matrix:")
    display_matrix(C)

    print("\nMatrix Size:", n, "x", n)
    print("Step/Frequency Count:", steps)

    # Analysis/Conclusion
    # Standard matrix multiplication uses three nested loops.
    # Therefore, its time complexity is O(n^3).
    # For an n x n matrix, there are n^3 multiplications
    # and approximately n^3 additions.

else:
    print("Invalid size.")
    print("Please enter a power of 2 such as 2, 4, 8, 16, 32, ...")