import random
import time
import sys
from collections import defaultdict

# Global counter for comparisons
comparison_count = 0

def reset_comparisons():
    global comparison_count
    comparison_count = 0

def get_comparisons():
    global comparison_count
    return comparison_count

def increment_comparisons():
    global comparison_count
    comparison_count += 1

# ============== LOMUTO PARTITION (last element as pivot) ==============
def lomuto_partition(arr, low, high):
    global comparison_count
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        increment_comparisons()
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort_lomuto(arr, low, high):
    while low < high:
        pivot_idx = lomuto_partition(arr, low, high)
        
        # Recurse on smaller part, loop on larger
        if pivot_idx - low < high - pivot_idx:
            quicksort_lomuto(arr, low, pivot_idx - 1)
            low = pivot_idx + 1
        else:
            quicksort_lomuto(arr, pivot_idx + 1, high)
            high = pivot_idx - 1

def quicksort_lomuto_wrapper(arr):
    reset_comparisons()
    if len(arr) > 1:
        quicksort_lomuto(arr, 0, len(arr) - 1)
    return get_comparisons()

# ============== HOARE PARTITION ==============
def hoare_partition(arr, low, high):
    global comparison_count
    pivot = arr[low]
    i = low - 1
    j = high + 1
    
    while True:
        i += 1
        while arr[i] < pivot:
            increment_comparisons()
            i += 1
        increment_comparisons()
        
        j -= 1
        while arr[j] > pivot:
            increment_comparisons()
            j -= 1
        increment_comparisons()
        
        if i >= j:
            return j
        
        arr[i], arr[j] = arr[j], arr[i]

def quicksort_hoare(arr, low, high):
    while low < high:
        pivot_idx = hoare_partition(arr, low, high)
        
        # Recurse on smaller part, loop on larger
        if pivot_idx - low < high - pivot_idx:
            quicksort_hoare(arr, low, pivot_idx)
            low = pivot_idx + 1
        else:
            quicksort_hoare(arr, pivot_idx + 1, high)
            high = pivot_idx

def quicksort_hoare_wrapper(arr):
    reset_comparisons()
    if len(arr) > 1:
        quicksort_hoare(arr, 0, len(arr) - 1)
    return get_comparisons()

# ============== RANDOMISED QUICKSORT ==============
def randomised_partition(arr, low, high):
    # Random pivot selection
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
    return lomuto_partition(arr, low, high)

def quicksort_randomised(arr, low, high):
    while low < high:
        pivot_idx = randomised_partition(arr, low, high)
        
        # Recurse on smaller part, loop on larger
        if pivot_idx - low < high - pivot_idx:
            quicksort_randomised(arr, low, pivot_idx - 1)
            low = pivot_idx + 1
        else:
            quicksort_randomised(arr, pivot_idx + 1, high)
            high = pivot_idx - 1

def quicksort_randomised_wrapper(arr):
    reset_comparisons()
    if len(arr) > 1:
        quicksort_randomised(arr, 0, len(arr) - 1)
    return get_comparisons()

# ============== THREE-WAY (DUTCH NATIONAL FLAG) QUICKSORT ==============
def three_way_partition(arr, low, high):
    global comparison_count
    pivot = arr[low]
    lt = low
    gt = high
    i = low + 1
    
    while i <= gt:
        increment_comparisons()
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1
        else:
            i += 1
    
    return lt, gt

def quicksort_three_way(arr, low, high):
    while low < high:
        lt, gt = three_way_partition(arr, low, high)
        
        # Recurse on smaller part, loop on larger
        if lt - low < high - gt:
            quicksort_three_way(arr, low, lt - 1)
            low = gt + 1
        else:
            quicksort_three_way(arr, gt + 1, high)
            high = lt - 1

def quicksort_three_way_wrapper(arr):
    reset_comparisons()
    if len(arr) > 1:
        quicksort_three_way(arr, 0, len(arr) - 1)
    return get_comparisons()

# ============== TEST DATA GENERATORS ==============
def generate_random(n):
    return [random.randint(0, n-1) for _ in range(n)]

def generate_sorted(n):
    return list(range(n))

