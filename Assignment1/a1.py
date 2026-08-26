import random

# MINMAX using Divide and Conquer
def MINMAX(A, lo, hi, counter):
    
    # Base case: one element
    if lo == hi:
        return A[lo], A[lo]

    # Base case: two elements
    if hi == lo + 1:
        counter[0] += 1  # One comparison

        if A[lo] < A[hi]:
            return A[lo], A[hi]
        else:
            return A[hi], A[lo]

    # Divide
    mid = (lo + hi) // 2

    min1, max1 = MINMAX(A, lo, mid, counter)
    min2, max2 = MINMAX(A, mid + 1, hi, counter)

    # Combine: compare minimums
    counter[0] += 1
    if min1 < min2:
        minimum = min1
    else:
        minimum = min2

    # Combine: compare maximums
    counter[0] += 1
    if max1 > max2:
        maximum = max1
    else:
        maximum = max2

    return minimum, maximum


# Test the algorithm
sizes = [8, 64, 512, 4096]

print("DIVIDE-AND-CONQUER MINMAX")
print("-" * 65)
print(f"{'n':>8} {'MIN':>10} {'MAX':>10} {'Comparisons':>15} {'Expected':>15}")
print("-" * 65)

for n in sizes:

    # Generate random numbers using 363 as the seed
    random.seed(363)

    A = [random.randint(1, 363) for _ in range(n)]

    # Comparison counter
    counter = [0]

    # Find minimum and maximum
    minimum, maximum = MINMAX(A, 0, n - 1, counter)

    # Theoretical number of comparisons
    expected = (3 * n) // 2 - 2

    print(f"{n:>8} {minimum:>10} {maximum:>10} "
          f"{counter[0]:>15} {expected:>15}")