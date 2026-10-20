
import math
import time
import random


def closest_pair_brute(points):
    """Find the closest pair by checking every pair."""
    n = len(points)

    if n < 2:
        raise ValueError("At least two points are required.")

    best_d2 = float("inf")
    best_pair = None

    for i in range(n):
        for j in range(i + 1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            d2 = dx * dx + dy * dy

            pair = (i, j)

            if (d2, pair) < (best_d2, best_pair or (n, n)):
                best_d2 = d2
                best_pair = pair

    return (math.sqrt(best_d2), best_pair[0], best_pair[1])


def closest_pair(points):
    """Find the closest pair using divide and conquer."""
    n = len(points)

    if n < 2:
        raise ValueError("At least two points are required.")

    # Store (x, y, original_index).
    px = sorted(
        (point[0], point[1], i)
        for i, point in enumerate(points)
    )
    py = sorted(px, key=lambda p: (p[1], p[0], p[2]))

    def distance_squared(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return dx * dx + dy * dy

    def pair_indices(a, b):
        return tuple(sorted((a[2], b[2])))

    def better(candidate, best):
        return candidate < best

    def solve(by_x, by_y):
        size = len(by_x)

        # Base case: directly compare small groups.
        if size <= 3:
            best = (float("inf"), (n, n))

            for i in range(size):
                for j in range(i + 1, size):
                    candidate = (
                        distance_squared(by_x[i], by_x[j]),
                        pair_indices(by_x[i], by_x[j])
                    )
                    if better(candidate, best):
                        best = candidate

            return best, sorted(by_x, key=lambda p: (p[1], p[0], p[2]))

        mid = size // 2
        left_x = by_x[:mid]
        right_x = by_x[mid:]
        left_ids = {p[2] for p in left_x}

        left_y = [p for p in by_y if p[2] in left_ids]
        right_y = [p for p in by_y if p[2] not in left_ids]

        best_left, _ = solve(left_x, left_y)
        best_right, _ = solve(right_x, right_y)
        best = min(best_left, best_right)

        # Check points within the current best distance of the split.
        split_x = right_x[0][0]
        strip = [
            p for p in by_y
            if (p[0] - split_x) ** 2 <= best[0]
        ]

        # The geometric packing argument limits the useful
        # comparisons to the next seven points in y-order.
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                dy = strip[j][1] - strip[i][1]

                if dy * dy > best[0]:
                    break

                candidate = (
                    distance_squared(strip[i], strip[j]),
                    pair_indices(strip[i], strip[j])
                )

                if better(candidate, best):
                    best = candidate

        # by_y is already sorted by y, so no further sort is needed.
        return best, by_y

    (best_d2, (i, j)), _ = solve(px, py)
    return (math.sqrt(best_d2), i, j)


def generate_random_points(n, x_range=1000, y_range=1000):
    """Generate n random points within the given range."""
    return [(random.uniform(0, x_range), random.uniform(0, y_range)) for _ in range(n)]


def measure_time(func, *args):
    """Measure execution time of a function."""
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, (end - start) * 1000  # Return result and time in milliseconds


def main():
    """Run Assignment 2: Closest Pair of Points Algorithm Comparison."""
    print("=" * 100)
    print("Assignment 2: Closest Pair of Points Algorithm Performance Comparison")
    print("=" * 100)
    print()

    # Test with different input sizes
    input_sizes = [100, 500, 1000, 2000, 5000]

    print(f"Testing with input sizes: {input_sizes}")
    print()

    for n in input_sizes:
        print(f"\n{'=' * 100}")
        print(f"Testing with {n:,} random points")
        print("=" * 100)

        # Generate random points
        points = generate_random_points(n)

        # Test brute force (skip for large n as it's O(n²))
        print(f"\nBrute Force Algorithm (O(n²)):")
        if n <= 2000:
            brute_result, brute_time = measure_time(closest_pair_brute, points)
            print(f"  Distance: {brute_result[0]:.6f}")
            print(f"  Pair indices: ({brute_result[1]}, {brute_result[2]})")
            print(f"  Time: {brute_time:.4f} ms")
        else:
            print(f"  SKIPPED (too slow for n={n:,})")
            brute_result = None
            brute_time = float('inf')

        # Test divide and conquer
        print(f"\nDivide and Conquer Algorithm (O(n log n)):")
        dc_result, dc_time = measure_time(closest_pair, points)
        print(f"  Distance: {dc_result[0]:.6f}")
        print(f"  Pair indices: ({dc_result[1]}, {dc_result[2]})")
        print(f"  Time: {dc_time:.4f} ms")

        # Verify results match
        if brute_result is not None:
            if abs(brute_result[0] - dc_result[0]) < 1e-6:
                print(f"\n✓ Results match!")
            else:
                print(f"\n✗ Results differ!")

        # Calculate speedup
        if brute_result is not None and brute_time > 0:
            speedup = brute_time / dc_time
            print(f"Speedup: {speedup:.2f}x")

    print("\n" + "=" * 100)
    print("Summary:")
    print("=" * 100)
    print("1. Brute Force: Checks every pair - O(n²) complexity - becomes impractical for large n")
    print("2. Divide and Conquer: Recursively splits and merges - O(n log n) complexity - scales well")
    print()
    print("Key Insights:")
    print("- Brute force is simple but becomes extremely slow as n increases")
    print("- Divide and conquer uses geometric properties to limit comparisons")
    print("- The strip check ensures only nearby points across the split are compared")
    print("- Performance gap grows dramatically as input size increases")
    print("=" * 100)


if __name__ == "__main__":
    main()
