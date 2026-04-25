"""
Visualization module for Knapsack problem

Handles plotting DP table, comparison charts, etc.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.table import Table

def plot_dp_table(dp_table, items, capacity, ax=None):
    """
    Plot the DP table as a heatmap with values.
    For large capacities, show a summary instead.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    if capacity > 50:
        ax.text(0.5, 0.5, f'DP Table too large to display\n(Capacity: {capacity})\n\nFinal value: {dp_table[-1][-1]}',
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
        ax.set_title('DP Table Summary')
        ax.axis('off')
        return ax

    # Create table
    table = ax.table(cellText=dp_table,
                     rowLabels=[''] + [item.name for item in items],
                     colLabels=['Weight'] + [str(i) for i in range(1, capacity + 1)],
                     cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    ax.axis('off')
    ax.set_title('DP Table - Tracking Maximum Value by Item & Weight')

    return ax

def plot_dp_table_step(dp_table, items, capacity, current_step, total_steps, ax=None):
    """
    Plot the DP table at a specific step of construction.
    current_step: which item row was last processed (0-indexed, -1 for initial)
    total_steps: total number of items
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    if capacity > 50:
        if current_step == -1:
            step_text = "Initial state (before processing)"
        else:
            step_text = f"After processing: {items[current_step].name}"
        ax.text(0.5, 0.5, f'DP Table too large to display\n(Capacity: {capacity})\n\n{step_text}\nFinal value so far: {dp_table[-1][-1]}',
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
        ax.set_title(f'DP Table Step {current_step + 2}/{total_steps + 1}')
        ax.axis('off')
        return ax

    # Create table
    table = ax.table(cellText=dp_table,
                     rowLabels=[''] + [item.name for item in items],
                     colLabels=['Weight'] + [str(i) for i in range(1, capacity + 1)],
                     cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    ax.axis('off')
    if current_step == -1:
        title_text = "DP Table - Initial State"
    else:
        title_text = f"DP Table - After Processing: {items[current_step].name}"
    ax.set_title(f'{title_text} (Step {current_step + 2}/{total_steps + 1})')

    return ax

def plot_comparison(results, ax=None):
    """
    Plot bar chart comparing total values from each algorithm.
    results: dict with keys 'Greedy', 'DP', 'Branch & Bound' and values as total_value
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    algorithms = list(results.keys())
    values = list(results.values())

    bars = ax.bar(algorithms, values, color=['blue', 'green', 'red'])
    ax.set_ylabel('Total Value')
    ax.set_title('Algorithm Comparison')
    ax.set_ylim(0, max(values) * 1.1)

    # Add value labels on bars
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.2f}', ha='center', va='bottom')

    return ax

def plot_selected_items(selected_items, algorithm_name, ax=None):
    """
    Plot selected items for a specific algorithm.
    For fractional, show fractions.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if not selected_items:
        ax.text(0.5, 0.5, 'No items selected', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{algorithm_name} - Selected Items')
        ax.axis('off')
        return ax

    names = []
    values = []

    for item, fraction in selected_items:
        names.append(item.name)
        values.append(item.value * fraction)

    bars = ax.bar(names, values, color='skyblue')
    ax.set_ylabel('Value')
    ax.set_title(f'{algorithm_name} - Selected Items')
    ax.set_ylim(0, max(values) * 1.1)

    # Add fraction labels if fractional
    for bar, (item, fraction) in zip(bars, selected_items):
        if fraction < 1.0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{fraction:.2f}', ha='center', va='bottom')

    return ax