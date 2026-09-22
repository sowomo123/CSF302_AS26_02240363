"""
Lab 3 - Q3: Binary Search vs Ternary Search (Menu-Driven Program)
----------------------------------------------------------------------
Menu-driven program that generates a sorted array, searches it with
Binary Search and Ternary Search, and records/compares step (comparison)
counts for best case, worst case, and across increasing n.

Random seed = 363
"""

import random

random.seed(363)  # as requested, seeded with 363

# Global state shared across menu options
array = []


# ---------------------------------------------------------------------
# 1. Array generation / display
# ---------------------------------------------------------------------
def generate_array(n, low=1, high=1000):
    """Generate n random integers and return them sorted."""
    arr = [random.randint(low, high) for _ in range(n)]
    arr.sort()
    return arr


def display_array(arr):
    if not arr:
        print("Array is empty. Please generate an array first (option 1).")
        return
    print(f"\nArray (n = {len(arr)}):")
    print(arr)


# ---------------------------------------------------------------------
# 2. Binary Search  ->  T(n) = T(n/2) + O(1)
# ---------------------------------------------------------------------
def binary_search(arr, key):
    """Returns (index_or_-1, comparison_count)."""
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == key:
            return mid, comparisons
        comparisons += 1
        if arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


# ---------------------------------------------------------------------
# 3. Ternary Search  ->  T(n) = T(n/3) + O(1)
# ---------------------------------------------------------------------
def ternary_search(arr, key):
    """Returns (index_or_-1, comparison_count)."""
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3

        comparisons += 1
        if arr[mid1] == key:
            return mid1, comparisons

        comparisons += 1
        if arr[mid2] == key:
            return mid2, comparisons

        comparisons += 1
        if key < arr[mid1]:
            high = mid1 - 1
        else:
            comparisons += 1
            if key > arr[mid2]:
                low = mid2 + 1
            else:
                low, high = mid1 + 1, mid2 - 1

    return -1, comparisons


# ---------------------------------------------------------------------
# 4. Best / Worst case step counts
# ---------------------------------------------------------------------
def best_case_analysis(arr):
    """Best case: the key found on the very first comparison
    (the first element examined by each algorithm)."""
    if not arr:
        print("Array is empty. Please generate an array first (option 1).")
        return

    n = len(arr)
    mid = (0 + n - 1) // 2
    best_key_binary = arr[mid]
    _, bs_steps = binary_search(arr, best_key_binary)

    mid1 = 0 + (n - 1 - 0) // 3
    best_key_ternary = arr[mid1]
    _, ts_steps = ternary_search(arr, best_key_ternary)

    print(f"\n--- Best Case (n = {n}) ---")
    print(f"Binary Search  : key={best_key_binary:<6} comparisons = {bs_steps}")
    print(f"Ternary Search : key={best_key_ternary:<6} comparisons = {ts_steps}")


def worst_case_analysis(arr):
    """Worst case: key absent from the array, forcing the search
    down to an empty range (maximum number of comparisons)."""
    if not arr:
        print("Array is empty. Please generate an array first (option 1).")
        return

    n = len(arr)
    # A key guaranteed not to be in the array (sorted, so max+1 works)
    absent_key = arr[-1] + 1

    _, bs_steps = binary_search(arr, absent_key)
    _, ts_steps = ternary_search(arr, absent_key)

    print(f"\n--- Worst Case (n = {n}, key absent) ---")
    print(f"Binary Search  : comparisons = {bs_steps}")
    print(f"Ternary Search : comparisons = {ts_steps}")


# ---------------------------------------------------------------------
# 5. Comparison table across increasing n
# ---------------------------------------------------------------------
def comparison_table():
    sizes = [10, 100, 1000, 10000, 100000, 1000000]
    print(f"\n{'n':>10} | {'Binary (worst)':>15} | {'Ternary (worst)':>16}")
    print("-" * 48)

    for n in sizes:
        arr = generate_array(n)
        absent_key = arr[-1] + 1
        _, bs_steps = binary_search(arr, absent_key)
        _, ts_steps = ternary_search(arr, absent_key)
        print(f"{n:>10} | {bs_steps:>15} | {ts_steps:>16}")

    print("""
Explanation (recurrence relations):
  Binary Search:  T(n) = T(n/2) + O(1)  ->  T(n) = O(log2 n)
  Ternary Search: T(n) = T(n/3) + O(2)  ->  T(n) = O(2 * log3 n)

  Even though ternary search shrinks the search space faster per
  step (dividing by 3 instead of 2), it makes 2 comparisons per
  level of recursion vs binary search's 1. Since log3(n) is only
  about 0.63 * log2(n), the total comparisons work out to:

      Binary  ~= log2(n)
      Ternary ~= 2 * log3(n) = 2 * log2(n)/log2(3) ~= 1.26 * log2(n)

  So Ternary Search actually performs MORE comparisons than Binary
  Search for the same n, despite splitting into 3 parts. This is
  why binary search is generally preferred in practice.
""")


# ---------------------------------------------------------------------
# Menu driver
# ---------------------------------------------------------------------
def print_menu():
    print("\n" + "=" * 55)
    print(" Binary Search vs Ternary Search - Menu")
    print(" (random seed = 363)")
    print("=" * 55)
    print("1. Generate n sorted random numbers -> Array")
    print("2. Display Array")
    print("3. Search for a key using Binary Search")
    print("4. Search for a key using Ternary Search")
    print("5. Step/frequency count for BEST case")
    print("6. Step/frequency count for WORST case")
    print("7. Step/frequency count comparison table across increasing n")
    print("8. Exit")


def main():
    global array

    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            n = int(input("Enter number of elements (n): "))
            array = generate_array(n)
            print(f"Generated a sorted array of {n} random integers.")

        elif choice == "2":
            display_array(array)

        elif choice == "3":
            if not array:
                print("Array is empty. Please generate an array first (option 1).")
                continue
            key = int(input("Enter key to search: "))
            idx, steps = binary_search(array, key)
            if idx != -1:
                print(f"Found {key} at index {idx}. Comparisons made: {steps}")
            else:
                print(f"{key} not found. Comparisons made: {steps}")

        elif choice == "4":
            if not array:
                print("Array is empty. Please generate an array first (option 1).")
                continue
            key = int(input("Enter key to search: "))
            idx, steps = ternary_search(array, key)
            if idx != -1:
                print(f"Found {key} at index {idx}. Comparisons made: {steps}")
            else:
                print(f"{key} not found. Comparisons made: {steps}")

        elif choice == "5":
            best_case_analysis(array)

        elif choice == "6":
            worst_case_analysis(array)

        elif choice == "7":
            comparison_table()

        elif choice == "8":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
    