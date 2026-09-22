"""
Lab 3 - Q2: Karatsuba's Algorithm for Large Integer Multiplication
----------------------------------------------------------------------
Compares grade-school O(n^2) multiplication against Karatsuba's
divide-and-conquer algorithm (3 multiplications per split) on very
large integers represented as digit strings/arrays.

Random seed = 363
"""

import random
import time

random.seed(363)  # as requested, seeded with 363


# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------
def generate_number_str(num_digits):
    """Generate a random positive integer with exactly num_digits digits,
    returned as a string (no leading zero unless num_digits == 1)."""
    if num_digits == 1:
        return str(random.randint(0, 9))
    first = str(random.randint(1, 9))
    rest = "".join(str(random.randint(0, 9)) for _ in range(num_digits - 1))
    return first + rest


def next_power_of_2(n):
    p = 1
    while p < n:
        p *= 2
    return p


def pad_left(s, length):
    """Pad a digit string on the left with zeros to reach `length`."""
    return s.zfill(length)


# ---------------------------------------------------------------------
# 1. Traditional grade-school multiplication -> O(n^2)
#    Operates directly on digit arrays (most significant digit first).
# ---------------------------------------------------------------------
def traditional_multiply(num1_str, num2_str):
    d1 = [int(c) for c in num1_str][::-1]   # least significant digit first
    d2 = [int(c) for c in num2_str][::-1]
    n1, n2 = len(d1), len(d2)

    result = [0] * (n1 + n2)

    for i in range(n1):
        carry = 0
        for j in range(n2):
            result[i + j] += d1[i] * d2[j] + carry
            carry = result[i + j] // 10
            result[i + j] %= 10
        result[i + n2] += carry

    # remove leading zeros (result is least-significant-first)
    while len(result) > 1 and result[-1] == 0:
        result.pop()

    return "".join(str(d) for d in result[::-1])


# ---------------------------------------------------------------------
# 2. Karatsuba's Algorithm -> O(n^log2(3)) ~= O(n^1.585)
# ---------------------------------------------------------------------
def add_str_numbers(a, b):
    """Add two non-negative integers given as strings."""
    return str(int(a) + int(b))


def sub_str_numbers(a, b):
    """Subtract b from a (a >= b assumed), both given as strings."""
    return str(int(a) - int(b))


def karatsuba_multiply(x_str, y_str):
    # Pad both operands to the same length, then to the next power of 2
    n = max(len(x_str), len(y_str))
    n = next_power_of_2(n)
    x_str = pad_left(x_str, n)
    y_str = pad_left(y_str, n)

    result = _karatsuba(x_str, y_str)
    return str(int(result))  # strip any leading zeros from the final answer


def _karatsuba(x_str, y_str):
    n = len(x_str)

    # Base case: small enough to multiply directly
    if n == 1:
        return str(int(x_str) * int(y_str))

    mid = n // 2

    # Split x = x_high * 10^mid + x_low ; same for y
    x_high, x_low = x_str[:n - mid], x_str[n - mid:]
    y_high, y_low = y_str[:n - mid], y_str[n - mid:]

    # 3 recursive multiplications instead of 4
    z2 = _karatsuba(pad_left(x_high, mid), pad_left(y_high, mid))            # x_high * y_high
    z0 = _karatsuba(pad_left(x_low, mid), pad_left(y_low, mid))              # x_low  * y_low

    sum_x = add_str_numbers(x_high, x_low)
    sum_y = add_str_numbers(y_high, y_low)
    z1_full = str(int(sum_x) * int(sum_y)) if len(sum_x) == 1 or len(sum_y) == 1 \
        else _karatsuba(pad_left(sum_x, mid + 1), pad_left(sum_y, mid + 1))
    # z1 = (x_high+x_low)*(y_high+y_low) - z2 - z0
    z1 = sub_str_numbers(sub_str_numbers(z1_full, z2), z0)

    # result = z2 * 10^(2*mid) + z1 * 10^mid + z0
    result = int(z2) * (10 ** (2 * mid)) + int(z1) * (10 ** mid) + int(z0)
    return str(result)


# ---------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------
def run_comparison(num_digits):
    print("=" * 70)
    print(f" Number size: {num_digits} digits   (random seed = 363)")
    print("=" * 70)

    x = generate_number_str(num_digits)
    y = generate_number_str(num_digits)

    if num_digits <= 16:
        print(f"X = {x}")
        print(f"Y = {y}")

    # --- Traditional method ---
    start = time.perf_counter()
    result_trad = traditional_multiply(x, y)
    trad_time = time.perf_counter() - start

    # --- Karatsuba's method ---
    start = time.perf_counter()
    result_karatsuba = karatsuba_multiply(x, y)
    karatsuba_time = time.perf_counter() - start

    # --- Ground truth (Python's built-in bigint multiply) ---
    ground_truth = str(int(x) * int(y))

    match_trad = (result_trad == ground_truth)
    match_karatsuba = (result_karatsuba == ground_truth)

    if num_digits <= 16:
        print(f"\nTraditional result : {result_trad}")
        print(f"Karatsuba result   : {result_karatsuba}")

    print("\n--- Performance ---")
    print(f"Traditional method time : {trad_time:.6f} sec")
    print(f"Karatsuba's method time  : {karatsuba_time:.6f} sec")
    print(f"Traditional matches ground truth : {match_trad}")
    print(f"Karatsuba matches ground truth   : {match_karatsuba}")
    print()

    return trad_time, karatsuba_time, match_trad and match_karatsuba


if __name__ == "__main__":
    sizes = [8, 16, 32, 64, 128, 256, 512, 1024]
    summary = []

    for size in sizes:
        t_trad, t_karat, ok = run_comparison(size)
        summary.append((size, t_trad, t_karat, ok))

    print("=" * 70)
    print(" SUMMARY")
    print("=" * 70)
    print(f"{'digits':>8} | {'Traditional (s)':>16} | {'Karatsuba (s)':>14} | {'Match':>6}")
    print("-" * 70)
    for size, t_trad, t_karat, ok in summary:
        print(f"{size:>8} | {t_trad:>16.6f} | {t_karat:>14.6f} | {str(ok):>6}")