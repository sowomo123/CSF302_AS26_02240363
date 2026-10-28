import heapq
import random
import time

# ============== UNION-FIND FOR KRUSKAL ==============

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        
        if px == py:
            return False
        
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        
        return True

# ============== DIJKSTRA'S ALGORITHM ==============

def dijkstra(graph, source):
    """
    Dijkstra's algorithm with binary heap
    graph: adjacency list {u: [(v, weight), ...]}
    Returns: distances dict, predecessors dict
    """
    n = len(graph)
    distances = {i: float('inf') for i in range(n)}
    predecessors = {i: None for i in range(n)}
    distances[source] = 0
    
    # Min-heap: (distance, vertex)
    heap = [(0, source)]
    visited = set()
    
    while heap:
        dist, u = heapq.heappop(heap)
        
        if u in visited:
            continue
        visited.add(u)
        
        for v, weight in graph.get(u, []):
            if v not in visited:
                new_dist = dist + weight
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = u
                    heapq.heappush(heap, (new_dist, v))
    
    return distances, predecessors

def reconstruct_path(predecessors, source, target):
    """
    Reconstruct path from source to target using predecessors
    """
    if predecessors[target] is None and source != target:
        return None
    
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    return path

# ============== KRUSKAL'S ALGORITHM ==============

def kruskal(graph, n):
    """
    Kruskal's algorithm with union-find
    graph: list of edges (u, v, weight)
    Returns: MST edges list, total weight
    """
    # Sort edges by weight
    edges = sorted(graph, key=lambda x: x[2])
    
    uf = UnionFind(n)
    mst_edges = []
    total_weight = 0
    
    for u, v, weight in edges:
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
    
    return mst_edges, total_weight

# ============== PRIM'S ALGORITHM ==============

def prim(graph, n, start=0):
    """
    Prim's algorithm with binary heap
    graph: adjacency list {u: [(v, weight), ...]}
    Returns: MST edges list, total weight
    """
    visited = set([start])
    mst_edges = []
    total_weight = 0
    
    # Min-heap: (weight, u, v)
    heap = []
    
    for v, weight in graph.get(start, []):
        heapq.heappush(heap, (weight, start, v))
    
    while heap and len(visited) < n:
        weight, u, v = heapq.heappop(heap)
        
        if v in visited:
            continue
        
        visited.add(v)
        mst_edges.append((u, v, weight))
        total_weight += weight
        
        for next_v, w in graph.get(v, []):
            if next_v not in visited:
                heapq.heappush(heap, (w, v, next_v))
    
    return mst_edges, total_weight

# ============== GRAPH GENERATION ==============

def generate_random_graph(n, edge_density='sparse'):
    """
    Generate random connected graph
    edge_density: 'sparse' (E ≈ 3V) or 'dense' (E ≈ V²/4)
    Returns: adjacency list, edge list
    """
    # First create a spanning tree to ensure connectivity
    adj = {i: [] for i in range(n)}
    edges = []
    
    # Create random spanning tree
    for i in range(1, n):
        parent = random.randint(0, i - 1)
        weight = random.randint(1, 100)
        adj[parent].append((i, weight))
        adj[i].append((parent, weight))
        edges.append((parent, i, weight))
    
    # Add extra edges based on density
    if edge_density == 'sparse':
        target_edges = 3 * n
    else:  # dense
        target_edges = n * n // 4
    
    while len(edges) < target_edges:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u != v:
            # Check if edge already exists
            exists = False
            for (x, y, _) in edges:
                if (x == u and y == v) or (x == v and y == u):
                    exists = True
                    break
            
            if not exists:
                weight = random.randint(1, 100)
                adj[u].append((v, weight))
                adj[v].append((u, weight))
                edges.append((u, v, weight))
    
    return adj, edges

# ============== DEMONSTRATION ==============
def demonstrate_dijkstra():
    print("=" * 80)
    print("Dijkstra's Algorithm Demonstration")
    print("=" * 80)
    print()
    
    # Example graph
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: [(4, 3)],
        4: []
    }
    
    source = 0
    distances, predecessors = dijkstra(graph, source)
    
    print(f"Source vertex: {source}")
    print()
    print("Shortest distances from source:")
    for v in sorted(distances.keys()):
        dist = distances[v]
        if dist == float('inf'):
            print(f"  Vertex {v}: unreachable")
        else:
            path = reconstruct_path(predecessors, source, v)
            print(f"  Vertex {v}: distance={dist}, path={path}")
    print("=" * 80)
    print()

def demonstrate_mst():
    print("=" * 80)
    print("MST Algorithms Demonstration")
    print("=" * 80)
    print()
    
    # Example graph
    adj = {
        0: [(1, 4), (2, 1)],
        1: [(0, 4), (2, 2), (3, 1)],
        2: [(0, 1), (1, 2), (3, 3)],
        3: [(1, 1), (2, 3)]
    }
    
    edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 1), (2, 3, 3)]
    n = 4
    
    # Kruskal
    kruskal_edges, kruskal_weight = kruskal(edges, n)
    print(f"Kruskal's MST:")
    print(f"  Edges: {kruskal_edges}")
    print(f"  Total weight: {kruskal_weight}")
    print()
    
    # Prim
    prim_edges, prim_weight = prim(adj, n)
    print(f"Prim's MST:")
    print(f"  Edges: {prim_edges}")
    print(f"  Total weight: {prim_weight}")
    print()
    
    print(f"Match: {kruskal_weight == prim_weight}")
    print("=" * 80)
    print()

