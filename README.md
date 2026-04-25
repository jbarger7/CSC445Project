# CSC445Project

Knapsack Problem Solver

This tool implements and visualizes three different approaches to solving the Knapsack problem with a modern, user-friendly GUI.

## Features

- **Modern GUI**: Clean interface with card-based design, progress bars, and status updates
- **Interactive Input**: Easy item management with validation and visual feedback
- **Real-time Results**: Formatted results display with algorithm comparisons
- **Rich Visualizations**: DP table, comparison charts, and selected item breakdowns
- **Asynchronous Processing**: Non-blocking algorithm execution with progress tracking

## Algorithms Implemented

1. **Greedy (Fractional Knapsack)**: Fast approximation, allows fractional items
2. **Dynamic Programming (0/1 Knapsack)**: Optimal solution with DP table visualization
3. **Branch & Bound (0/1 Knapsack)**: Efficient pruning for large problems

## GUI Layout

- **Input Tab**: Set capacity, manage items, run algorithms
- **Results Tab**: Detailed algorithm outputs and comparisons
- **Visualization Tab**: Charts and DP table display

## Installation & Usage

1. Install Python 3.x and dependencies: `pip install -r requirements.txt`
2. Run: `python main.py`
3. Add items, set capacity, choose algorithms to run

## Algorithm Analysis

### When Each Approach is Optimal

- **Greedy**: Best for fractional knapsack or when speed > accuracy
- **DP**: Optimal for 0/1 problems with reasonable capacity limits
- **Branch & Bound**: Superior for 0/1 when DP is too slow due to high capacity


LATEST COPILOT RESPONSE
"
Why the results are correct
Your output is exactly what should happen for these algorithms:

Greedy is solving the fractional knapsack variant.
DP and Branch & Bound are solving the 0/1 knapsack variant.
What happened in your test
Your items:

apple: 10 weight, 60 value
orange: 20 weight, 100 value
banana: 30 weight, 120 value
capacity: 50
Greedy chooses:

apple (full)
orange (full)
banana at 0.67 fraction
That is allowed in fractional knapsack, so total = 60 + 100 + 80 = 240.

DP and B&B choose:

orange (full)
banana (full)
Because in 0/1 knapsack you cannot take fractional items, the best value with 50 capacity is 220.

Key point
Greedy = 240 is optimal for the fractional case.
DP = 220 and Branch & Bound = 220 are optimal for the 0/1 case.
So the comparison is showing the expected behavior: greedy can do better only because it is allowed to split items.
If you want a fair 0/1 comparison
Use a dataset where fractional selection is not possible or compare only the 0/1 algorithms:

Greedy should be treated as an approximate algorithm only for 0/1 knapsack.
DP and B&B are the true exact solvers for 0/1.
If you want, I can also make the UI explicitly label Greedy as “Fractional Knapsack” and the others as “0/1 Knapsack” so this distinction is clearer.
"