def generate_reverse_sorted(n):
    return list(range(n-1, -1, -1))

def generate_duplicates(n):
    return [random.randint(0, 9) for _ in range(n)]

# ============== EXPERIMENT RUNNER ==============
def run_experiment(sort_func, data_generator, n, trials=5):
    times = []
    comparisons = []
    
    # Reduce trials for sorted/reverse sorted with Lomuto to avoid excessive runtime
    if (data_generator in [generate_sorted, generate_reverse_sorted] and 
        sort_func.__name__ == 'quicksort_lomuto_wrapper' and n >= 4000):
        trials = 1
    
    for _ in range(trials):
        arr = data_generator(n)
        arr_copy = arr.copy()
        
        start_time = time.perf_counter()
        comps = sort_func(arr)
        end_time = time.perf_counter()
        
        elapsed = (end_time - start_time) * 1000  # Convert to milliseconds
        times.append(elapsed)
        comparisons.append(comps)
        
        # Verify sorted
        assert arr == sorted(arr_copy), f"Sort failed for {data_generator.__name__}"
    
    avg_time = sum(times) / trials
    avg_comparisons = sum(comparisons) / trials
    return avg_time, avg_comparisons

def main():
    input_sizes = [1000, 2000, 4000, 8000, 16000]
    data_generators = [
        ("Random", generate_random),
        ("Sorted", generate_sorted),
        ("Reverse Sorted", generate_reverse_sorted),
        ("Duplicates (0-9)", generate_duplicates)
    ]
    
    sort_functions = [
        ("Lomuto", quicksort_lomuto_wrapper),
        ("Hoare", quicksort_hoare_wrapper),
        ("Randomised", quicksort_randomised_wrapper),
        ("Three-way", quicksort_three_way_wrapper)
    ]
    
    # Set recursion limit higher just in case
    sys.setrecursionlimit(100000)
    
    # Cache for results
    results = {}
    
    print("=" * 120)
    print("QUICKSORT VARIANTS COMPARISON")
    print("=" * 120)
    print()
    
    for sort_name, sort_func in sort_functions:
        print(f"\n{sort_name} Partition")
        print("-" * 120)
        print(f"{'Input Type':<20} {'n':>8} {'Time (ms)':>15} {'Comparisons':>15}")
        print("-" * 120)
        
        for gen_name, gen_func in data_generators:
            for n in input_sizes:
                avg_time, avg_comps = run_experiment(sort_func, gen_func, n)
                results[(sort_name, gen_name, n)] = (avg_time, avg_comps)
                print(f"{gen_name:<20} {n:>8} {avg_time:>15.4f} {avg_comps:>15.0f}")
        
        print()
    
    # Summary table for comparisons
    print("\n" + "=" * 120)
    print("SUMMARY: COMPARISON COUNTS")
    print("=" * 120)
    print()
    
    for gen_name, gen_func in data_generators:
        print(f"\n{gen_name}")
        print("-" * 100)
        header = f"{'n':>8}"
        for sort_name, _ in sort_functions:
            header += f" {sort_name:>15}"
        print(header)
        print("-" * 100)
        
        for n in input_sizes:
            row = f"{n:>8}"
            for sort_name, sort_func in sort_functions:
                _, avg_comps = results[(sort_name, gen_name, n)]
                row += f" {avg_comps:>15.0f}"
            print(row)
        print()
    
    # Summary table for time
    print("\n" + "=" * 120)
    print("SUMMARY: EXECUTION TIME (ms)")
    print("=" * 120)
    print()
    
    for gen_name, gen_func in data_generators:
        print(f"\n{gen_name}")
        print("-" * 100)
        header = f"{'n':>8}"
        for sort_name, _ in sort_functions:
            header += f" {sort_name:>15}"
        print(header)
        print("-" * 100)
        
        for n in input_sizes:
            row = f"{n:>8}"
            for sort_name, sort_func in sort_functions:
                avg_time, _ = results[(sort_name, gen_name, n)]
                row += f" {avg_time:>15.4f}"
            print(row)
        print()

if __name__ == "__main__":
    main()
