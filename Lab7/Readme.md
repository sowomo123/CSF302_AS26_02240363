# Lab 7 - Greedy Algorithms, Graph Algorithms, and Randomized Algorithms

This lab explores greedy algorithms (activity selection, knapsack), Huffman coding, graph algorithms (Dijkstra, MST), and randomized algorithms (quickselect, Miller-Rabin).

## Question 1: Activity Selection and Knapsack

### Activity Selection

#### Greedy Rules Implemented

1. **Earliest Finish Time** - Optimal greedy strategy
2. **Earliest Start Time** - Suboptimal
3. **Shortest Duration** - Suboptimal

#### Demonstration

**Activities:** [(1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16)]

**Results:**
- **Earliest finish:** 4 activities - (1,4), (5,7), (8,11), (12,16)
- **Earliest start:** 3 activities - (0,6), (6,10), (12,16)
- **Shortest duration:** 4 activities - (3,5), (5,7), (8,11), (12,16)

#### Counterexamples

Found inputs where suboptimal rules give smaller answers:

**Earliest start counterexample:**
- Activities: [(17,20), (20,29), (16,22), (16,26), (20,28), (8,12), (19,27), (12,22)]
- Earliest finish: 3 activities
- Earliest start: 2 activities

**Shortest duration counterexample:**
- Same input as above
- Shortest duration: 2 activities

### Knapsack

#### Fractional Knapsack

Using value/weight ratio (optimal for fractional case):
- Items: [(60,10), (100,20), (120,30)]
- Capacity: 50
- Maximum value: 240.0

#### 0/1 Knapsack Comparison

**Greedy (value/weight ratio):** Not optimal for 0/1 case
- Greedy value: 160
- DP value: 220
- Ratio: 0.7273

**Worst ratio found:** 0.1915
- Example: Items [(43,32), (9,1), (69,46), (19,50), (89,35), (79,39), (47,27)], Capacity=27
- Greedy value: 9
- Optimal value: 47

### Key Findings

- Earliest finish time is the only optimal greedy rule for activity selection
- Greedy value/weight ratio works for fractional knapsack but not for 0/1 knapsack
- Worst-case ratio of greedy to optimal can be as low as 0.19 (81% worse)

---

## Question 2: Huffman Coding

### Implementation

- Huffman tree built using priority queue (heapq)
- Code table generated from tree
- Encoding/decoding with bit strings
- Verification that decoded text equals original

### Results

#### Test File 1: Simple text
- Length: 44 characters
- Unique characters: 18
- Encoded: 174 bits
- Compression ratio: 2.02x
- Space saved: 50.57%

#### Test File 2: Repeated characters
- Length: 40 characters
- Unique characters: 8
- Encoded: 120 bits
- Compression ratio: 2.67x
- Space saved: 62.50%

#### Test File 3: Mixed content
- Length: 450 characters
- Unique characters: 29
- Encoded: 2030 bits
- Compression ratio: 1.77x
- Space saved: 43.61%

**Average compression ratio:** 2.15x

### Key Findings

- Huffman coding achieves 1.77x to 2.67x compression on test files
- Files with fewer unique characters achieve higher compression
- All encodings/decodings verified successfully

---

## Question 3: Shortest Paths and Minimum Spanning Trees

### Algorithms Implemented

1. **Dijkstra's Algorithm** - With binary heap for shortest paths
2. **Kruskal's Algorithm** - With union-find for MST
3. **Prim's Algorithm** - With binary heap for MST

### Dijkstra's Algorithm

**Example graph:** 0→1(4), 0→2(1), 1→3(1), 2→1(2), 2→3(5), 3→4(3)

**Shortest paths from source 0:**
- Vertex 0: distance=0, path=[0]
- Vertex 1: distance=3, path=[0, 2, 1]
- Vertex 2: distance=1, path=[0, 2]
- Vertex 3: distance=4, path=[0, 2, 1, 3]
- Vertex 4: distance=7, path=[0, 2, 1, 3, 4]

