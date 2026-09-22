"""
Lab 3 - Q1: Matrix Multiplication - Strassen's vs Traditional
----------------------------------------------------------------
Compares the traditional O(n^3) triple-loop method against
Strassen's divide-and-conquer algorithm (7 multiplications per split).

Random seed = 363
"""

import random
import time
import copy

random.seed(363)  # as requested, seeded with 363


# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------
def generate_matrix(n, low=0, high=9):
    """Generate an n x n matrix with random integers."""
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def print_matrix(M, name="Matrix"):
    print(f"\n{name}:")
    for row in M:
        print(" ".join(f"{val:4}" for val in row))


def matrices_equal(A, B):
    n = len(A)
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))


def is_power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0


# ---------------------------------------------------------------------
# 1. Traditional Matrix Multiplication  -> O(n^3)
# ---------------------------------------------------------------------
def traditional_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C


# ---------------------------------------------------------------------
# 2. Strassen's Algorithm -> O(n^log2(7)) ~= O(n^2.81)
# ---------------------------------------------------------------------
def add_matrix(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub_matrix(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split_matrix(M):
    """Split M into 4 equal quadrants."""
    n = len(M)
    mid = n // 2
    A11 = [row[:mid] for row in M[:mid]]
    A12 = [row[mid:] for row in M[:mid]]
    A21 = [row[:mid] for row in M[mid:]]
    A22 = [row[mid:] for row in M[mid:]]
    return A11, A12, A21, A22


def combine_quadrants(C11, C12, C21, C22):
    """Combine 4 quadrants back into a single matrix."""
    top = [r1 + r2 for r1, r2 in zip(C11, C12)]
    bottom = [r1 + r2 for r1, r2 in zip(C21, C22)]
    return top + bottom


def strassen_multiply(A, B):
    n = len(A)

    # Base case: 1x1 matrix
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    # 7 recursive multiplications
    M1 = strassen_multiply(add_matrix(A11, A22), add_matrix(B11, B22))
    M2 = strassen_multiply(add_matrix(A21, A22), B11)
    M3 = strassen_multiply(A11, sub_matrix(B12, B22))
    M4 = strassen_multiply(A22, sub_matrix(B21, B11))
    M5 = strassen_multiply(add_matrix(A11, A12), B22)
    M6 = strassen_multiply(sub_matrix(A21, A11), add_matrix(B11, B12))
    M7 = strassen_multiply(sub_matrix(A12, A22), add_matrix(B21, B22))

    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(sub_matrix(add_matrix(M1, M3), M2), M6)

    return combine_quadrants(C11, C12, C21, C22)


# ---------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------
def run_comparison(n):
    if not is_power_of_2(n):
        raise ValueError("Matrix size must be a power of 2 (2, 4, 8, 16, ...)")

    print("=" * 60)
    print(f" Matrix size: {n} x {n}   (random seed = 363)")
    print("=" * 60)

    A = generate_matrix(n)
    B = generate_matrix(n)

    if n <= 8:
        print_matrix(A, "Matrix A")
        print_matrix(B, "Matrix B")

    # --- Traditional method ---
    start = time.perf_counter()
    C_trad = traditional_multiply(copy.deepcopy(A), copy.deepcopy(B))
    trad_time = time.perf_counter() - start

    # --- Strassen's method ---
    start = time.perf_counter()
    C_strassen = strassen_multiply(copy.deepcopy(A), copy.deepcopy(B))
    strassen_time = time.perf_counter() - start

    if n <= 8:
        print_matrix(C_trad, "Result - Traditional Method")
        print_matrix(C_strassen, "Result - Strassen's Method")

    match = matrices_equal(C_trad, C_strassen)

    print("\n--- Performance ---")
    print(f"Traditional method time : {trad_time:.6f} sec")
    print(f"Strassen's method time  : {strassen_time:.6f} sec")
    print(f"Results match           : {match}")
    print()

    return trad_time, strassen_time, match


if __name__ == "__main__":
    # Run for several powers-of-2 sizes and compare growth in time
    sizes = [2, 4, 8, 16, 32, 64, 128]
    summary = []

    for size in sizes:
        t_trad, t_strass, ok = run_comparison(size)
        summary.append((size, t_trad, t_strass, ok))

    # Final summary table
    print("=" * 60)
    print(" SUMMARY")
    print("=" * 60)
    print(f"{'n':>6} | {'Traditional (s)':>16} | {'Strassen (s)':>14} | {'Match':>6}")
    print("-" * 60)
    for size, t_trad, t_strass, ok in summary:
        print(f"{size:>6} | {t_trad:>16.6f} | {t_strass:>14.6f} | {str(ok):>6}")