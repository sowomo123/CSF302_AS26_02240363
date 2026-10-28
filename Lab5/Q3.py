import random
import time
import sys

# ============== BRUTE-FORCE INVERSION COUNT ==============
def count_inversions_brute_force(arr):
    """
    Count inversions using brute force - O(n²)
    Checks every pair (i, j) where i < j
    """
    n = len(arr)
    inversions = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inversions += 1
    
    return inversions

# ============== MERGE-SORT-BASED INVERSION COUNT ==============
def count_inversions_merge_sort(arr):
    """
    Count inversions using merge sort - O(n log n)
    Returns (sorted_array, inversion_count)
    """
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_inv = count_inversions_merge_sort(arr[:mid])
    right, right_inv = count_inversions_merge_sort(arr[mid:])
    merged, split_inv = merge_and_count(left, right)
    
    total_inv = left_inv + right_inv + split_inv
    return merged, total_inv

def merge_and_count(left, right):
    """
    Merge two sorted arrays and count split inversions
    A split inversion is when an element in left is greater than an element in right
    """
    result = []
    i = j = 0
    split_inversions = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            # All remaining elements in left are inversions with right[j]
            split_inversions += len(left) - i
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result, split_inversions

def count_inversions_merge_sort_wrapper(arr):
    """Wrapper that returns just the inversion count"""
    _, inversions = count_inversions_merge_sort(arr)
    return inversions

# ============== VERIFICATION ==============
def verify_correctness():
    """
    Verify both methods give the same answer on random arrays up to size 2,000
    """
    print("=" * 80)
    print("Verifying Correctness: Brute Force vs Merge Sort Method")
    print("=" * 80)
    
    test_sizes = [10, 50, 100, 500, 1000, 2000]
    all_passed = True
    
    for size in test_sizes:
        # Generate random array
        arr = [random.randint(0, size * 10) for _ in range(size)]
        
        # Count inversions using both methods
        brute_count = count_inversions_brute_force(arr)
        merge_count = count_inversions_merge_sort_wrapper(arr)
        
        # Check if they match
        passed = brute_count == merge_count
        status = "✓ PASS" if passed else "✗ FAIL"
        
        print(f"n={size:<6} Brute: {brute_count:<10} Merge: {merge_count:<10} {status}")
        
        if not passed:
            all_passed = False
            print(f"  ERROR: Mismatch detected!")
    
    print("=" * 80)
    print(f"All tests passed: {all_passed}")
    print("=" * 80)
    print()
    
    return all_passed

# ============== TIMING EXPERIMENT ==============
def timing_experiment():
    """
    Time both methods for n = 1,000 to 1,000,000
    Stop brute force when it exceeds 60 seconds
    """
    print("=" * 80)
    print("Timing Experiment: Brute Force vs Merge Sort")
    print("=" * 80)
    print(f"{'n':<12} {'Brute Force (ms)':<20} {'Merge Sort (ms)':<20} {'Speedup':<10}")
    print("-" * 80)
    
    n_values = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]
    
    for n in n_values:
        # Generate random array
        arr = [random.randint(0, n * 10) for _ in range(n)]
        
        # Time merge sort method
        arr_copy = arr.copy()
        start = time.perf_counter()
        merge_count = count_inversions_merge_sort_wrapper(arr_copy)
        merge_time = (time.perf_counter() - start) * 1000
        
        # Time brute force (with 60 second timeout)
        arr_copy = arr.copy()
        start = time.perf_counter()
        brute_count = count_inversions_brute_force(arr_copy)
        brute_time = (time.perf_counter() - start) * 1000
        
        # Check if exceeded 60 seconds
        if brute_time > 60000:
            print(f"{n:<12} {'> 60000':<20} {merge_time:<20.4f} {'N/A':<10}")
            print("  Brute force exceeded 60 seconds - stopping further measurements")
            break
        
        # Calculate speedup
        speedup = brute_time / merge_time if merge_time > 0 else 0
        
        print(f"{n:<12} {brute_time:<20.4f} {merge_time:<20.4f} {speedup:<10.2f}x")
        
        # Verify counts match
        if brute_count != merge_count:
            print(f"  WARNING: Counts don't match! Brute: {brute_count}, Merge: {merge_count}")
    
    print("=" * 80)
    print()

# ============== KENDALL TAU DISTANCE (MOVIE RANKINGS) ==============
def kendall_tau_distance(rank1, rank2):
    """
    Compute Kendall tau distance between two rankings
    This is the number of pairwise disagreements between two rankings
    Equivalent to counting inversions when we map one ranking to the other
    """
    n = len(rank1)
    
    # Create position mapping from rank1 to rank2
    # rank1 gives the order of items as ranked by user 1
    # rank2 gives the order of items as ranked by user 2
    # We need to count how many pairs are in different order
    
    # Map each movie to its position in rank2
    position_in_rank2 = {}
    for idx, movie in enumerate(rank2):
        position_in_rank2[movie] = idx
    
    # Create array representing rank1's order in terms of rank2's positions
    # If user1 ranks movie A before movie B, but user2 ranks B before A,
    # that's an inversion
    arr = [position_in_rank2[movie] for movie in rank1]
    
    # Count inversions in this array
    inversions = count_inversions_merge_sort_wrapper(arr)
    
    return inversions

