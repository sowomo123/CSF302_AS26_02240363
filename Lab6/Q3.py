import random
import time
from itertools import combinations

# ============== LCS - BOTTOM-UP DP ==============
def lcs_length(X, Y):
    """
    Compute LCS length using bottom-up DP
    Time Complexity: O(m*n)
    Space Complexity: O(m*n)
    """
    m, n = len(X), len(Y)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp

def print_lcs_table(X, Y, dp):
    """
    Print the LCS table with headers
    """
    m, n = len(X), len(Y)
    
    print("  ", end='')
    print("  " + " ".join(list(Y)))
    
    for i in range(m + 1):
        if i == 0:
            print("  ", end='')
        else:
            print(X[i - 1] + " ", end='')
        
        for j in range(n + 1):
            print(f"{dp[i][j]:2}", end=' ')
        print()

def reconstruct_lcs(X, Y, dp):
    """
    Reconstruct one LCS from the DP table
    """
    m, n = len(X), len(Y)
    lcs = []
    
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))

# ============== SPACE-OPTIMIZED LCS ==============
def lcs_length_space_optimized(X, Y):
    """
    Space-optimized LCS using only two rows
    Time Complexity: O(m*n)
    Space Complexity: O(min(m, n))
    """
    # Ensure X is the shorter string for better space efficiency
    if len(X) > len(Y):
        X, Y = Y, X
    
    m, n = len(X), len(Y)
    
    # Only keep two rows
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        
        # Swap rows
        prev, curr = curr, prev
        curr = [0] * (n + 1)
    
    return prev[n]

# ============== BRUTE-FORCE LCS ==============
def lcs_brute_force(X, Y):
    """
    Brute-force LCS by trying every subsequence of X
    Time Complexity: O(2^m * n) where m = len(X), n = len(Y)
    """
    m = len(X)
    best_lcs =""
    
    # Generate all possible subsequences of X
    for r in range(m + 1):
        for indices in combinations(range(m), r):
            subsequence = ''.join(X[i] for i in indices)
            
            # Check if this subsequence is a subsequence of Y
            if is_subsequence(subsequence, Y):
                if len(subsequence) > len(best_lcs):
                    best_lcs = subsequence
    
    return best_lcs

def is_subsequence(sub, string):
    """
    Check if sub is a subsequence of string
    """
    it = iter(string)
    return all(c in it for c in sub)

# ============== TIMING COMPARISON ==============
def compare_running_times():
    """
    Compare DP vs brute-force for string lengths 5 to 18
    """
    print("=" * 80)
    print("Timing Comparison: DP vs Brute-Force LCS")
    print("=" * 80)
    print()
    
    print(f"{'Length':<10} {'DP Time (ms)':<20} {'Brute Time (ms)':<20} {'Speedup':<10}")
    print("-" * 80)
    
    for length in range(5, 19):
        # Generate random strings
        X = ''.join(random.choice('ABCD') for _ in range(length))
        Y = ''.join(random.choice('ABCD') for _ in range(length))
        
        # Time DP
        start = time.perf_counter()
        dp_result = lcs_length(X, Y)
        dp_time = (time.perf_counter() - start) * 1000
        
        # Time brute force (skip for very long strings)
        start = time.perf_counter()
        brute_result = lcs_brute_force(X, Y)
        brute_time = (time.perf_counter() - start) * 1000
        
        # Verify results match
        dp_lcs = reconstruct_lcs(X, Y, dp_result)
        assert len(dp_lcs) == len(brute_result), f"Results don't match for length {length}"
        
        speedup = brute_time / dp_time if dp_time > 0 else 0
        print(f"{length:<10} {dp_time:<20.6f} {brute_time:<20.6f} {speedup:<10.2f}x")
    
    print("=" * 80)
    print()

# ============== LINE-BY-LINE DIFF ==============
def line_by_line_diff(file1, file2):
    """
    Print line-by-line diff using LCS
    Lines in LCS are unchanged, others are added or removed
    """
    with open(file1, 'r') as f:
        lines1 = f.readlines()
    
    with open(file2, 'r') as f:
        lines2 = f.readlines()
    
    # Compute LCS of lines
    dp = lcs_length(lines1, lines2)
    
    # Reconstruct LCS and track which indices are in LCS
    m, n = len(lines1), len(lines2)
    lcs_indices1 = set()
    lcs_indices2 = set()
    
    i, j = m, n
    while i > 0 and j > 0:
        if lines1[i - 1] == lines2[j - 1]:
            lcs_indices1.add(i - 1)
            lcs_indices2.add(j - 1)
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    print("=" * 80)
    print(f"Line-by-Line Diff: {file1} vs {file2}")
    print("=" * 80)
    print()
    
    print(f"File 1 ({file1}):")
    for idx, line in enumerate(lines1):
        if idx in lcs_indices1:
            print(f"  {line}", end='')
        else:
            print(f"- {line}", end='')
    
    print()
    print(f"File 2 ({file2}):")
    for idx, line in enumerate(lines2):
        if idx in lcs_indices2:
            print(f"  {line}", end='')
        else:
            print(f"+ {line}", end='')
    
    print("=" * 80)
    print()

# ============== DEMONSTRATION ==============
def demonstrate_lcs():
    print("=" * 80)
    print("LCS Demonstration: X = ABCBDAB, Y = BDCABA")
    print("=" * 80)
    print()
    
    X = "ABCBDAB"
    Y = "BDCABA"
    
    # Compute LCS table
    dp = lcs_length(X, Y)
    
    # Print table
    print("LCS Table:")
    print_lcs_table(X, Y, dp)
    print()
    
    # Reconstruct LCS
    lcs = reconstruct_lcs(X, Y, dp)
    print(f"LCS: {lcs}")
    print(f"LCS Length: {len(lcs)}")
    print()
    
    # Verify with space-optimized version
    space_opt_len = lcs_length_space_optimized(X, Y)
    print(f"Space-optimized LCS length: {space_opt_len}")
    print(f"Match: {space_opt_len == len(lcs)}")
    print("=" * 80)
    print()

# ============== CREATE TEST FILES FOR DIFF ==============
def create_test_files():
    """
    Create test files for line-by-line diff demonstration
    """
    file1_content = """Line 1
Line 2
Line 3
Line 4
Line 5
"""
    
    file2_content = """Line 1
Line 2
Line 3 modified
Line 4
Line 6
"""
    
    with open('test_file1.txt', 'w') as f:
        f.write(file1_content)
    
    with open('test_file2.txt', 'w') as f:
        f.write(file2_content)

# ============== MAIN FUNCTION ==============
def main():
    # Demonstrate LCS with given strings
    demonstrate_lcs()
    
    # Compare running times
    compare_running_times()
    
    # Create test files and show diff
    create_test_files()
    line_by_line_diff('test_file1.txt', 'test_file2.txt')

if __name__ == "__main__":
    main()
