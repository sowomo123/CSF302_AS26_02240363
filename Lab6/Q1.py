import time

# Price table for lengths 1 to 10
price_table = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]

# Global counter for recursive calls
recursive_calls = 0

def reset_calls():
    global recursive_calls
    recursive_calls = 0

def get_calls():
    global recursive_calls
    return recursive_calls

def increment_calls():
    global recursive_calls
    recursive_calls += 1

# ============== NAIVE RECURSIVE SOLUTION ==============
def rod_cutting_naive(n, prices):
    """
    Naive recursive solution - O(2^n)
    """
    increment_calls()
    
    if n == 0:
        return 0
    
    max_revenue = float('-inf')
    
    for i in range(1, n + 1):
        price = get_extended_price(i)
        max_revenue = max(max_revenue, price + rod_cutting_naive(n - i, prices))
    
    return max_revenue

def rod_cutting_naive_with_pieces(n, prices):
    """
    Naive recursive solution that also returns the piece lengths
    """
    increment_calls()
    
    if n == 0:
        return 0, []
    
    max_revenue = float('-inf')
    best_pieces = []
    
    for i in range(1, n + 1):
        price = get_extended_price(i)
        revenue, pieces = rod_cutting_naive_with_pieces(n - i, prices)
        total = price + revenue
        
        if total > max_revenue:
            max_revenue = total
            best_pieces = [i] + pieces
    
    return max_revenue, best_pieces

# ============== TOP-DOWN MEMOIZED SOLUTION ==============
def rod_cutting_memo(n, prices, memo=None):
    """
    Top-down memoized solution - O(n^2)
    """
    increment_calls()
    
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n == 0:
        memo[n] = 0
        return 0
    
    max_revenue = float('-inf')
    
    for i in range(1, n + 1):
        price = get_extended_price(i)
        max_revenue = max(max_revenue, price + rod_cutting_memo(n - i, prices, memo))
    
    memo[n] = max_revenue
    return max_revenue

def rod_cutting_memo_with_pieces(n, prices, memo=None, pieces_memo=None):
    """
    Top-down memoized solution that also returns the piece lengths
    """
    increment_calls()
    
    if memo is None:
        memo = {}
    if pieces_memo is None:
        pieces_memo = {}
    
    if n in memo:
        return memo[n], pieces_memo[n]
    
    if n == 0:
        memo[n] = 0
        pieces_memo[n] = []
        return 0, []
    
    max_revenue = float('-inf')
    best_pieces = []
    
    for i in range(1, n + 1):
        price = get_extended_price(i)
        revenue, pieces = rod_cutting_memo_with_pieces(n - i, prices, memo, pieces_memo)
        total = price + revenue
        
        if total > max_revenue:
            max_revenue = total
            best_pieces = [i] + pieces
    
    memo[n] = max_revenue
    pieces_memo[n] = best_pieces
    return max_revenue, best_pieces

# ============== BOTTOM-UP TABULATED SOLUTION ==============
def rod_cutting_bottom_up(n, prices):
    """
    Bottom-up tabulated solution - O(n^2)
    """
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            price = get_extended_price(j)
            dp[i] = max(dp[i], price + dp[i - j])
    
    return dp[n]

def rod_cutting_bottom_up_with_pieces(n, prices):
    """
    Bottom-up tabulated solution that also returns the piece lengths
    """
    dp = [0] * (n + 1)
    pieces = [[] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            price = get_extended_price(j)
            if price + dp[i - j] > dp[i]:
                dp[i] = price + dp[i - j]
                pieces[i] = [j] + pieces[i - j]
    
    return dp[n], pieces[n]

# ============== EXTENDED PRICE TABLE ==============
def get_extended_price(n):
    """
    Get price for length n, using 3*i for i > 10
    """
    if n <= 10:
        return price_table[n]
    else:
        return 3 * n

# ============== PART 1: Print max revenue and pieces for n = 1 to 10 ==============
def part1():
    print("=" * 80)
    print("Part 1: Maximum Revenue and Piece Lengths for n = 1 to 10")
    print("=" * 80)
    print()
    
    print(f"{'n':<5} {'Max Revenue':<15} {'Piece Lengths':<30}")
    print("-" * 80)
    
    for n in range(1, 11):
        revenue, pieces = rod_cutting_bottom_up_with_pieces(n, price_table)
        print(f"{n:<5} {revenue:<15} {str(pieces):<30}")
    
    print("=" * 80)
    print()

# ============== PART 2: Count recursive calls and measure time ==============
def part2():
    print("=" * 80)
    print("Part 2: Recursive Calls and Execution Time Comparison")
    print("=" * 80)
    print()
    
    test_values = [5, 10, 15, 20, 25]
    
    print(f"{'n':<5} {'Naive Calls':<15} {'Naive Time (ms)':<20} {'Memo Calls':<15} {'Memo Time (ms)':<20} {'Bottom-up Time (ms)':<20}")
    print("-" * 140)
    
    for n in test_values:
        # Naive
        reset_calls()
        start = time.perf_counter()
        revenue_naive = rod_cutting_naive(n, price_table)
        naive_time = (time.perf_counter() - start) * 1000
        naive_calls = get_calls()
        
        # Memoized
        reset_calls()
        start = time.perf_counter()
        revenue_memo = rod_cutting_memo(n, price_table)
        memo_time = (time.perf_counter() - start) * 1000
        memo_calls = get_calls()
        
        # Bottom-up (no recursive calls)
        start = time.perf_counter()
        revenue_bottom = rod_cutting_bottom_up(n, price_table)
        bottom_time = (time.perf_counter() - start) * 1000
        
        print(f"{n:<5} {naive_calls:<15} {naive_time:<20.6f} {memo_calls:<15} {memo_time:<20.6f} {bottom_time:<20.6f}")
        
        # Verify all give same answer
        assert revenue_naive == revenue_memo == revenue_bottom, f"Results don't match for n={n}"
    
    print("=" * 80)
    print()
    
    # Explanation
    print("Explanation of Differences:")
    print("-" * 80)
    print("1. Naive Recursive:")
    print("   - Time Complexity: O(2^n)")
    print("   - Space Complexity: O(n) for recursion stack")
    print("   - Recalculates the same subproblems multiple times")
    print("   - Number of calls grows exponentially with n")
    print()
    print("2. Top-Down Memoized:")
    print("   - Time Complexity: O(n^2)")
    print("   - Space Complexity: O(n^2) for memoization table")
    print("   - Stores results of subproblems to avoid recalculation")
    print("   - Each subproblem is solved only once")
    print()
    print("3. Bottom-Up Tabulated:")
    print("   - Time Complexity: O(n^2)")
    print("   - Space Complexity: O(n)")
    print("   - Iteratively fills the DP table")
    print("   - No recursive calls, most efficient in practice")
    print()
    print("The memoized and bottom-up versions have the same asymptotic complexity,")
    print("but bottom-up is typically faster due to no function call overhead.")
    print("=" * 80)
    print()

# ============== MAIN FUNCTION ==============
def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
