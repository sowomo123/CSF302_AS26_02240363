# Lab 6 - Dynamic Programming

This lab explores dynamic programming through four classic problems: Rod Cutting, Matrix Chain Multiplication, Longest Common Subsequence, and Optimal Binary Search Tree.

## Question 1: Rod Cutting

### Problem
Given a rod of length n and a price table for different lengths, find the maximum revenue by cutting the rod optimally.

### Algorithms Implemented

1. **Naive Recursive** - O(2^n) - Exponential time, recalculates subproblems
2. **Top-Down Memoized** - O(n²) - Stores results to avoid recalculation
3. **Bottom-Up Tabulated** - O(n²) - Iterative DP table filling

### Results

#### Part 1: Maximum Revenue for n = 1 to 10

| n | Max Revenue | Piece Lengths |
|---|-------------|---------------|
| 1 | 1 | [1] |
| 2 | 5 | [2] |
| 3 | 8 | [3] |
| 4 | 10 | [2, 2] |
| 5 | 13 | [2, 3] |
| 6 | 17 | [6] |
| 7 | 18 | [1, 6] |
| 8 | 22 | [2, 6] |
| 9 | 25 | [3, 6] |
| 10 | 30 | [10] |

#### Part 2: Recursive Calls and Execution Time

| n | Naive Calls | Naive Time (ms) | Memo Calls | Memo Time (ms) | Bottom-up Time (ms) |
|---|-------------|-----------------|------------|----------------|---------------------|
| 5 | 32 | 0.031 | 16 | 0.013 | 0.006 |
| 10 | 1,024 | 0.403 | 56 | 0.017 | 0.009 |
| 15 | 32,768 | 8.828 | 121 | 0.030 | 0.015 |
| 20 | 1,048,576 | 522.323 | 211 | 0.048 | 0.062 |
| 25 | 33,554,432 | 12,739.194 | 326 | 0.080 | 0.036 |

### Key Findings

- **Naive recursive** grows exponentially (2^n calls)
- **Memoized** reduces to O(n²) calls by storing subproblem results
- **Bottom-up** is fastest due to no function call overhead
- Speedup increases dramatically with n (from 7.85x at n=5 to over 400,000x at n=25)

---

## Question 2: Matrix Chain Multiplication

### Problem
Given dimensions of matrices, find the optimal parenthesization to minimize scalar multiplications.

### Algorithms Implemented

1. **Bottom-Up DP** - O(n³) - Computes optimal cost and parenthesization
2. **Brute-Force Recursive** - O(2^n) - Tries all possible parenthesizations

### Results

#### Verification: DP vs Brute Force (up to 8 matrices)
All tests passed ✓

#### Test 1: <30, 35, 15, 5, 10, 20, 25>
- **Optimal cost:** 15,125
- **Expected:** 15,125 ✓
- **Optimal parenthesization:** ((A1(A2A3))((A4A5)A6))
- **Left-to-right cost:** 40,500
- **Speedup:** 2.68x

#### Test 2: <5, 4, 6, 2, 7>
- **Optimal cost:** 158
- **Optimal parenthesization:** ((A1(A2A3))A4)
- **Left-to-right cost:** 250
- **Speedup:** 1.58x

#### Random Chains (5 tests)
All verified with brute force, speedup ranging from 1.90x to 9.19x

### Key Findings

- DP solution is O(n³) vs brute force O(2^n)
- Optimal parenthesization can provide significant speedup (up to 9x)
- Left-to-right multiplication is often suboptimal

---

## Question 3: Longest Common Subsequence

### Problem
Find the longest subsequence common to two strings.

### Algorithms Implemented

1. **Bottom-Up DP** - O(mn) - Full DP table
2. **Space-Optimized** - O(min(m,n)) - Uses only two rows
3. **Brute-Force** - O(2^m * n) - Tries all subsequences

### Results

#### LCS Table for X = ABCBDAB, Y = BDCABA

```
    B D C A B A
   0  0  0  0  0  0  0
A  0  0  0  0  1  1  1
B  0  1  1  1  1  2  2
C  0  1  1  2  2  2  2
B  0  1  1  2  2  3  3
D  0  1  2  2  2  3  3
A  0  1  2  2  3  3  4
B  0  1  2  2  3  4  4
```

- **LCS:** BDAB
- **LCS Length:** 4
- **Space-optimized:** Matches ✓

#### Timing Comparison (Lengths 5-18)

| Length | DP Time (ms) | Brute Time (ms) | Speedup |
|--------|--------------|-----------------|---------|
| 5 | 0.012 | 0.073 | 6.19x |
| 10 | 0.022 | 3.143 | 140.94x |
| 15 | 0.045 | 105.418 | 2,363.65x |
| 18 | 0.052 | 546.639 | 10,492.10x |

#### Line-by-Line Diff
Successfully implemented using LCS to show unchanged, added, and removed lines.

### Key Findings

- DP solution is O(mn) vs brute force O(2^m)
- Speedup increases exponentially with string length
- Space optimization reduces memory from O(mn) to O(min(m,n))
- LCS can be used for file diffing

---

## Question 4: Optimal Binary Search Tree (Optional)

### Problem
Given keys with search probabilities, construct BST with minimum expected search cost.

### Results

**Input:**
- p (successful): [0.15, 0.10, 0.05, 0.10, 0.20]
- q (unsuccessful): [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]

**Output:**
- **Expected search cost:** 2.75
- **Expected:** 2.75 ✓
- **Optimal BST Structure:**
  ```
  k2
    k1
      d0
      d1
    k5
      k4
        k3
          d2
          d3
        d4
      d5
  ```

### Key Findings

- DP solution computes optimal BST in O(n³)
- Expected cost matches theoretical value
- Optimal structure balances search probabilities

---

## Files

- `Q1.py` - Rod cutting with three implementations
- `Q2.py` - Matrix chain multiplication with verification
- `Q3.py` - LCS with space optimization and diff
- `Q4.py` - Optimal BST construction

## Running the Code

```bash
python Q1.py  # Rod cutting
python Q2.py  # Matrix chain multiplication
python Q3.py  # LCS and diff
python Q4.py  # Optimal BST
```
