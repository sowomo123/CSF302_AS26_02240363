import time
import statistics
import math

def naive_trial_division(n):
    """
    Naive Prime Checking using Trial Division
    Checks divisibility by all numbers from 2 to n-1
    Time Complexity: O(n²)
    Space Complexity: O(n)
    """
    if n < 2:
        return []
    
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

def optimized_trial_division(n):
    """
    Optimized Trial Division (checking up to √n)
    Only checks divisibility up to square root of the number
    Time Complexity: O(n√n)
    Space Complexity: O(n)
    """
    if n < 2:
        return []
    
    primes = [2]
    for num in range(3, n + 1, 2):
        is_prime = True
        sqrt_num = math.isqrt(num) + 1
        for p in primes:
            if p > sqrt_num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

def sieve_of_eratosthenes(n):
    """
    Generate primes up to n using Sieve of Eratosthenes
    Time Complexity: O(n log log n)
    Space Complexity: O(n)
    """
    if n < 2:
        return []
    
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, math.isqrt(n) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def measure_execution_time(prime_function, n):
    """
    Measure execution time of a prime generation function
    Returns time in milliseconds
    """
    start_time = time.perf_counter()
    primes = prime_function(n)
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000, len(primes)

def average_execution_time(prime_function, n, num_runs=3):
    """
    Measure average execution time over multiple runs
    """
    times = []
    prime_count = 0
    for _ in range(num_runs):
        time_taken, count = measure_execution_time(prime_function, n)
        times.append(time_taken)
        prime_count = count
    return statistics.mean(times), prime_count

def main():
    """
    Main function to run the prime generation algorithm benchmark
    """
    input_sizes = [10000, 50000, 100000, 500000, 1000000]
    num_runs = 3
    
    algorithms = [
        ("Naive Trial Division", naive_trial_division),
        ("Optimized Trial Division", optimized_trial_division),
        ("Sieve of Eratosthenes", sieve_of_eratosthenes),
    ]
    
    print("=" * 100)
    print("Prime Number Generation Algorithm Performance Comparison")
    print("=" * 100)
    print(f"Number of runs per measurement: {num_runs}")
    print(f"Input sizes (n): {input_sizes}")
    print("=" * 100)
    print()
    
    for size in input_sizes:
        print(f"\nGenerating primes up to {size:,}:")
        print("-" * 100)
        print(f"{'Algorithm':<30} {'Time (ms)':<15} {'Primes Found':<15} {'Time per Prime (μs)':<20}")
        print("-" * 100)
        
        results = []
        for name, func in algorithms:
            # Skip naive trial division for large sizes as it's too slow
            if name == "Naive Trial Division" and size > 50000:
                print(f"{name:<30} {'SKIPPED':<15} {'N/A':<15} {'N/A':<20}")
                continue
                
            avg_time, prime_count = average_execution_time(func, size, num_runs)
            time_per_prime = (avg_time * 1000) / prime_count if prime_count > 0 else 0
            results.append((name, avg_time, prime_count, time_per_prime))
            print(f"{name:<30} {avg_time:<15.4f} {prime_count:<15} {time_per_prime:<20.4f}")
        
        # Find fastest algorithm
        if results:
            fastest = min(results, key=lambda x: x[1])
            print(f"\nFastest for n={size:,}: {fastest[0]} ({fastest[1]:.4f} ms)")
    
    print("\n" + "=" * 100)
    print("Summary Analysis:")
    print("=" * 100)
    print("1. Naive Trial Division: Checks all numbers from 2 to n-1 - O(n²) complexity - extremely slow")
    print("2. Optimized Trial Division: Checks up to √n - O(n√n) complexity - much better but still slow for large n")
    print("3. Sieve of Eratosthenes: Eliminates multiples efficiently - O(n log log n) complexity - fastest for bulk generation")
    print()
    print("Key Insights:")
    print("- Naive trial division becomes impractical for n > 50,000 due to O(n²) complexity")
    print("- Optimized trial division is significantly better but still struggles with large n")
    print("- Sieve of Eratosthenes scales excellently and is the clear winner for large input sizes")
    print("- The performance gap between trial division and sieve grows dramatically as n increases")
    print("=" * 100)

if __name__ == "__main__":
    main()
