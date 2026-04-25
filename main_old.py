"""
Knapsack Problem Solver GUI

Main application with GUI for inputting items, running algorithms, and visualizing results.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from knapsack import Item, greedy_fractional_knapsack, dynamic_programming_knapsack, branch_and_bound_knapsack
from visualization import plot_dp_table, plot_comparison, plot_selected_items

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Problem Solver")
        self.root.geometry("1000x700")

        self.items = []

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Input tab
        self.input_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.input_frame, text="Input")

        # Results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")

        # Visualization tab
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="Visualization")

        self.setup_input_tab()
        self.setup_results_tab()
        self.setup_viz_tab()

        self.results = {}

    def setup_input_tab(self):
        # Capacity input
        ttk.Label(self.input_frame, text="Knapsack Capacity:").grid(row=0, column=0, padx=10, pady=10)
        self.capacity_var = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.capacity_var).grid(row=0, column=1, padx=10, pady=10)

        # Items list
        ttk.Label(self.input_frame, text="Items:").grid(row=1, column=0, padx=10, pady=10)
        self.items_listbox = tk.Listbox(self.input_frame, height=10, width=50)
        self.items_listbox.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        button_frame = ttk.Frame(self.input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Item", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Item", command=self.remove_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_items).pack(side=tk.LEFT, padx=5)

        # Run buttons
        run_frame = ttk.Frame(self.input_frame)
        run_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(run_frame, text="Run Greedy", command=self.run_greedy).pack(side=tk.LEFT, padx=5)
        ttk.Button(run_frame, text="Run DP", command=self.run_dp).pack(side=tk.LEFT, padx=5)
        ttk.Button(run_frame, text="Run Branch & Bound", command=self.run_bb).pack(side=tk.LEFT, padx=5)
        ttk.Button(run_frame, text="Run All", command=self.run_all).pack(side=tk.LEFT, padx=5)

    def setup_results_tab(self):
        self.results_text = tk.Text(self.results_frame, height=20, width=80)
        self.results_text.pack(padx=10, pady=10)

    def setup_viz_tab(self):
        self.viz_notebook = ttk.Notebook(self.viz_frame)
        self.viz_notebook.pack(fill=tk.BOTH, expand=True)

        # DP Table tab
        self.dp_frame = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(self.dp_frame, text="DP Table")

        # Comparison tab
        self.comp_frame = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(self.comp_frame, text="Comparison")

        # Selected Items tabs
        self.greedy_viz_frame = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(self.greedy_viz_frame, text="Greedy Items")

        self.dp_viz_frame = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(self.dp_viz_frame, text="DP Items")

        self.bb_viz_frame = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(self.bb_viz_frame, text="B&B Items")

    def add_item(self):
        name = simpledialog.askstring("Item Name", "Enter item name:")
        if not name:
            return
        weight = simpledialog.askfloat("Weight", "Enter weight:")
        if weight is None or weight <= 0:
            messagebox.showerror("Error", "Invalid weight")
            return
        value = simpledialog.askfloat("Value", "Enter value:")
        if value is None or value < 0:
            messagebox.showerror("Error", "Invalid value")
            return

        item = Item(name, weight, value)
        self.items.append(item)
        self.update_items_list()

    def remove_item(self):
        selection = self.items_listbox.curselection()
        if selection:
            index = selection[0]
            del self.items[index]
            self.update_items_list()

    def clear_items(self):
        self.items = []
        self.update_items_list()

    def update_items_list(self):
        self.items_listbox.delete(0, tk.END)
        for item in self.items:
            self.items_listbox.insert(tk.END, f"{item.name}: w={item.weight}, v={item.value}")

    def get_capacity(self):
        try:
            capacity = float(self.capacity_var.get())
            if capacity <= 0:
                raise ValueError
            return capacity
        except ValueError:
            messagebox.showerror("Error", "Invalid capacity")
            return None

    def run_greedy(self):
        capacity = self.get_capacity()
        if capacity is None or not self.items:
            return

        selected, total_value = greedy_fractional_knapsack(self.items, capacity)
        self.results['Greedy'] = {'selected': selected, 'value': total_value}
        self.update_results()
        self.update_viz()

    def run_dp(self):
        capacity = self.get_capacity()
        if capacity is None or not self.items:
            return

        capacity = int(capacity)  # DP needs integer capacity
        dp_table, selected, total_value = dynamic_programming_knapsack(self.items, capacity)
        self.results['DP'] = {'selected': [(item, 1.0) for item in selected], 'value': total_value, 'dp_table': dp_table}
        self.update_results()
        self.update_viz()

    def run_bb(self):
        capacity = self.get_capacity()
        if capacity is None or not self.items:
            return

        selected, total_value = branch_and_bound_knapsack(self.items, capacity)
        self.results['Branch & Bound'] = {'selected': [(item, 1.0) for item in selected], 'value': total_value}
        self.update_results()
        self.update_viz()

    def run_all(self):
        self.run_greedy()
        self.run_dp()
        self.run_bb()

    def update_results(self):
        self.results_text.delete(1.0, tk.END)
        for algo, data in self.results.items():
            self.results_text.insert(tk.END, f"{algo}:\n")
            self.results_text.insert(tk.END, f"Total Value: {data['value']:.2f}\n")
            self.results_text.insert(tk.END, "Selected Items:\n")
            for item, fraction in data['selected']:
                if fraction == 1.0:
                    self.results_text.insert(tk.END, f"  {item.name} (full)\n")
                else:
                    self.results_text.insert(tk.END, f"  {item.name} ({fraction:.2f})\n")
            self.results_text.insert(tk.END, "\n")

    def update_viz(self):
        # Clear previous plots
        for widget in self.dp_frame.winfo_children():
            widget.destroy()
        for widget in self.comp_frame.winfo_children():
            widget.destroy()
        for widget in self.greedy_viz_frame.winfo_children():
            widget.destroy()
        for widget in self.dp_viz_frame.winfo_children():
            widget.destroy()
        for widget in self.bb_viz_frame.winfo_children():
            widget.destroy()

        # DP Table
        if 'DP' in self.results and 'dp_table' in self.results['DP']:
            fig, ax = plt.subplots(figsize=(8, 6))
            plot_dp_table(self.results['DP']['dp_table'], self.items, int(self.get_capacity()), ax)
            canvas = FigureCanvasTkAgg(fig, master=self.dp_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Comparison
        if len(self.results) > 1:
            fig, ax = plt.subplots(figsize=(8, 5))
            comp_data = {k: v['value'] for k, v in self.results.items()}
            plot_comparison(comp_data, ax)
            canvas = FigureCanvasTkAgg(fig, master=self.comp_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Selected Items
        if 'Greedy' in self.results:
            fig, ax = plt.subplots(figsize=(8, 5))
            plot_selected_items(self.results['Greedy']['selected'], 'Greedy', ax)
            canvas = FigureCanvasTkAgg(fig, master=self.greedy_viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        if 'DP' in self.results:
            fig, ax = plt.subplots(figsize=(8, 5))
            plot_selected_items(self.results['DP']['selected'], 'DP', ax)
            canvas = FigureCanvasTkAgg(fig, master=self.dp_viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        if 'Branch & Bound' in self.results:
            fig, ax = plt.subplots(figsize=(8, 5))
            plot_selected_items(self.results['Branch & Bound']['selected'], 'Branch & Bound', ax)
            canvas = FigureCanvasTkAgg(fig, master=self.bb_viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()