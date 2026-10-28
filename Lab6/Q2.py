import random
import time

# ============== MATRIX CHAIN MULTIPLICATION - BOTTOM-UP DP ==============
def matrix_chain_order(dimensions):
    """
    Compute minimum number of scalar multiplications using bottom-up DP
    Returns: (m table, s table for reconstruction)
    Time Complexity: O(n^3)
    Space Complexity: O(n^2)
    """
    n = len(dimensions) - 1  # Number of matrices
    
    # m[i][j] = minimum scalar multiplications for matrices i..j
    m = [[0] * (n + 1) for _ in range(n + 1)]
    
    # s[i][j] = optimal split point for matrices i..j
    s = [[0] * (n + 1) for _ in range(n + 1)]
    
    # l is chain length
    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')
            
            for k in range(i, j):
                # Cost = cost of left part + cost of right part + cost of multiplying results
                cost = m[i][k] + m[k + 1][j] + dimensions[i - 1] * dimensions[k] * dimensions[j]
                
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    
    return m, s

def print_optimal_parenthesization(s, i, j):
    """
    Print optimal parenthesization from s table
    """
    if i == j:
        print(f"A{i}", end='')
    else:
        print("(", end='')
        print_optimal_parenthesization(s, i, s[i][j])
        print_optimal_parenthesization(s, s[i][j] + 1, j)
        print(")", end='')

def get_optimal_parenthesization(s, i, j):
    """
    Return optimal parenthesization as string from s table
    """
    if i == j:
        return f"A{i}"
    else:
        left = get_optimal_parenthesization(s, i, s[i][j])
        right = get_optimal_parenthesization(s, s[i][j] + 1, j)
        return f"({left}{right})"

# ============== BRUTE-FORCE RECURSIVE SEARCH ==============
def matrix_chain_brute_force(dimensions, i, j):
    """
    Brute-force recursive search for minimum scalar multiplications
    Time Complexity: O(2^n * n) - exponential
    """
    if i == j:
        return 0
    
    min_cost = float('inf')
    
    for k in range(i, j):
        cost = (matrix_chain_brute_force(dimensions, i, k) + 
                matrix_chain_brute_force(dimensions, k + 1, j) + 
                dimensions[i - 1] * dimensions[k] * dimensions[j])
        
        if cost < min_cost:
            min_cost = cost
    
    return min_cost

# ============== LEFT-TO-RIGHT ORDER COST ==============
def left_to_right_cost(dimensions):
    """
    Compute cost of multiplying matrices in left-to-right order
    ((...(A1 * A2) * A3) ... * An)
    """
    n = len(dimensions) - 1
    if n <= 1:
        return 0
    
    cost = 0
    result_dim = dimensions[:2]  # Dimensions of result after first multiplication
    
    for i in range(2, n + 1):
        cost += result_dim[0] * result_dim[1] * dimensions[i]
        result_dim = [result_dim[0], dimensions[i]]
    
    return cost

# ============== TEST FUNCTIONS ==============
def test_with_given_dimensions():
    print("=" * 80)
    print("Test 1: Given Dimensions <30, 35, 15, 5, 10, 20, 25>")
    print("=" * 80)
    
    dimensions = [30, 35, 15, 5, 10, 20, 25]
    
    m, s = matrix_chain_order(dimensions)
    n = len(dimensions) - 1
    
    optimal_cost = m[1][n]
    optimal_paren = get_optimal_parenthesization(s, 1, n)
    left_right_cost = left_to_right_cost(dimensions)
    
    print(f"Dimensions: {dimensions}")
    print(f"Number of matrices: {n}")
    print(f"Optimal cost: {optimal_cost}")
    print(f"Expected: 15,125")
    print(f"Optimal parenthesization: {optimal_paren}")
    print(f"Left-to-right cost: {left_right_cost}")
    print(f"Speedup: {left_right_cost / optimal_cost:.2f}x")
    print("=" * 80)
    print()
    
    # Verify with brute force
    brute_cost = matrix_chain_brute_force(dimensions, 1, n)
    print(f"Verification with brute force: {brute_cost}")
    print(f"Match: {brute_cost == optimal_cost}")
    print("=" * 80)
    print()

def test_with_small_dimensions():
    print("=" * 80)
    print("Test 2: Small Dimensions <5, 4, 6, 2, 7>")
    print("=" * 80)
    
    dimensions = [5, 4, 6, 2, 7]
    
    m, s = matrix_chain_order(dimensions)
    n = len(dimensions) - 1
    
    optimal_cost = m[1][n]
    optimal_paren = get_optimal_parenthesization(s, 1, n)
    left_right_cost = left_to_right_cost(dimensions)
    
    print(f"Dimensions: {dimensions}")
    print(f"Number of matrices: {n}")
    print(f"Optimal cost: {optimal_cost}")
    print(f"Optimal parenthesization: {optimal_paren}")
    print(f"Left-to-right cost: {left_right_cost}")
    print(f"Speedup: {left_right_cost / optimal_cost:.2f}x")
    print("=" * 80)
    print()
    
    # Verify with brute force
    brute_cost = matrix_chain_brute_force(dimensions, 1, n)
    print(f"Verification with brute force: {brute_cost}")
    print(f"Match: {brute_cost == optimal_cost}")
    print("=" * 80)
    print()

def test_random_chains():
    print("=" * 80)
    print("Test 3: Random Matrix Chains")
    print("=" * 80)
    
    for i in range(5):
        # Generate random chain of 4-6 matrices
        n_matrices = random.randint(4, 6)
        dimensions = [random.randint(1, 20) for _ in range(n_matrices + 1)]
        
        m, s = matrix_chain_order(dimensions)
        n = len(dimensions) - 1
        
        optimal_cost = m[1][n]
        optimal_paren = get_optimal_parenthesization(s, 1, n)
        left_right_cost = left_to_right_cost(dimensions)
        
        print(f"\nChain {i + 1}:")
        print(f"  Dimensions: {dimensions}")
        print(f"  Optimal cost: {optimal_cost}")
        print(f"  Optimal parenthesization: {optimal_paren}")
        print(f"  Left-to-right cost: {left_right_cost}")
        print(f"  Speedup: {left_right_cost / optimal_cost:.2f}x")
        
        # Verify with brute force
        brute_cost = matrix_chain_brute_force(dimensions, 1, n)
        print(f"  Brute force verification: {brute_cost}")
        print(f"  Match: {brute_cost == optimal_cost}")
    
    print("=" * 80)
    print()

def verify_brute_force():
    """
    Verify DP solution with brute force for chains up to 8 matrices
    """
    print("=" * 80)
    print("Verification: DP vs Brute Force for chains up to 8 matrices")
    print("=" * 80)
    
    for n_matrices in range(2, 9):
        # Generate random dimensions
        dimensions = [random.randint(1, 10) for _ in range(n_matrices + 1)]
        
        # DP solution
        m, s = matrix_chain_order(dimensions)
        dp_cost = m[1][n_matrices]
        
        # Brute force solution
        brute_cost = matrix_chain_brute_force(dimensions, 1, n_matrices)
        
        match = dp_cost == brute_cost
        status = "✓ PASS" if match else "✗ FAIL"
        
        print(f"n={n_matrices}: DP={dp_cost}, Brute={brute_cost} {status}")
        
        if not match:
            print(f"  Dimensions: {dimensions}")
    
    print("=" * 80)
    print()

# ============== MAIN FUNCTION ==============
def main():
    verify_brute_force()
    test_with_given_dimensions()
    test_with_small_dimensions()
    test_random_chains()

if __name__ == "__main__":
    main()
