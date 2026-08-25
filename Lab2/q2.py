import random
import time

array = []


# Merge function
def merge(arr, left, mid, right):
    steps = 0

    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]

    i = 0
    j = 0
    k = left

    while i < len(L) and j < len(R):
        steps += 1

        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1

        k += 1

    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
        steps += 1

    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1
        steps += 1

    return steps


# Merge Sort
def merge_sort(arr, left, right):
    steps = 0

    if left < right:
        mid = (left + right) // 2

        steps += merge_sort(arr, left, mid)
        steps += merge_sort(arr, mid + 1, right)

        steps += merge(arr, left, mid, right)

    return steps


# Menu
while True:

    print("\n===== MERGE SORT MENU =====")
    print("1. Generate n random numbers")
    print("2. Display Array")
    print("3. Sort in Ascending Order using Merge Sort")
    print("4. Sort in Descending Order")
    print("5. Time Complexity for ascending random data")
    print("6. Time Complexity for ascending already sorted data")
    print("7. Time Complexity for ascending descending-sorted data")
    print("8. Exit")

    choice = int(input("Enter your choice: "))

    # 1. Generate random array
    if choice == 1:
        n = 363
        array = [random.randint(1, 1000) for _ in range(n)]
        print("Generated", n, "random numbers.")

    # 2. Display array
    elif choice == 2:
        if len(array) == 0:
            print("Array is empty.")
        else:
            print("Array:")
            print(array)

    # 3. Ascending Merge Sort
    elif choice == 3:
        if len(array) == 0:
            print("Generate the array first.")
        else:
            arr = array.copy()

            start = time.perf_counter()
            steps = merge_sort(arr, 0, len(arr) - 1)
            end = time.perf_counter()

            print("Ascending Sorted Array:")
            print(arr)
            print("Steps/Frequency Count:", steps)
            print("Time:", end - start, "seconds")

    # 4. Descending sort
    elif choice == 4:
        if len(array) == 0:
            print("Generate the array first.")
        else:
            arr = array.copy()

            start = time.perf_counter()
            arr.sort(reverse=True)
            end = time.perf_counter()

            print("Descending Sorted Array:")
            print(arr)
            print("Time:", end - start, "seconds")

    # 5. Random data
    elif choice == 5:
        arr = [random.randint(1, 1000) for _ in range(363)]

        start = time.perf_counter()
        steps = merge_sort(arr, 0, len(arr) - 1)
        end = time.perf_counter()

        print("Random Data - 363 elements")
        print("Steps/Frequency Count:", steps)
        print("Time:", end - start, "seconds")

    # 6. Already sorted data
    elif choice == 6:
        arr = list(range(1, 364))

        start = time.perf_counter()
        steps = merge_sort(arr, 0, len(arr) - 1)
        end = time.perf_counter()

        print("Already Sorted Data - 363 elements")
        print("Steps/Frequency Count:", steps)
        print("Time:", end - start, "seconds")

    # 7. Descending data
    elif choice == 7:
        arr = list(range(363, 0, -1))

        start = time.perf_counter()
        steps = merge_sort(arr, 0, len(arr) - 1)
        end = time.perf_counter()

        print("Descending Data - 363 elements")
        print("Steps/Frequency Count:", steps)
        print("Time:", end - start, "seconds")

    # 8. Exit
    elif choice == 8:
        print("Program ended.")
        break

    else:
        print("Invalid choice.")