import random
import time
import statistics

def bubble_sort(arr):
    """
    Bubble Sort implementation
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

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

def generate_random_array(size):
    """
    Generate a random array of given size
    Values range from 0 to size * 10
    """
    return [random.randint(0, size * 10) for _ in range(size)]

def measure_execution_time(sort_function, arr):
    """
    Measure execution time of a sort function
    Returns time in milliseconds
    """
    arr_copy = arr.copy()
    start_time = time.perf_counter()
    sort_function(arr_copy)
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000  # Convert to milliseconds

def average_execution_time(sort_function, array_size, num_runs=10):
    """
    Measure average execution time over multiple runs
    """
    times = []
    for _ in range(num_runs):
        arr = generate_random_array(array_size)
        time_taken = measure_execution_time(sort_function, arr)
        times.append(time_taken)
    return statistics.mean(times)

def main():
    """
    Main function to run the sorting algorithm benchmark
    """
    input_sizes = [100, 500, 1000, 2000, 4000, 8000]
    num_runs = 10
    
    print("=" * 80)
    print("Sorting Algorithm Performance Comparison")
    print("=" * 80)
    print(f"Number of runs per measurement: {num_runs}")
    print(f"Input sizes: {input_sizes}")
    print("=" * 80)
    print()
    
    print(f"{'Input Size':<12} {'Bubble Sort (ms)':<20} {'Merge Sort (ms)':<20} {'Ratio':<10}")
    print("-" * 80)
    
    for size in input_sizes:
        bubble_avg = average_execution_time(bubble_sort, size, num_runs)
        merge_avg = average_execution_time(merge_sort, size, num_runs)
        ratio = bubble_avg / merge_avg if merge_avg > 0 else 0
        
        print(f"{size:<12} {bubble_avg:<20.4f} {merge_avg:<20.4f} {ratio:<10.2f}")
    
    print("=" * 80)
    print()
    print("Analysis:")
    print("- Bubble Sort has O(n^2) time complexity - execution time grows quadratically")
    print("- Merge Sort has O(n log n) time complexity - execution time grows more slowly")
    print("- As input size increases, Merge Sort becomes significantly faster")
    print("=" * 80)

if __name__ == "__main__":
    main()
