"""
Knapsack Problem Algorithms Implementation

This module contains implementations of three approaches to solve the Knapsack problem:
1. Greedy (Fractional Knapsack)
2. Dynamic Programming (0/1 Knapsack)
3. Branch & Bound (0/1 Knapsack)
"""

import heapq

class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value
        self.ratio = value / weight if weight > 0 else 0

    def __repr__(self):
        return f"Item({self.name}, w={self.weight}, v={self.value})"

def greedy_fractional_knapsack(items, capacity):
    """
    Greedy algorithm for fractional knapsack.
    Sorts items by value/weight ratio and takes as much as possible.
    Returns selected items with fractions and total value.
    """
    # Sort items by ratio descending
    sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)

    total_value = 0
    selected = []

    for item in sorted_items:
        if capacity >= item.weight:
            # Take whole item
            selected.append((item, 1.0))
            total_value += item.value
            capacity -= item.weight
        elif capacity > 0:
            # Take fraction
            fraction = capacity / item.weight
            selected.append((item, fraction))
            total_value += item.value * fraction
            capacity = 0
        else:
            break

    return selected, total_value

def dynamic_programming_knapsack(items, capacity):
    """
    Dynamic Programming for 0/1 Knapsack.
    Returns DP table, selected items, total value, and intermediate steps.
    """
    # DP only supports integer weights/capacity
    weights = []
    for item in items:
        if abs(item.weight - int(item.weight)) > 1e-9:
            raise ValueError("DP algorithm requires integer item weights.")
        weights.append(int(item.weight))

    if abs(capacity - int(capacity)) > 1e-9:
        raise ValueError("DP algorithm requires integer capacity.")
    capacity = int(capacity)

    n = len(items)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    dp_steps = []

    # Build DP table and capture steps
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + items[i-1].value)
            else:
                dp[i][w] = dp[i-1][w]
        # Store a copy of current state after processing each item
        dp_steps.append([row[:] for row in dp])

    # Backtrack to find selected items
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if w >= 0 and dp[i][w] != dp[i-1][w]:
            selected.append(items[i-1])
            w -= weights[i-1]

    total_value = dp[n][capacity]
    return dp, selected, total_value, dp_steps

class Node:
    def __init__(self, level, profit, weight, bound, selected):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.bound = bound
        self.selected = selected[:]

    def __lt__(self, other):
        return self.bound > other.bound  # Max heap

def branch_and_bound_knapsack(items, capacity):
    """
    Branch & Bound for 0/1 Knapsack.
    Returns selected items and total value.
    """
    n = len(items)
    # Sort by value descending for better pruning
    items = sorted(items, key=lambda x: x.value, reverse=True)

    def bound(u):
        if u.weight >= capacity:
            return 0
        profit_bound = u.profit
        j = u.level + 1
        totweight = u.weight
        while j < n and totweight + items[j].weight <= capacity:
            totweight += items[j].weight
            profit_bound += items[j].value
            j += 1
        if j < n:
            profit_bound += (capacity - totweight) * (items[j].value / items[j].weight)
        return profit_bound

    pq = []
    u = Node(-1, 0, 0, 0, [])
    max_profit = 0
    best_selected = []

    heapq.heappush(pq, u)

    while pq:
        u = heapq.heappop(pq)
        if u.level == n - 1:
            continue

        v = Node(u.level + 1, u.profit, u.weight, 0, u.selected[:])

        # Not take
        v.bound = bound(v)
        if v.bound > max_profit:
            heapq.heappush(pq, v)

        # Take
        v.weight += items[v.level].weight
        if v.weight <= capacity:
            v.profit += items[v.level].value
            v.selected.append(items[v.level])
            if v.profit > max_profit:
                max_profit = v.profit
                best_selected = v.selected[:]
            v.bound = bound(v)
            if v.bound > max_profit:
                heapq.heappush(pq, v)

    return best_selected, max_profit