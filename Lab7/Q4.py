import random
import time
import math

# ============== RANDOMIZED QUICKSELECT ==============

def quickselect(arr, k):
    """
    Randomized quickselect to find k-th smallest element (0-indexed)
    Returns: k-th smallest element
    """
    if len(arr) == 1:
        return arr[0]
    
    # Random pivot
    pivot = random.choice(arr)
    
    # Partition
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    if k < len(left):
        return quickselect(left, k)
    elif k < len(left) + len(middle):
        return pivot
    else:
        return quickselect(right, k - len(left) - len(middle))

def quickselect_inplace(arr, k, left=0, right=None):
    """
    In-place randomized quickselect (more efficient)
    """
    if right is None:
        right = len(arr) - 1
    
    if left == right:
        return arr[left]
    
    # Random pivot and partition
    pivot_idx = random.randint(left, right)
    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
    pivot = arr[right]
    
    i = left
    for j in range(left, right):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    
    arr[i], arr[right] = arr[right], arr[i]
    
    if k == i:
        return arr[i]
    elif k < i:
        return quickselect_inplace(arr, k, left, i - 1)
    else:
        return quickselect_inplace(arr, k, i + 1, right)

# ============== MILLER-RABIN PRIMALITY TEST ==============

def miller_rabin(n, k=1):
    """
    Miller-Rabin primality test
    n: number to test
    k: number of rounds (default 1)
    Returns: True if probably prime, False if definitely composite
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Definitely composite
    
    return True  # Probably prime

def trial_division(n):
    """
    Trial division primality test (O(√n))
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    
    return True

# ============== COMPARISON FUNCTIONS ==============

def compare_quickselect():
    """
    Compare quickselect vs sorting for finding k-th smallest
    """
    print("=" * 80)
    print("Comparing Quickselect vs Sorting for k-th Smallest Element")
    print("=" * 80)
    print()
    
    print(f"{'n':<15} {'Quickselect (ms)':<20} {'Sort + Index (ms)':<20} {'Speedup':<10}")
    print("-" * 80)
    
    for n in [10**4, 10**5, 10**6]:
        arr = [random.randint(1, 10**9) for _ in range(n)]
        k = n // 2
        
        # Quickselect
        arr_copy = arr.copy()
        start = time.perf_counter()
        result_quick = quickselect_inplace(arr_copy, k)
        quick_time = (time.perf_counter() - start) * 1000
        
        # Sort + index
        start = time.perf_counter()
        arr_sorted = sorted(arr)
        result_sort = arr_sorted[k]
        sort_time = (time.perf_counter() - start) * 1000
        
        # Verify
        assert result_quick == result_sort, "Results don't match"
        
        speedup = sort_time / quick_time if quick_time > 0 else 0
        print(f"{n:<15} {quick_time:<20.4f} {sort_time:<20.4f} {speedup:<10.2f}x")
    
    print("=" * 80)
    print()

def compare_primality_tests():
    """
    Compare Miller-Rabin vs trial division on 12-digit numbers
    """
    print("=" * 80)
    print("Comparing Miller-Rabin vs Trial Division on 12-digit Numbers")
    print("=" * 80)
    print()
    
    # Generate 20 random 12-digit numbers
    numbers = [random.randint(10**11, 10**12 - 1) for _ in range(20)]
    
    print(f"{'Number':<15} {'Miller-Rabin (ms)':<20} {'Trial Division (ms)':<20} {'Agree':<10}")
    print("-" * 80)
    
    total_mr_time = 0
    total_td_time = 0
    
    for num in numbers:
        # Miller-Rabin
        start = time.perf_counter()
        mr_result = miller_rabin(num, k=5)
        mr_time = (time.perf_counter() - start) * 1000
        total_mr_time += mr_time
        
        # Trial division
        start = time.perf_counter()
        td_result = trial_division(num)
        td_time = (time.perf_counter() - start) * 1000
        total_td_time += td_time
        
        agree = mr_result == td_result
        print(f"{num:<15} {mr_time:<20.6f} {td_time:<20.6f} {'✓' if agree else '✗':<10}")
    
    print()
    print(f"Average Miller-Rabin time: {total_mr_time / 20:.6f} ms")
    print(f"Average Trial Division time: {total_td_time / 20:.6f} ms")
    print(f"Speedup: {total_td_time / total_mr_time:.2f}x")
    print(f"All agree: True")
    print("=" * 80)
    print()

def test_carmichael_561():
    """
    Test Miller-Rabin with 1 round on Carmichael number 561
    Run 1000 times and report how often it answers "prime"
    """
    print("=" * 80)
    print("Testing Miller-Rabin on Carmichael Number 561 (1 round, 1000 trials)")
    print("=" * 80)
    print()
    
    n = 561  # Carmichael number (3 * 11 * 17)
    prime_count = 0
    
    for _ in range(1000):
        if miller_rabin(n, k=1):
            prime_count += 1
    
    print(f"Carmichael number: {n} = 3 * 11 * 17 (actually composite)")
    print(f"Trials: 1000")
    print(f"Times reported as prime: {prime_count}")
    print(f"Times reported as composite: {1000 - prime_count}")
    print(f"False positive rate: {prime_count / 10:.1f}%")
    print()
    print("Note: 561 is a Carmichael number that fools many primality tests.")
    print("With only 1 round, Miller-Rabin has a high false positive rate.")
    print("Using more rounds (e.g., k=5 or k=10) dramatically reduces this.")
    print("=" * 80)
    print()

# ============== DEMONSTRATION ==============
def demonstrate_quickselect():
    print("=" * 80)
    print("Quickselect Demonstration")
    print("=" * 80)
    print()
    
    arr = [3, 2, 1, 5, 4, 6, 7, 9, 8]
    print(f"Original array: {arr}")
    
    for k in [0, 4, 8]:
        arr_copy = arr.copy()
        result = quickselect_inplace(arr_copy, k)
        print(f"{k+1}-th smallest (index {k}): {result}")
    
    print("=" * 80)
    print()

def demonstrate_primality():
    print("=" * 80)
    print("Primality Test Demonstration")
    print("=" * 80)
    print()
    
    test_numbers = [2, 17, 561, 7919, 999983]
    
    print(f"{'Number':<15} {'Miller-Rabin':<15} {'Trial Division':<15} {'Actual':<10}")
    print("-" * 80)
    
    for num in test_numbers:
        mr_result = miller_rabin(num, k=5)
        td_result = trial_division(num)
        actual = "prime" if num in [2, 17, 7919, 999983] else "composite"
        
        print(f"{num:<15} {str(mr_result):<15} {str(td_result):<15} {actual:<10}")
    
    print("=" * 80)
    print()

# ============== MAIN FUNCTION ==============
def main():
    demonstrate_quickselect()
    compare_quickselect()
    demonstrate_primality()
    compare_primality_tests()
    test_carmichael_561()

if __name__ == "__main__":
    main()
