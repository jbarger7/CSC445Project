"""
Knapsack Problem Solver GUI

Main application with GUI for inputting items, running algorithms, and visualizing results.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from knapsack import Item, greedy_fractional_knapsack, dynamic_programming_knapsack, branch_and_bound_knapsack
from visualization import plot_dp_table, plot_dp_table_step, plot_comparison, plot_selected_items
import threading

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Problem Solver")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # Set style
        style = ttk.Style()
        style.theme_use('clam')  # Modern theme
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=6)
        style.configure('TLabel', font=('Arial', 10), background='#f0f0f0')
        style.configure('TEntry', font=('Arial', 10), padding=5)
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])
        style.configure('Card.TFrame', background='white', relief='raised', borderwidth=2)

        self.items = []
        self.is_running = False
        self.current_dp_step = -1  # Track current step in DP visualization

        # Create main frame
        main_frame = ttk.Frame(root, style='Card.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(main_frame, text="Knapsack Problem Solver", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(20, 10))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Input tab
        self.input_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.input_frame, text="Input")

        # Results tab
        self.results_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.results_frame, text="Results")

        # Visualization tab
        self.viz_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.viz_frame, text="Visualization")

        self.setup_input_tab()
        self.setup_results_tab()
        self.setup_viz_tab()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.results = {}

    def setup_input_tab(self):
        # Capacity input section
        capacity_frame = ttk.LabelFrame(self.input_frame, text="Knapsack Capacity", padding=10)
        capacity_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(capacity_frame, text="Enter capacity:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.capacity_var = tk.StringVar()
        capacity_entry = ttk.Entry(capacity_frame, textvariable=self.capacity_var, width=20)
        capacity_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Items section
        items_frame = ttk.LabelFrame(self.input_frame, text="Items", padding=10)
        items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Items list with scrollbar
        list_frame = ttk.Frame(items_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.items_listbox = tk.Listbox(list_frame, height=8, width=60, font=('Arial', 10),
                                       yscrollcommand=scrollbar.set, selectbackground='#cce7ff')
        self.items_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.items_listbox.yview)

        # Buttons frame
        buttons_frame = ttk.Frame(items_frame)
        buttons_frame.pack(fill=tk.X, pady=10)

        ttk.Button(buttons_frame, text="+ Add Item", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="- Remove Item", command=self.remove_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Clear All", command=self.clear_items).pack(side=tk.LEFT, padx=5)

        # Run section
        run_frame = ttk.LabelFrame(self.input_frame, text="Run Algorithms", padding=10)
        run_frame.pack(fill=tk.X, padx=20, pady=10)

        run_buttons_frame = ttk.Frame(run_frame)
        run_buttons_frame.pack()

        self.run_buttons = []
        button_configs = [
            ("Run Greedy", self.run_greedy),
            ("Run DP", self.run_dp),
            ("Run B&B", self.run_bb),
            ("Run All", self.run_all)
        ]

        for text, command in button_configs:
            btn = ttk.Button(run_buttons_frame, text=text, command=command, state=tk.NORMAL)
            btn.pack(side=tk.LEFT, padx=10, pady=5)
            self.run_buttons.append(btn)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(run_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))

    def setup_results_tab(self):
        results_inner_frame = ttk.Frame(self.results_frame)
        results_inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(results_inner_frame, text="Algorithm Results", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        self.results_text = scrolledtext.ScrolledText(results_inner_frame, height=25, width=80,
                                                     font=('Consolas', 10), wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)

    def setup_viz_tab(self):
        viz_inner_frame = ttk.Frame(self.viz_frame)
        viz_inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(viz_inner_frame, text="Visualizations", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        self.viz_notebook = ttk.Notebook(viz_inner_frame)
        self.viz_notebook.pack(fill=tk.BOTH, expand=True)

        # DP Table tab with navigation
        dp_container = ttk.Frame(self.viz_notebook, style='Card.TFrame')
        self.viz_notebook.add(dp_container, text="DP Table")
        
        # Navigation controls for DP
        dp_control_frame = ttk.Frame(dp_container)
        dp_control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.dp_prev_btn = ttk.Button(dp_control_frame, text="< Previous Step", command=self.prev_dp_step)
        self.dp_prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.dp_step_label = ttk.Label(dp_control_frame, text="Step: 0/0", font=('Arial', 10))
        self.dp_step_label.pack(side=tk.LEFT, padx=20)
        
        self.dp_next_btn = ttk.Button(dp_control_frame, text="Next Step >", command=self.next_dp_step)
        self.dp_next_btn.pack(side=tk.LEFT, padx=5)
        
        self.dp_frame = ttk.Frame(dp_container, style='Card.TFrame')
        self.dp_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Comparison tab
        self.comp_frame = ttk.Frame(self.viz_notebook, style='Card.TFrame')
        self.viz_notebook.add(self.comp_frame, text="Comparison")

        # Selected Items tabs
        self.greedy_viz_frame = ttk.Frame(self.viz_notebook, style='Card.TFrame')
        self.viz_notebook.add(self.greedy_viz_frame, text="Greedy Items")

        self.dp_viz_frame = ttk.Frame(self.viz_notebook, style='Card.TFrame')
        self.viz_notebook.add(self.dp_viz_frame, text="DP Items")

        self.bb_viz_frame = ttk.Frame(self.viz_notebook, style='Card.TFrame')
        self.viz_notebook.add(self.bb_viz_frame, text="B&B Items")

    def add_item(self):
        name = simpledialog.askstring("Add Item", "Enter item name:", parent=self.root)
        if not name:
            return
        weight = simpledialog.askfloat("Add Item", "Enter weight:", parent=self.root)
        if weight is None or weight <= 0:
            messagebox.showerror("Error", "Invalid weight. Must be positive number.", parent=self.root)
            return
        value = simpledialog.askfloat("Add Item", "Enter value:", parent=self.root)
        if value is None or value < 0:
            messagebox.showerror("Error", "Invalid value. Must be non-negative number.", parent=self.root)
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
        else:
            messagebox.showinfo("Info", "Please select an item to remove.", parent=self.root)

    def clear_items(self):
        if messagebox.askyesno("Confirm", "Clear all items?", parent=self.root):
            self.items = []
            self.update_items_list()

    def update_items_list(self):
        self.items_listbox.delete(0, tk.END)
        for i, item in enumerate(self.items, 1):
            self.items_listbox.insert(tk.END, f"{i}. {item.name}: Weight={item.weight}, Value={item.value}, Ratio={item.ratio:.2f}")

    def get_capacity(self):
        try:
            capacity = float(self.capacity_var.get())
            if capacity <= 0:
                raise ValueError
            return capacity
        except ValueError:
            messagebox.showerror("Error", "Invalid capacity. Must be positive number.", parent=self.root)
            return None

    def set_running_state(self, running):
        self.is_running = running
        state = tk.DISABLED if running else tk.NORMAL
        for btn in self.run_buttons:
            btn.config(state=state)
        if running:
            self.progress_var.set(0)
            self.status_var.set("Running algorithm...")
        else:
            self.progress_var.set(100)
            self.status_var.set("Ready")

    def run_algorithm(self, algo_func, algo_name):
        if self.is_running:
            return
        capacity = self.get_capacity()
        if capacity is None or not self.items:
            if not self.items:
                messagebox.showerror("Error", "Please add at least one item.", parent=self.root)
            return

        self.set_running_state(True)
        self.progress_var.set(25)

        def run():
            try:
                result = algo_func()
                self.results.update(result)
                self.root.after(0, self.update_results)
                self.root.after(0, self.update_viz)
                self.root.after(0, lambda: self.set_running_state(False))
                self.root.after(0, lambda: self.status_var.set(f"{algo_name} completed"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Algorithm failed: {str(e)}", parent=self.root))
                self.root.after(0, lambda: self.set_running_state(False))

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    def run_greedy(self):
        def func():
            capacity = float(self.capacity_var.get())
            selected, total_value = greedy_fractional_knapsack(self.items, capacity)
            return {'Greedy': {'selected': selected, 'value': total_value}}
        self.run_algorithm(func, "Greedy")

    def validate_integer_dp_inputs(self):
        capacity = self.get_capacity()
        if capacity is None:
            return None
        if abs(capacity - int(capacity)) > 1e-9:
            messagebox.showerror("Error", "DP requires integer capacity.", parent=self.root)
            return None

        for item in self.items:
            if abs(item.weight - int(item.weight)) > 1e-9:
                messagebox.showerror("Error", "DP requires integer item weights.", parent=self.root)
                return None

        return int(capacity)

    def run_dp(self):
        capacity_int = self.validate_integer_dp_inputs()
        if capacity_int is None:
            return

        def func():
            dp_table, selected, total_value, dp_steps = dynamic_programming_knapsack(self.items, capacity_int)
            return {'DP': {'selected': [(item, 1.0) for item in selected], 'value': total_value, 'dp_table': dp_table, 'dp_steps': dp_steps}}
        self.run_algorithm(func, "Dynamic Programming")

    def run_bb(self):
        def func():
            capacity = float(self.capacity_var.get())
            selected, total_value = branch_and_bound_knapsack(self.items, capacity)
            return {'Branch & Bound': {'selected': [(item, 1.0) for item in selected], 'value': total_value}}
        self.run_algorithm(func, "Branch & Bound")

    def run_all(self):
        if self.is_running:
            return
        capacity = self.get_capacity()
        if capacity is None or not self.items:
            if not self.items:
                messagebox.showerror("Error", "Please add at least one item.", parent=self.root)
            return

        capacity_int = self.validate_integer_dp_inputs()
        if capacity_int is None:
            return

        self.set_running_state(True)
        self.progress_var.set(10)

        def run():
            try:
                # Run Greedy
                selected_g, total_g = greedy_fractional_knapsack(self.items, capacity)
                self.root.after(0, lambda: self.progress_var.set(30))

                # Run DP
                dp_table, selected_dp, total_dp, dp_steps = dynamic_programming_knapsack(self.items, capacity_int)
                self.root.after(0, lambda: self.progress_var.set(60))

                # Run B&B
                selected_bb, total_bb = branch_and_bound_knapsack(self.items, capacity)
                self.root.after(0, lambda: self.progress_var.set(90))

                results = {
                    'Greedy': {'selected': selected_g, 'value': total_g},
                    'DP': {'selected': [(item, 1.0) for item in selected_dp], 'value': total_dp, 'dp_table': dp_table, 'dp_steps': dp_steps},
                    'Branch & Bound': {'selected': [(item, 1.0) for item in selected_bb], 'value': total_bb}
                }

                self.results.update(results)
                self.root.after(0, self.update_results)
                self.root.after(0, self.update_viz)
                self.root.after(0, lambda: self.set_running_state(False))
                self.root.after(0, lambda: self.status_var.set("All algorithms completed"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Algorithms failed: {str(e)}", parent=self.root))
                self.root.after(0, lambda: self.set_running_state(False))

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    def prev_dp_step(self):
        if 'DP' in self.results and 'dp_steps' in self.results['DP']:
            if self.current_dp_step > -1:
                self.current_dp_step -= 1
                self.update_dp_viz()

    def next_dp_step(self):
        if 'DP' in self.results and 'dp_steps' in self.results['DP']:
            if self.current_dp_step < len(self.results['DP']['dp_steps']) - 1:
                self.current_dp_step += 1
                self.update_dp_viz()

    def update_dp_viz(self):
        # Clear previous DP visualization
        for widget in self.dp_frame.winfo_children():
            widget.destroy()

        if 'DP' in self.results and 'dp_steps' in self.results['DP']:
            try:
                capacity_int = int(float(self.capacity_var.get()))
                dp_steps = self.results['DP']['dp_steps']
                total_steps = len(self.results['DP']['dp_steps'])

                # Get the appropriate DP table for current step
                if self.current_dp_step == -1:
                    # Show initial state (all zeros)
                    dp_to_show = [[0 for _ in range(capacity_int + 1)] for _ in range(len(self.items) + 1)]
                else:
                    dp_to_show = dp_steps[self.current_dp_step]

                fig, ax = plt.subplots(figsize=(10, 8))
                plot_dp_table_step(dp_to_show, self.items, capacity_int, self.current_dp_step, len(self.items), ax)
                canvas = FigureCanvasTkAgg(fig, master=self.dp_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                # Update step label and button states
                self.dp_step_label.config(text=f"Step: {self.current_dp_step + 1}/{total_steps + 1}")
                self.dp_prev_btn.config(state=tk.NORMAL if self.current_dp_step > -1 else tk.DISABLED)
                self.dp_next_btn.config(state=tk.NORMAL if self.current_dp_step < total_steps - 1 else tk.DISABLED)
            except Exception as e:
                error_label = ttk.Label(self.dp_frame, text=f"Error displaying DP table: {str(e)}\nTable may be too large to visualize.", wraplength=400)
                error_label.pack(pady=20)

    def update_results(self):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, "KNAPSACK PROBLEM RESULTS\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")

        for algo, data in self.results.items():
            self.results_text.insert(tk.END, f"> {algo} Algorithm\n")
            self.results_text.insert(tk.END, "-" * 40 + "\n")
            self.results_text.insert(tk.END, f"Total Value: {data['value']:.2f}\n")
            self.results_text.insert(tk.END, "Selected Items:\n")
            if data['selected']:
                for item, fraction in data['selected']:
                    if fraction == 1.0:
                        self.results_text.insert(tk.END, f"  > {item.name} (weight: {item.weight}, value: {item.value})\n")
                    else:
                        self.results_text.insert(tk.END, f"  > {item.name} ({fraction:.2f} fraction, weight: {item.weight * fraction:.2f}, value: {item.value * fraction:.2f})\n")
            else:
                self.results_text.insert(tk.END, "  No items selected\n")
            self.results_text.insert(tk.END, "\n")

        # Add comparison
        if len(self.results) > 1:
            self.results_text.insert(tk.END, "COMPARISON\n")
            self.results_text.insert(tk.END, "-" * 40 + "\n")
            for algo, data in self.results.items():
                self.results_text.insert(tk.END, f"{algo}: {data['value']:.2f}\n")
            best = max(self.results.items(), key=lambda x: x[1]['value'])
            self.results_text.insert(tk.END, f"\nBest: {best[0]} with value {best[1]['value']:.2f}\n")

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

        # Reset DP step counter and update visualization
        self.current_dp_step = -1
        self.update_dp_viz()

        # Comparison
        if len(self.results) > 1:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                comp_data = {k: v['value'] for k, v in self.results.items()}
                plot_comparison(comp_data, ax)
                canvas = FigureCanvasTkAgg(fig, master=self.comp_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            except Exception as e:
                error_label = ttk.Label(self.comp_frame, text=f"Error displaying comparison: {str(e)}", wraplength=400)
                error_label.pack(pady=20)

        # Selected Items
        if 'Greedy' in self.results:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                plot_selected_items(self.results['Greedy']['selected'], 'Greedy', ax)
                canvas = FigureCanvasTkAgg(fig, master=self.greedy_viz_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            except Exception as e:
                error_label = ttk.Label(self.greedy_viz_frame, text=f"Error displaying Greedy items: {str(e)}", wraplength=400)
                error_label.pack(pady=20)

        if 'DP' in self.results:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                plot_selected_items(self.results['DP']['selected'], 'DP', ax)
                canvas = FigureCanvasTkAgg(fig, master=self.dp_viz_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            except Exception as e:
                error_label = ttk.Label(self.dp_viz_frame, text=f"Error displaying DP items: {str(e)}", wraplength=400)
                error_label.pack(pady=20)

        if 'Branch & Bound' in self.results:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                plot_selected_items(self.results['Branch & Bound']['selected'], 'Branch & Bound', ax)
                canvas = FigureCanvasTkAgg(fig, master=self.bb_viz_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            except Exception as e:
                error_label = ttk.Label(self.bb_viz_frame, text=f"Error displaying B&B items: {str(e)}", wraplength=400)
                error_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()