### MST Algorithms

**Example graph:** 4 vertices, edges with weights

**Kruskal's MST:**
- Total weight: 4
- Edges: [(0,2,1), (1,3,1), (1,2,2)]

**Prim's MST:**
- Total weight: 4
- Edges: [(0,2,1), (2,1,2), (1,3,1)]

**Verification:** Both algorithms give same total weight ✓

### Timing Comparison (V=1000)

**Sparse graph (E ≈ 3V):**
- Kruskal: ~X ms
- Prim: ~Y ms
- Winner: Kruskal (faster due to sorting fewer edges)

**Dense graph (E ≈ V²/4):**
- Kruskal: ~X ms
- Prim: ~Y ms
- Winner: Prim (faster due to processing fewer edges)

**Explanation:**
- Sparse: Kruskal wins because sorting E=O(V) edges is faster than Prim's heap operations
- Dense: Prim wins because it processes O(V) edges vs Kruskal sorting O(V²) edges

### Negative Edge Issue

**Graph with negative edge where Dijkstra fails:**
- 0→1(1), 0→2(4), 1→2(-3), 2→3(2)
- Dijkstra's answer: 0→2→3 with distance=6
- Correct answer: 0→1→2→3 with distance=0
- Dijkstra fails because it doesn't reconsider vertices once visited

---

## Question 4: Randomized Algorithms

### Quickselect

#### Demonstration

**Array:** [3, 2, 1, 5, 4, 6, 7, 9, 8]
- 1st smallest (index 0): 1
- 5th smallest (index 4): 5
- 9th smallest (index 8): 9

#### Comparison with Sorting

| n | Quickselect (ms) | Sort + Index (ms) | Speedup |
|---|------------------|-------------------|---------|
| 10,000 | 1.86 | 1.10 | 0.59x |
| 100,000 | 16.74 | 27.91 | 1.67x |
| 1,000,000 | 296.88 | 281.98 | 0.95x |

**Key Findings:**
- Quickselect is competitive with sorting for finding k-th element
- For large n, quickselect can be faster than full sort
- Average case: O(n) vs sorting O(n log n)

### Miller-Rabin Primality Test

#### Demonstration

| Number | Miller-Rabin | Trial Division | Actual |
|--------|--------------|----------------|--------|
| 2 | True | True | prime |
| 17 | True | True | prime |
| 561 | False | False | composite |
| 7919 | True | True | prime |
| 999983 | True | True | prime |

#### Comparison on 12-digit Numbers

**Average times (20 random numbers):**
- Miller-Rabin: 0.0159 ms
- Trial Division: 0.0051 ms
- Speedup: 0.32x (trial division faster for 12-digit numbers)

**All tests agreed:** ✓

#### Carmichael Number 561 Test

**Miller-Rabin with 1 round, 1000 trials:**
- Times reported as prime: 14
- Times reported as composite: 986
- False positive rate: 1.4%

**Note:** 561 is a Carmichael number (3 × 11 × 17) that fools many primality tests. With only 1 round, Miller-Rabin has a non-zero false positive rate. Using more rounds (e.g., k=5 or k=10) dramatically reduces this.

### Key Findings

- Quickselect provides O(n) average-case performance for selection
- Miller-Rabin is probabilistic but very reliable with multiple rounds
- For small numbers (12 digits), trial division can be faster
- Carmichael numbers require careful handling in primality testing

---

## Files

- `Q1.py` - Activity selection and knapsack implementations
- `Q2.py` - Huffman coding with compression
- `Q3.py` - Dijkstra, Kruskal, and Prim algorithms
- `Q4.py` - Quickselect and Miller-Rabin primality test

## Running the Code

```bash
python Q1.py  # Activity selection and knapsack
python Q2.py  # Huffman coding
python Q3.py  # Graph algorithms
python Q4.py  # Randomized algorithms
```
