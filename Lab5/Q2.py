import random
import time
import matplotlib.pyplot as plt
from copy import deepcopy

# ============== MERGE SORT (from Lab 1) ==============
def merge_sort(arr):
    """
    Merge Sort implementation
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    return merge(left_half, right_half)

def merge(left, right):
    """
    Helper function for Merge Sort
    Merges two sorted arrays into one sorted array
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_wrapper(arr):
    """Wrapper for merge sort that sorts in-place"""
    return merge_sort(arr)

# ============== STABLE COUNTING SORT ==============
def counting_sort(arr, k):
    """
    Stable counting sort for integers in range [0, k]
    Time Complexity: O(n + k)
    Space Complexity: O(n + k)
    """
    n = len(arr)
    
    # Initialize count array
    count = [0] * (k + 1)
    
    # Count occurrences of each element
    for num in arr:
        count[num] += 1
    
    # Convert count to cumulative count
    for i in range(1, k + 1):
        count[i] += count[i - 1]
    
    # Build output array (iterate backwards for stability)
    output = [0] * n
    for i in range(n - 1, -1, -1):
        num = arr[i]
        count[num] -= 1
        output[count[num]] = arr[i]
    
    return output

def counting_sort_stable(arr, k):
    """
    Stable counting sort that works with (key, index) pairs
    Demonstrates stability by preserving original order of equal keys
    """
    n = len(arr)
    
    # Initialize count array
    count = [0] * (k + 1)
    
    # Count occurrences of each key
    for key, _ in arr:
        count[key] += 1
    
    # Convert count to cumulative count
    for i in range(1, k + 1):
        count[i] += count[i - 1]
    
    # Build output array (iterate backwards for stability)
    output = [None] * n
    for i in range(n - 1, -1, -1):
        key, idx = arr[i]
        count[key] -= 1
        output[count[key]] = (key, idx)
    
    return output

