import random
import time

# ============== ACTIVITY SELECTION ==============

def activity_selection_earliest_finish(activities):
    """
    Greedy activity selection using earliest finish time
    Returns: list of selected activities (start, finish)
    """
    # Sort by finish time
    sorted_activities = sorted(activities, key=lambda x: x[1])
    
    selected = []
    last_finish = float('-inf')
    
    for start, finish in sorted_activities:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish
    
    return selected

def activity_selection_earliest_start(activities):
    """
    Greedy activity selection using earliest start time
    """
    sorted_activities = sorted(activities, key=lambda x: x[0])
    
    selected = []
    last_finish = float('-inf')
    
    for start, finish in sorted_activities:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish
    
    return selected

def activity_selection_shortest_duration(activities):
    """
    Greedy activity selection using shortest duration
    """
    sorted_activities = sorted(activities, key=lambda x: x[1] - x[0])
    
    selected = []
    last_finish = float('-inf')
    
    for start, finish in sorted_activities:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish
    
    return selected

def find_counterexample():
    """
    Find random inputs where earliest start and shortest duration give smaller answers
    than earliest finish
    """
    print("=" * 80)
    print("Finding Counterexamples for Greedy Activity Selection Rules")
    print("=" * 80)
    print()
    
    found_early_start = False
    found_shortest = False
    
    attempts = 0
    max_attempts = 10000
    
    while attempts < max_attempts and (not found_early_start or not found_shortest):
        attempts += 1
        
        # Generate random activities
        n = random.randint(5, 10)
        activities = []
        for _ in range(n):
            start = random.randint(0, 20)
            duration = random.randint(1, 10)
            finish = start + duration
            activities.append((start, finish))
        
        # Run all three algorithms
        earliest_finish = activity_selection_earliest_finish(activities)
        earliest_start = activity_selection_earliest_start(activities)
        shortest = activity_selection_shortest_duration(activities)
        
        ef_count = len(earliest_finish)
        es_count = len(earliest_start)
        sd_count = len(shortest)
        
        # Check if earliest start gives smaller answer
        if not found_early_start and es_count < ef_count:
            print(f"Found counterexample for earliest start (attempt {attempts}):")
            print(f"Activities: {activities}")
            print(f"Earliest finish: {ef_count} activities")
            print(f"Earliest start: {es_count} activities")
            print(f"Shortest duration: {sd_count} activities")
            print()
            found_early_start = True
        
        # Check if shortest duration gives smaller answer
        if not found_shortest and sd_count < ef_count:
            print(f"Found counterexample for shortest duration (attempt {attempts}):")
            print(f"Activities: {activities}")
            print(f"Earliest finish: {ef_count} activities")
            print(f"Earliest start: {es_count} activities")
            print(f"Shortest duration: {sd_count} activities")
            print()
            found_shortest = True
    
    if not found_early_start:
        print("Could not find counterexample for earliest start after 10000 attempts")
    
    if not found_shortest:
        print("Could not find counterexample for shortest duration after 10000 attempts")
    
    print("=" * 80)
    print()

# ============== KNAPSACK ==============

def fractional_knapsack(items, capacity):
    """
    Fractional knapsack using value/weight ratio
    items: list of (value, weight)
    Returns: maximum value
    """
    # Sort by value/weight ratio in descending order
    sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    
    total_value = 0
    remaining_capacity = capacity
    
    for value, weight in sorted_items:
        if remaining_capacity >= weight:
            total_value += value
            remaining_capacity -= weight
        else:
            # Take fraction of the item
            fraction = remaining_capacity / weight
            total_value += value * fraction
            remaining_capacity = 0
            break
    
    return total_value

def knapsack_0_1_greedy(items, capacity):
    """
    0/1 knapsack using greedy value/weight ratio (not optimal)
    items: list of (value, weight)
    Returns: maximum value
    """
    # Sort by value/weight ratio in descending order
    sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    
    total_value = 0
    remaining_capacity = capacity
    
    for value, weight in sorted_items:
        if remaining_capacity >= weight:
            total_value += value
            remaining_capacity -= weight
    
    return total_value