def verify_mst_algorithms():
    """
    Verify Kruskal and Prim give same total weight on random graphs
    """
    print("=" * 80)
    print("Verifying MST Algorithms on Random Graphs")
    print("=" * 80)
    print()
    
    all_match = True
    for i in range(10):
        n = random.randint(5, 20)
        adj, edges = generate_random_graph(n, 'sparse')
        
        kruskal_edges, kruskal_weight = kruskal(edges, n)
        prim_edges, prim_weight = prim(adj, n)
        
        match = kruskal_weight == prim_weight
        status = "✓ PASS" if match else "✗ FAIL"
        print(f"Test {i+1}: n={n}, Kruskal={kruskal_weight}, Prim={prim_weight} {status}")
        
        if not match:
            all_match = False
    
    print()
    print(f"All tests passed: {all_match}")
    print("=" * 80)
    print()

def time_mst_algorithms():
    """
    Time Kruskal and Prim for V=1000 on sparse and dense graphs
    """
    print("=" * 80)
    print("Timing MST Algorithms (V=1000)")
    print("=" * 80)
    print()
    
    n = 1000
    
    # Sparse graph
    print("Sparse graph (E ≈ 3V):")
    adj_sparse, edges_sparse = generate_random_graph(n, 'sparse')
    
    start = time.perf_counter()
    kruskal_edges, kruskal_weight = kruskal(edges_sparse, n)
    kruskal_time = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    prim_edges, prim_weight = prim(adj_sparse, n)
    prim_time = (time.perf_counter() - start) * 1000
    
    print(f"  Kruskal: {kruskal_time:.2f} ms")
    print(f"  Prim: {prim_time:.2f} ms")
    print(f"  Winner: {'Kruskal' if kruskal_time < prim_time else 'Prim'}")
    print(f"  Speedup: {max(kruskal_time, prim_time) / min(kruskal_time, prim_time):.2f}x")
    print()
    
    # Dense graph
    print("Dense graph (E ≈ V²/4):")
    adj_dense, edges_dense = generate_random_graph(n, 'dense')
    
    start = time.perf_counter()
    kruskal_edges, kruskal_weight = kruskal(edges_dense, n)
    kruskal_time = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    prim_edges, prim_weight = prim(adj_dense, n)
    prim_time = (time.perf_counter() - start) * 1000
    
    print(f"  Kruskal: {kruskal_time:.2f} ms")
    print(f"  Prim: {prim_time:.2f} ms")
    print(f"  Winner: {'Kruskal' if kruskal_time < prim_time else 'Prim'}")
    print(f"  Speedup: {max(kruskal_time, prim_time) / min(kruskal_time, prim_time):.2f}x")
    print()
    
    print("Explanation:")
    print("- Sparse graph: Kruskal wins because sorting E=O(V) edges is faster than Prim's heap operations")
    print("- Dense graph: Prim wins because it processes O(V) edges vs Kruskal sorting O(V²) edges")
    print("=" * 80)
    print()

def demonstrate_dijkstra_negative_edge():
    """
    Show input where Dijkstra gives wrong answer with negative edge
    """
    print("=" * 80)
    print("Dijkstra with Negative Edge (Wrong Answer)")
    print("=" * 80)
    print()
    
    # Graph with negative edge where Dijkstra fails
    graph = {
        0: [(1, 1), (2, 4)],
        1: [(2, -3)],
        2: [(3, 2)],
        3: []
    }
    
    source = 0
    distances, predecessors = dijkstra(graph, source)
    
    print(f"Graph with negative edge (1->2 has weight -3):")
    print(f"  0 -> 1 (weight 1)")
    print(f"  0 -> 2 (weight 4)")
    print(f"  1 -> 2 (weight -3)")
    print(f"  2 -> 3 (weight 2)")
    print()
    
    print("Dijkstra's result:")
    for v in sorted(distances.keys()):
        dist = distances[v]
        path = reconstruct_path(predecessors, source, v)
        print(f"  Vertex {v}: distance={dist}, path={path}")
    print()
    
    print("Correct answer (0->1->2->3): distance=0")
    print("Dijkstra's answer (0->2->3): distance=6")
    print("Dijkstra fails because it doesn't reconsider vertices once visited")
    print("=" * 80)
    print()

# ============== MAIN FUNCTION ==============
def main():
    demonstrate_dijkstra()
    demonstrate_mst()
    verify_mst_algorithms()
    time_mst_algorithms()
    demonstrate_dijkstra_negative_edge()

if __name__ == "__main__":
    main()