# ============== LSD RADIX SORT ==============
def counting_sort_by_digit(arr, exp, base):
    """
    Counting sort based on a specific digit
    Used as a subroutine for radix sort
    """
    n = len(arr)
    output = [0] * n
    count = [0] * base
    
    # Count occurrences of each digit
    for num in arr:
        digit = (num // exp) % base
        count[digit] += 1
    
    # Convert count to cumulative count
    for i in range(1, base):
        count[i] += count[i - 1]
    
    # Build output array (iterate backwards for stability)
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % base
        count[digit] -= 1
        output[count[digit]] = arr[i]
    
    return output

def radix_sort_lsd(arr, base=10):
    """
    LSD Radix Sort using counting sort on each digit
    Time Complexity: O(d * (n + b)) where d is number of digits, b is base
    Space Complexity: O(n + b)
    """
    if not arr:
        return arr
    
    # Find the maximum number to know number of digits
    max_num = max(arr)
    
    # Do counting sort for every digit
    exp = 1
    while max_num // exp > 0:
        arr = counting_sort_by_digit(arr, exp, base)
        exp *= base
    
    return arr

# ============== DATA GENERATORS ==============
def generate_array_fixed_n_varying_k(n, k):
    """Generate array of size n with values in range [0, k]"""
    return [random.randint(0, k) for _ in range(n)]

def generate_array_fixed_k_varying_n(n, k):
    """Generate array of size n with values in range [0, k]"""
    return [random.randint(0, k) for _ in range(n)]

# ============== EXPERIMENT 1: Counting Sort - Fixed n, Varying k ==============
def experiment_counting_sort():
    """
    Fix n = 100,000 and vary k = 10, 10^3, 10^5, 10^7
    Compare counting sort with merge sort
    """
    n = 100000
    k_values = [10, 10**3, 10**5, 10**7]
    
    counting_times = []
    merge_times = []
    
    print("=" * 80)
    print("Experiment 1: Counting Sort vs Merge Sort (Fixed n=100,000, Varying k)")
    print("=" * 80)
    print(f"{'k':<15} {'Counting Sort (ms)':<20} {'Merge Sort (ms)':<20} {'Ratio':<10}")
    print("-" * 80)
    
    for k in k_values:
        # Generate array
        arr = generate_array_fixed_n_varying_k(n, k)
        arr_copy = arr.copy()
        
        # Measure counting sort
        start = time.perf_counter()
        sorted_arr = counting_sort(arr, k)
        counting_time = (time.perf_counter() - start) * 1000
        
        # Verify sorted
        assert sorted_arr == sorted(arr_copy), "Counting sort failed"
        
        # Measure merge sort
        start = time.perf_counter()
        sorted_arr = merge_sort_wrapper(arr_copy)
        merge_time = (time.perf_counter() - start) * 1000
        
        # Verify sorted
        assert sorted_arr == sorted(arr_copy), "Merge sort failed"
        
        counting_times.append(counting_time)
        merge_times.append(merge_time)
        ratio = counting_time / merge_time if merge_time > 0 else 0
        
        print(f"{k:<15} {counting_time:<20.4f} {merge_time:<20.4f} {ratio:<10.4f}")
    
    print("=" * 80)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot([str(k) for k in k_values], counting_times, 'o-', label='Counting Sort', linewidth=2)
    plt.plot([str(k) for k in k_values], merge_times, 's-', label='Merge Sort', linewidth=2)
    plt.xlabel('k (max value)')
    plt.ylabel('Time (ms)')
    plt.title('Counting Sort vs Merge Sort (n=100,000)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('image/Q2_counting_vs_merge.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    return k_values, counting_times, merge_times

# ============== EXPERIMENT 2: Radix Sort vs Merge Sort - Fixed k, Varying n ==============
def experiment_radix_sort():
    """
    Fix k = 10^9 and vary n = 10,000 to 1,000,000
    Compare radix sort (base 10 and base 256) with merge sort
    """
    k = 10**9
    n_values = [10000, 50000, 100000, 500000, 1000000]
    
    radix_base10_times = []
    radix_base256_times = []
    merge_times = []
    
    print("=" * 80)
    print("Experiment 2: Radix Sort vs Merge Sort (Fixed k=10^9, Varying n)")
    print("=" * 80)
    print(f"{'n':<12} {'Radix Base 10 (ms)':<20} {'Radix Base 256 (ms)':<20} {'Merge Sort (ms)':<20}")
    print("-" * 80)
    
    for n in n_values:
        # Generate array
        arr = generate_array_fixed_k_varying_n(n, k)
        arr_copy1 = arr.copy()
        arr_copy2 = arr.copy()
        arr_copy3 = arr.copy()
        
        # Measure radix sort base 10
        start = time.perf_counter()
        sorted_arr = radix_sort_lsd(arr_copy1, base=10)
        radix_base10_time = (time.perf_counter() - start) * 1000
        
        # Verify sorted
        assert sorted_arr == sorted(arr_copy1), "Radix sort base 10 failed"
        
        # Measure radix sort base 256
        start = time.perf_counter()
        sorted_arr = radix_sort_lsd(arr_copy2, base=256)
        radix_base256_time = (time.perf_counter() - start) * 1000
        
        # Verify sorted
        assert sorted_arr == sorted(arr_copy2), "Radix sort base 256 failed"
        
        # Measure merge sort
        start = time.perf_counter()
        sorted_arr = merge_sort_wrapper(arr_copy3)
        merge_time = (time.perf_counter() - start) * 1000
        
        # Verify sorted
        assert sorted_arr == sorted(arr_copy3), "Merge sort failed"
        
        radix_base10_times.append(radix_base10_time)
        radix_base256_times.append(radix_base256_time)
        merge_times.append(merge_time)
        
        print(f"{n:<12} {radix_base10_time:<20.4f} {radix_base256_time:<20.4f} {merge_time:<20.4f}")
    
    print("=" * 80)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, radix_base10_times, 'o-', label='Radix Sort (Base 10)', linewidth=2)
    plt.plot(n_values, radix_base256_times, 's-', label='Radix Sort (Base 256)', linewidth=2)
    plt.plot(n_values, merge_times, '^-', label='Merge Sort', linewidth=2)
    plt.xlabel('n (array size)')
    plt.ylabel('Time (ms)')
    plt.title('Radix Sort vs Merge Sort (k=10^9)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('image/Q2_radix_vs_merge.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    return n_values, radix_base10_times, radix_base256_times, merge_times

# ============== DEMONSTRATE STABILITY OF COUNTING SORT ==============
def demonstrate_stability():
    """
    Demonstrate that counting sort is stable by sorting (key, original index) pairs
    """
    print("=" * 80)
    print("Demonstrating Stability of Counting Sort")
    print("=" * 80)
    
    # Create array with duplicate keys and original indices
    arr = [(5, 0), (3, 1), (5, 2), (1, 3), (3, 4), (5, 5), (1, 6), (3, 7)]
    k = 5
    
    print("\nOriginal array (key, original index):")
    print(arr)
    
    # Sort using stable counting sort
    sorted_arr = counting_sort_stable(arr, k)
    
    print("\nSorted array (key, original index):")
    print(sorted_arr)
    
    # Verify stability: for equal keys, original indices should be in ascending order
    print("\nStability check indices for each key:")
    current_key = None
    prev_index = -1
    is_stable = True
    
    for key, idx in sorted_arr:
        if key != current_key:
            if current_key is not None:
                print(f"  Key {current_key}: indices in order")
            current_key = key
            prev_index = idx
        else:
            if idx < prev_index:
                is_stable = False
                print(f"  ERROR: Key {key} has indices out of order!")
            prev_index = idx
    
    if current_key is not None:
        print(f"  Key {current_key}: indices in order")
    
    print(f"\nCounting sort is stable: {is_stable}")
    print("=" * 80)
    
    return is_stable

# ============== MAIN FUNCTION ==============
def main():
    # Create image directory if it doesn't exist
    import os
    os.makedirs('image', exist_ok=True)
    
    # Demonstrate stability
    demonstrate_stability()
    print()
    
    # Run experiment 1: Counting sort with varying k
    k_values, counting_times, merge_times = experiment_counting_sort()
    print()
    
    # Run experiment 2: Radix sort with varying n
    n_values, radix_base10_times, radix_base256_times, merge_times2 = experiment_radix_sort()
    print()
    
    # Analysis
    print("=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    print("When do linear-time sorts win?")
    print("-" * 80)
    print("1. Counting Sort wins when k is small relative to n")
    print("   - Time complexity: O(n + k)")
    print("   - When k << n, the O(k) term is negligible")
    print("   - For n=100,000: wins at k=10 and k=10^3")
    print()
    print("2. Counting Sort loses when k is large")
    print("   - When k >> n, the O(k) term dominates")
    print("   - Memory usage also becomes prohibitive (O(k) space)")
    print("   - For n=100,000: loses at k=10^5 and k=10^7")
    print()
    print("3. Radix Sort wins when:")
    print("   - The range of values is large but number of digits is small")
    print("   - Base 256 is faster than base 10 (fewer passes)")
    print("   - For large n with large k, radix sort outperforms merge sort")
    print()
    print("4. Radix Sort loses when:")
    print("   - Number of digits is large (many passes required)")
    print("   - n is very small (overhead of digit extraction)")
    print()
    print("5. Merge Sort is consistent:")
    print("   - Always O(n log n) regardless of input range")
    print("   - Works well when k is very large or unknown")
    print("   - More memory efficient than counting sort for large k")
    print("=" * 80)

if __name__ == "__main__":
    main()
