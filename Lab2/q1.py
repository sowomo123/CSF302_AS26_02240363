import time
import math
import matplotlib.pyplot as plt


# Naive Method
def naive_prime(n):
    steps = 0

    if n < 2:
        return False, steps

    for i in range(2, n):
        steps += 1
        if n % i == 0:
            return False, steps

    return True, steps


# Optimized Method
def optimized_prime(n):
    steps = 0

    if n < 2:
        return False, steps

    for i in range(2, int(math.sqrt(n)) + 1):
        steps += 1
        if n % i == 0:
            return False, steps

    return True, steps


# Take at least 10 numbers
numbers = []

print("Enter at least 10 numbers.")
print("Example: 363")

for i in range(10):
    n = int(input(f"Enter number {i + 1}: "))
    numbers.append(n)


naive_steps = []
optimized_steps = []
naive_times = []
optimized_times = []

print("\n========== RESULTS ==========")

for n in numbers:

    # Naive method timing
    start = time.perf_counter()
    naive_result, n_steps = naive_prime(n)
    end = time.perf_counter()

    naive_time = end - start

    # Optimized method timing
    start = time.perf_counter()
    optimized_result, o_steps = optimized_prime(n)
    end = time.perf_counter()

    optimized_time = end - start

    naive_steps.append(n_steps)
    optimized_steps.append(o_steps)
    naive_times.append(naive_time)
    optimized_times.append(optimized_time)

    print(f"\nNumber: {n}")
    print(f"Naive Method:     {'Prime' if naive_result else 'Not Prime'}")
    print(f"Naive Steps:      {n_steps}")
    print(f"Naive Time:       {naive_time:.10f} seconds")

    print(f"Optimized Method: {'Prime' if optimized_result else 'Not Prime'}")
    print(f"Optimized Steps:  {o_steps}")
    print(f"Optimized Time:   {optimized_time:.10f} seconds")


# Step/Frequency comparison graph
x = range(len(numbers))

plt.figure(figsize=(10, 6))

plt.plot(x, naive_steps, marker='o', label='Naive Method')
plt.plot(x, optimized_steps, marker='o', label='Optimized Method')

plt.xticks(x, numbers)
plt.xlabel("Input Number")
plt.ylabel("Number of Steps")
plt.title("Prime Testing: Naive vs Optimized Method")
plt.legend()
plt.grid(True)

plt.show()


# Time comparison graph
plt.figure(figsize=(10, 6))

plt.plot(x, naive_times, marker='o', label='Naive Method')
plt.plot(x, optimized_times, marker='o', label='Optimized Method')

plt.xticks(x, numbers)
plt.xlabel("Input Number")
plt.ylabel("Time (seconds)")
plt.title("Execution Time: Naive vs Optimized Method")
plt.legend()
plt.grid(True)

plt.show()