def knapsack_0_1_dp(items, capacity):
    """
    0/1 knapsack using DP (optimal)
    items: list of (value, weight)
    Returns: maximum value
    """
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        value, weight = items[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]

def compare_knapsack():
    """
    Compare greedy vs DP for 0/1 knapsack on random inputs
    Report worst ratio of greedy to optimal
    """
    print("=" * 80)
    print("Comparing Greedy vs DP for 0/1 Knapsack")
    print("=" * 80)
    print()
    
    worst_ratio = 1.0
    worst_example = None
    
    for i in range(1000):
        # Generate random items
        n = random.randint(5, 20)
        items = []
        for _ in range(n):
            value = random.randint(1, 100)
            weight = random.randint(1, 50)
            items.append((value, weight))
        
        capacity = random.randint(10, 100)
        
        # Run both algorithms
        greedy_value = knapsack_0_1_greedy(items, capacity)
        dp_value = knapsack_0_1_dp(items, capacity)
        
        # Calculate ratio
        if dp_value > 0:
            ratio = greedy_value / dp_value
            if ratio < worst_ratio:
                worst_ratio = ratio
                worst_example = (items, capacity, greedy_value, dp_value)
    
    print(f"Worst ratio of greedy to optimal: {worst_ratio:.4f}")
    if worst_example:
        items, capacity, greedy_value, dp_value = worst_example
        print(f"Example with worst ratio:")
        print(f"  Items: {items}")
        print(f"  Capacity: {capacity}")
        print(f"  Greedy value: {greedy_value}")
        print(f"  Optimal value: {dp_value}")
    print("=" * 80)
    print()

# ============== DEMONSTRATION ==============
def demonstrate_activity_selection():
    print("=" * 80)
    print("Activity Selection Demonstration")
    print("=" * 80)
    print()
    
    # Example activities
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    
    print("Activities (start, finish):")
    for i, (s, f) in enumerate(activities):
        print(f"  A{i+1}: ({s}, {f})")
    print()
    
    # Earliest finish time
    selected = activity_selection_earliest_finish(activities)
    print(f"Earliest finish time - Selected {len(selected)} activities:")
    for i, (s, f) in enumerate(selected):
        print(f"  ({s}, {f})", end='')
        if i < len(selected) - 1:
            print(", ", end='')
    print()
    print()
    
    # Earliest start time
    selected = activity_selection_earliest_start(activities)
    print(f"Earliest start time - Selected {len(selected)} activities:")
    for i, (s, f) in enumerate(selected):
        print(f"  ({s}, {f})", end='')
        if i < len(selected) - 1:
            print(", ", end='')
    print()
    print()
    
    # Shortest duration
    selected = activity_selection_shortest_duration(activities)
    print(f"Shortest duration - Selected {len(selected)} activities:")
    for i, (s, f) in enumerate(selected):
        print(f"  ({s}, {f})", end='')
        if i < len(selected) - 1:
            print(", ", end='')
    print()
    print("=" * 80)
    print()

def demonstrate_knapsack():
    print("=" * 80)
    print("Knapsack Demonstration")
    print("=" * 80)
    print()
    
    # Example items
    items = [(60, 10), (100, 20), (120, 30)]
    capacity = 50
    
    print("Items (value, weight):")
    for i, (v, w) in enumerate(items):
        print(f"  Item {i+1}: value={v}, weight={w}")
    print(f"Capacity: {capacity}")
    print()
    
    # Fractional knapsack
    fractional_value = fractional_knapsack(items, capacity)
    print(f"Fractional knapsack value: {fractional_value}")
    print()
    
    # 0/1 knapsack
    greedy_value = knapsack_0_1_greedy(items, capacity)
    dp_value = knapsack_0_1_dp(items, capacity)
    print(f"0/1 knapsack (greedy): {greedy_value}")
    print(f"0/1 knapsack (DP): {dp_value}")
    print(f"Ratio: {greedy_value / dp_value:.4f}")
    print("=" * 80)
    print()

# ============== MAIN FUNCTION ==============
def main():
    demonstrate_activity_selection()
    find_counterexample()
    demonstrate_knapsack()
    compare_knapsack()

if __name__ == "__main__":
    main()
