# ============== OPTIMAL BINARY SEARCH TREE ==============
def optimal_bst(p, q, n):
    """
    Compute optimal BST using DP
    p: probabilities of successful search for keys k1..kn
    q: probabilities of unsuccessful search (dummies d0..dn)
    n: number of keys
    
    Returns: (cost table, root table)
    Time Complexity: O(n^3)
    Space Complexity: O(n^2)
    """
    # Create cost and root tables
    # e[i][j] = expected search cost for subtree containing keys i..j
    # w[i][j] = sum of probabilities in subtree i..j
    # root[i][j] = optimal root for subtree i..j
    
    e = [[0] * (n + 2) for _ in range(n + 2)]
    w = [[0] * (n + 2) for _ in range(n + 2)]
    root = [[0] * (n + 2) for _ in range(n + 2)]
    
    # Initialize for empty subtrees (only dummy nodes)
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]
    
    # Fill tables for chains of increasing length
    for l in range(1, n + 1):  # l is chain length
        for i in range(1, n - l + 2):
            j = i + l - 1
            e[i][j] = float('inf')
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            
            # Try all possible roots
            for r in range(i, j + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                
                if t < e[i][j]:
                    e[i][j] = t
                    root[i][j] = r
    
    return e, root

def construct_optimal_bst(root, i, j, key_names=None):
    """
    Construct and print the optimal BST structure
    """
    if key_names is None:
        key_names = [f"k{i}" for i in range(1, len(root))]
    
    if i > j:
        return f"d{j}"
    
    r = root[i][j]
    
    left = construct_optimal_bst(root, i, r - 1, key_names)
    right = construct_optimal_bst(root, r + 1, j, key_names)
    
    return f"({key_names[r-1]}: {left}, {right})"

def print_bst_structure(root, i, j, key_names=None, indent=0):
    """
    Print BST structure in a readable format
    """
    if key_names is None:
        key_names = [f"k{i}" for i in range(1, len(root))]
    
    if i > j:
        print("  " * indent + "d" + str(j))
        return
    
    r = root[i][j]
    
    print("  " * indent + key_names[r-1])
    print_bst_structure(root, i, r - 1, key_names, indent + 1)
    print_bst_structure(root, r + 1, j, key_names, indent + 1)

# ============== DEMONSTRATION ==============
def demonstrate_obst():
    print("=" * 80)
    print("Optimal Binary Search Tree")
    print("=" * 80)
    print()
    
    # Given probabilities
    p = [0, 0.15, 0.10, 0.05, 0.10, 0.20]  # p[1] to p[5]
    q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]  # q[0] to q[5]
    n = 5
    
    print("Probabilities:")
    print(f"p (successful search): {p[1:]}")
    print(f"q (unsuccessful search): {q}")
    print()
    
    # Compute optimal BST
    e, root = optimal_bst(p, q, n)
    
    expected_cost = e[1][n]
    print(f"Expected search cost: {expected_cost}")
    print(f"Expected: 2.75")
    print(f"Match: {abs(expected_cost - 2.75) < 0.01}")
    print()
    
    # Print optimal BST structure
    print("Optimal BST Structure:")
    print("-" * 80)
    key_names = ["k1", "k2", "k3", "k4", "k5"]
    print_bst_structure(root, 1, n, key_names)
    print()
    
    # Print parenthesized representation
    print("Parenthesized representation:")
    structure = construct_optimal_bst(root, 1, n, key_names)
    print(structure)
    print()
    
    # Print cost table for verification
    print("Cost Table (e[i][j]):")
    print("-" * 80)
    print("    ", end='')
    for j in range(n):
        print(f"j={j:<4}", end='')
    print()
    
    for i in range(1, n + 2):
        print(f"i={i:<2}", end='')
        for j in range(n):
            if j >= i - 1:
                print(f"{e[i][j]:<6.2f}", end='')
            else:
                print(f"{'-':<6}", end='')
        print()
    
    print("=" * 80)
    print()

# ============== MAIN FUNCTION ==============
def main():
    demonstrate_obst()

if __name__ == "__main__":
    main()