def kendall_tau_similarity(rank1, rank2):
    """
    Compute normalized Kendall tau similarity
    Returns a value between 0 (completely different) and 1 (identical)
    """
    n = len(rank1)
    distance = kendall_tau_distance(rank1, rank2)
    max_distance = n * (n - 1) / 2  # Maximum possible inversions
    similarity = 1 - (distance / max_distance)
    return similarity

def get_movie_rankings():
    """
    Get movie rankings from keyboard input
    Returns two lists of 10 movie rankings
    """
    print("=" * 80)
    print("Kendall Tau Distance: Movie Ranking Similarity")
    print("=" * 80)
    print("Enter rankings for 10 movies (1-10, where 1 is best)")
    print()
    
    # Get movies (optional - can use generic names)
    movies = [f"Movie {i+1}" for i in range(10)]
    
    # Get user 1 ranking
    print("User 1: Enter ranking for each movie (1-10, no duplicates)")
    rank1 = []
    for i, movie in enumerate(movies):
        while True:
            try:
                ranking = int(input(f"  {movie}: "))
                if 1 <= ranking <= 10 and ranking not in rank1:
                    rank1.append(ranking)
                    break
                else:
                    print("  Invalid ranking! Must be 1-10 and unique.")
            except ValueError:
                print("  Please enter a number.")
    
    # Get user 2 ranking
    print("\nUser 2: Enter ranking for each movie (1-10, no duplicates)")
    rank2 = []
    for i, movie in enumerate(movies):
        while True:
            try:
                ranking = int(input(f"  {movie}: "))
                if 1 <= ranking <= 10 and ranking not in rank2:
                    rank2.append(ranking)
                    break
                else:
                    print("  Invalid ranking! Must be 1-10 and unique.")
            except ValueError:
                print("  Please enter a number.")
    
    return rank1, rank2

def interactive_kendall_tau():
    """
    Interactive mode to compute Kendall tau distance between two users' rankings
    """
    rank1, rank2 = get_movie_rankings()
    
    # Compute distance and similarity
    distance = kendall_tau_distance(rank1, rank2)
    similarity = kendall_tau_similarity(rank1, rank2)
    
    print()
    print("=" * 80)
    print("Results")
    print("=" * 80)
    print(f"User 1 ranking: {rank1}")
    print(f"User 2 ranking: {rank2}")
    print()
    print(f"Kendall Tau Distance: {distance}")
    print(f"Kendall Tau Similarity: {similarity:.4f} (0 = different, 1 = identical)")
    print("=" * 80)

def demo_kendall_tau():
    """
    Demo with predefined rankings
    """
    print("=" * 80)
    print("Demo: Kendall Tau Distance with Example Rankings")
    print("=" * 80)
    
    # Example rankings
    rank1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # User 1 ranks in order
    rank2 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]  # User 2 ranks in reverse order
    
    print(f"User 1 ranking: {rank1}")
    print(f"User 2 ranking: {rank2}")
    print()
    
    distance = kendall_tau_distance(rank1, rank2)
    similarity = kendall_tau_similarity(rank1, rank2)
    
    print(f"Kendall Tau Distance: {distance}")
    print(f"Kendall Tau Similarity: {similarity:.4f}")
    print(f"Maximum possible distance for 10 items: {10 * 9 / 2} = 45")
    print()
    
    # Another example
    rank3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rank4 = [1, 3, 2, 4, 5, 6, 7, 8, 9, 10]  # Only swap 2 and 3
    
    print(f"User 3 ranking: {rank3}")
    print(f"User 4 ranking: {rank4}")
    print()
    
    distance = kendall_tau_distance(rank3, rank4)
    similarity = kendall_tau_similarity(rank3, rank4)
    
    print(f"Kendall Tau Distance: {distance}")
    print(f"Kendall Tau Similarity: {similarity:.4f}")
    print("=" * 80)
    print()

# ============== MAIN FUNCTION ==============
def main():
    # Verify correctness
    verify_correctness()
    
    # Run timing experiment
    timing_experiment()
    
    # Demo Kendall tau
    demo_kendall_tau()
    
    # Ask if user wants interactive mode
    print("Do you want to enter your own movie rankings? (y/n)")
    choice = input().strip().lower()
    
    if choice == 'y':
        interactive_kendall_tau()

if __name__ == "__main__":
    main()
