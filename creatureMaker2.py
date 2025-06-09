import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import statistics
from typing import Dict, Any, List, Optional

# --- New Imports for Analysis Tab ---
# Matplotlib is required for the new graphing feature.
# You can install it using: pip install matplotlib
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
# ------------------------------------

class CreatureManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Creature JSON Manager")
        self.root.geometry("1100x800") # Increased size for new features
        self.root.configure(bg='#2c3e50')
        
        # Configure modern style
        self.setup_styles()
        
        # Data storage
        self.creatures = []  # List of creature dictionaries
        self.current_creature_index = None
        self.current_file_path = None
        
        # Create the main interface
        self.create_widgets()
        
        # Initialize with empty form
        self.clear_form()
    
    def setup_styles(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background='#2c3e50', borderwidth=0)
        style.configure('TNotebook.Tab', 
                        background='#34495e', 
                        foreground='#ecf0f1', 
                        padding=[10, 5],
                        font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab', 
                  background=[('selected', '#3498db')],
                  foreground=[('selected', 'white')])

        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       background='#2c3e50',
                       foreground='#ecf0f1')
        
        style.configure('Heading.TLabel',
                       font=('Arial', 11, 'bold'),
                       background='#2c3e50',
                       foreground='#3498db')

        style.configure('SubHeading.TLabel',
                       font=('Arial', 12, 'bold'),
                       background='#34495e',
                       foreground='#ecf0f1')
        
        style.configure('Modern.TEntry',
                       fieldbackground='#34495e',
                       foreground='#ecf0f1',
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Modern.TCombobox',
                       fieldbackground='#34495e',
                       foreground='#ecf0f1',
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Action.TButton',
                       background='#3498db',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
        
        style.configure('Success.TButton',
                       background='#27ae60',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
        
        style.configure('Warning.TButton',
                       background='#e74c3c',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
        
        style.configure('Modern.Treeview',
                       background='#34495e',
                       foreground='#ecf0f1',
                       fieldbackground='#34495e',
                       borderwidth=1,
                       relief='solid',
                       rowheight=25)
        
        style.configure('Modern.Treeview.Heading',
                       background='#2c3e50',
                       foreground='#3498db',
                       font=('Arial', 10, 'bold'),
                       relief='raised')

    def create_widgets(self):
        """Create the main interface widgets using tabs"""
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        title_label = ttk.Label(main_frame, text="Creature JSON Manager", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create a Notebook (tabbed interface)
        notebook = ttk.Notebook(main_frame, style='TNotebook')
        notebook.pack(fill='both', expand=True)

        # --- Editor Tab ---
        editor_tab = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(editor_tab, text='Creature Editor')
        self.create_editor_tab(editor_tab)

        # --- Analysis Tab ---
        analysis_tab = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(analysis_tab, text='Stat Analysis')
        self.create_analysis_tab(analysis_tab)
        
        # Bottom - File operations
        self.create_file_operations(main_frame)

    def create_editor_tab(self, parent_tab):
        """Create the content for the creature editor tab"""
        content_frame = tk.Frame(parent_tab, bg='#2c3e50')
        content_frame.pack(fill='both', expand=True, pady=10)
        
        self.create_creature_list(content_frame)
        self.create_creature_editor(content_frame)

    def create_analysis_tab(self, parent_tab):
        """Create the content for the stat analysis tab"""
        analysis_frame = tk.Frame(parent_tab, bg='#34495e', padx=20, pady=20)
        analysis_frame.pack(fill='both', expand=True, pady=10)

        # --- Summary Table ---
        summary_frame = tk.Frame(analysis_frame, bg='#34495e')
        summary_frame.pack(fill='x', pady=(0, 20))
        
        summary_label = ttk.Label(summary_frame, text="Class Statistics Summary", style='SubHeading.TLabel')
        summary_label.pack(anchor='w', pady=(0, 10))
        
        self.summary_tree = ttk.Treeview(summary_frame, style='Modern.Treeview')
        self.summary_tree['columns'] = ('Class', 'Count', 'AvgHP', 'AvgDef', 'AvgAtt', 'MinMaxHP', 'MinMaxDef', 'MinMaxAtt')
        self.summary_tree['show'] = 'headings'
        
        cols = {
            'Class': ('Class', 60), 'Count': ('Count', 60), 
            'AvgHP': ('Avg HP', 80), 'AvgDef': ('Avg Def', 80), 'AvgAtt': ('Avg Att', 80),
            'MinMaxHP': ('HP (Min/Max)', 100), 'MinMaxDef': ('Def (Min/Max)', 100), 'MinMaxAtt': ('Att (Min/Max)', 100)
        }
        for col, (text, width) in cols.items():
            self.summary_tree.heading(col, text=text)
            self.summary_tree.column(col, width=width, anchor='center')
        
        self.summary_tree.pack(fill='x', expand=True)

        # --- Graphing Section ---
        graph_frame = tk.Frame(analysis_frame, bg='#34495e')
        graph_frame.pack(fill='both', expand=True)

        graph_label = ttk.Label(graph_frame, text="Visual Comparison", style='SubHeading.TLabel')
        graph_label.pack(anchor='w', pady=(10, 10))

        if MATPLOTLIB_AVAILABLE:
            self.fig = Figure(figsize=(8, 4), dpi=100, facecolor='#34495e')
            self.ax = self.fig.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(fill='both', expand=True)

            plot_button = ttk.Button(graph_frame, text="Plot Average Stats per Class", 
                                     command=self.plot_avg_stats, style='Action.TButton')
            plot_button.pack(pady=(10, 0))
        else:
            error_label = ttk.Label(graph_frame, 
                                    text="Matplotlib not found. Graphing is disabled.\nPlease run: pip install matplotlib",
                                    background='#34495e', foreground='#e74c3c', font=('Arial', 10, 'italic'))
            error_label.pack(pady=20)

    def create_creature_list(self, parent):
        """Create the creature list panel"""
        list_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        list_header = tk.Frame(list_frame, bg='#34495e')
        list_header.pack(fill='x', padx=20, pady=(15, 10))
        
        list_title = ttk.Label(list_header, text="Creatures List", style='SubHeading.TLabel')
        list_title.pack(side='left')
        
        list_buttons = tk.Frame(list_header, bg='#34495e')
        list_buttons.pack(side='right')
        
        add_btn = ttk.Button(list_buttons, text="Add", command=self.add_creature, style='Success.TButton')
        add_btn.pack(side='left', padx=(0, 5))
        
        remove_btn = ttk.Button(list_buttons, text="Remove", command=self.remove_creature, style='Warning.TButton')
        remove_btn.pack(side='left')
        
        list_container = tk.Frame(list_frame, bg='#34495e')
        list_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.creature_tree = ttk.Treeview(list_container, style='Modern.Treeview', height=15)
        self.creature_tree['columns'] = ('Name', 'Class', 'HP', 'Def', 'Att')
        self.creature_tree['show'] = 'headings'
        
        for col in self.creature_tree['columns']:
            self.creature_tree.heading(col, text=col, command=lambda c=col: self.sort_creature_list(c))
        
        self.creature_tree.column('Name', width=120)
        self.creature_tree.column('Class', width=50, anchor='center')
        self.creature_tree.column('HP', width=50, anchor='center')
        self.creature_tree.column('Def', width=50, anchor='center')
        self.creature_tree.column('Att', width=50, anchor='center')
        
        tree_scroll = ttk.Scrollbar(list_container, orient='vertical', command=self.creature_tree.yview)
        self.creature_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.creature_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        self.creature_tree.bind('<<TreeviewSelect>>', self.on_creature_select)
        self._sort_column = 'Name'
        self._sort_asc = True

    def sort_creature_list(self, col):
        """Sort the creature list when a column header is clicked."""
        if self._sort_column == col:
            self._sort_asc = not self._sort_asc
        else:
            self._sort_asc = True
        self._sort_column = col

        key_map = {
            'Name': 'name', 'Class': 'class', 'HP': 'baseHp',
            'Def': 'baseDef', 'Att': 'baseAttack'
        }
        sort_key = key_map.get(col, 'name')

        self.creatures.sort(key=lambda c: c.get(sort_key, 0) if isinstance(c.get(sort_key), int) else str(c.get(sort_key, "")).lower(), 
                              reverse=not self._sort_asc)
        
        self.refresh_all_views()
    
    def create_creature_editor(self, parent):
        """Create the creature editor panel"""
        editor_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        editor_frame.pack(side='right', fill='both', expand=True)
        
        editor_header = tk.Frame(editor_frame, bg='#34495e')
        editor_header.pack(fill='x', padx=20, pady=(15, 10))
        
        editor_title = ttk.Label(editor_header, text="Creature Editor", style='SubHeading.TLabel')
        editor_title.pack(side='left')
        
        save_changes_btn = ttk.Button(editor_header, text="Save Changes", command=self.save_creature_changes, style='Success.TButton')
        save_changes_btn.pack(side='right')
        
        form_content = tk.Frame(editor_frame, bg='#34495e', padx=30, pady=20)
        form_content.pack(fill='both', expand=True)
        
        name_label = ttk.Label(form_content, text="Creature Name:", style='Heading.TLabel')
        name_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(form_content, textvariable=self.name_var, style='Modern.TEntry', width=25, font=('Arial', 11))
        name_entry.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        
        stats_label = ttk.Label(form_content, text="Base Statistics:", style='Heading.TLabel')
        stats_label.grid(row=2, column=0, columnspan=2, sticky='w', pady=(10, 5))
        
        hp_label = ttk.Label(form_content, text="Base HP:", background='#34495e', foreground='#ecf0f1')
        hp_label.grid(row=3, column=0, sticky='w', padx=(0, 10))
        
        self.hp_var = tk.StringVar()
        hp_entry = ttk.Entry(form_content, textvariable=self.hp_var, style='Modern.TEntry', width=15)
        hp_entry.grid(row=3, column=1, sticky='w', pady=2)
        
        def_label = ttk.Label(form_content, text="Base Defense:", background='#34495e', foreground='#ecf0f1')
        def_label.grid(row=4, column=0, sticky='w', padx=(0, 10))
        
        self.def_var = tk.StringVar()
        def_entry = ttk.Entry(form_content, textvariable=self.def_var, style='Modern.TEntry', width=15)
        def_entry.grid(row=4, column=1, sticky='w', pady=2)
        
        attack_label = ttk.Label(form_content, text="Base Attack:", background='#34495e', foreground='#ecf0f1')
        attack_label.grid(row=5, column=0, sticky='w', padx=(0, 10))
        
        self.attack_var = tk.StringVar()
        attack_entry = ttk.Entry(form_content, textvariable=self.attack_var, style='Modern.TEntry', width=15)
        attack_entry.grid(row=5, column=1, sticky='w', pady=2)
        
        class_label = ttk.Label(form_content, text="Class (1-10):", background='#34495e', foreground='#ecf0f1')
        class_label.grid(row=6, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        
        self.class_var = tk.StringVar()
        class_combo = ttk.Combobox(form_content, textvariable=self.class_var, style='Modern.TCombobox', width=12, state='readonly')
        class_combo['values'] = tuple(str(i) for i in range(1, 11))
        class_combo.grid(row=6, column=1, sticky='w', pady=(10, 0))
        
        form_content.columnconfigure(1, weight=1)
        
        self.status_label = ttk.Label(form_content, text="Select a creature to edit or add a new one", 
                                     background='#34495e', foreground='#95a5a6', font=('Arial', 9, 'italic'))
        self.status_label.grid(row=7, column=0, columnspan=2, pady=(20, 0))
    
    def create_file_operations(self, parent):
        """Create file operation buttons"""
        file_frame = tk.Frame(parent, bg='#2c3e50')
        file_frame.pack(fill='x', pady=(20, 0))
        
        file_buttons = tk.Frame(file_frame, bg='#2c3e50')
        file_buttons.pack(side='left')
        
        new_btn = ttk.Button(file_buttons, text="New Project", command=self.new_project, style='Action.TButton')
        new_btn.pack(side='left', padx=(0, 5))
        
        load_btn = ttk.Button(file_buttons, text="Load JSON", command=self.load_creatures, style='Action.TButton')
        load_btn.pack(side='left', padx=5)
        
        save_btn = ttk.Button(file_buttons, text="Save JSON", command=self.save_creatures, style='Success.TButton')
        save_btn.pack(side='left', padx=5)
        
        save_as_btn = ttk.Button(file_buttons, text="Save As...", command=self.save_creatures_as, style='Success.TButton')
        save_as_btn.pack(side='left', padx=5)
        
        export_btn = ttk.Button(file_buttons, text="Export Selected", command=self.export_selected_creature, style='Action.TButton')
        export_btn.pack(side='left', padx=5)
    
    def refresh_all_views(self):
        """Refresh all data-dependent views."""
        self.refresh_creature_list()
        self.refresh_summary_table()
        # Optionally, auto-update the plot, or let the user do it manually.
        # self.plot_avg_stats()

    def clear_form(self):
        self.name_var.set("")
        self.hp_var.set("")
        self.def_var.set("")
        self.attack_var.set("")
        self.class_var.set("1")
        self.current_creature_index = None
        if self.creature_tree.selection():
            self.creature_tree.selection_remove(self.creature_tree.selection())
        self.update_status("Ready to create new creature")
    
    def update_status(self, message: str):
        self.status_label.config(text=message)
    
    def refresh_creature_list(self):
        for item in self.creature_tree.get_children():
            self.creature_tree.delete(item)
        
        for i, creature in enumerate(self.creatures):
            name = creature.get('name', 'Unnamed')
            class_val = creature.get('class', 1)
            hp = creature.get('baseHp', '-')
            defense = creature.get('baseDef', '-')
            attack = creature.get('baseAttack', '-')
            
            self.creature_tree.insert('', 'end', iid=str(i), values=(name, class_val, hp, defense, attack))
    
    def calculate_class_stats(self):
        """Calculate summary statistics for each class."""
        class_stats = {i: {'creatures': []} for i in range(1, 11)}
        
        for creature in self.creatures:
            class_val = creature.get('class')
            if class_val in class_stats:
                class_stats[class_val]['creatures'].append(creature)
        
        summary_data = []
        for class_val, data in class_stats.items():
            count = len(data['creatures'])
            if count == 0:
                summary_data.append([class_val, 0, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
                continue

            hp_vals = [c.get('baseHp', 0) for c in data['creatures']]
            def_vals = [c.get('baseDef', 0) for c in data['creatures']]
            att_vals = [c.get('baseAttack', 0) for c in data['creatures']]

            summary_data.append([
                class_val,
                count,
                f"{statistics.mean(hp_vals):.1f}",
                f"{statistics.mean(def_vals):.1f}",
                f"{statistics.mean(att_vals):.1f}",
                f"{min(hp_vals)} / {max(hp_vals)}",
                f"{min(def_vals)} / {max(def_vals)}",
                f"{min(att_vals)} / {max(att_vals)}",
            ])
        return summary_data

    def refresh_summary_table(self):
        """Refresh the class statistics summary table."""
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)
        
        summary_data = self.calculate_class_stats()
        for row in summary_data:
            self.summary_tree.insert('', 'end', values=row)

    def plot_avg_stats(self):
        """Plot the average stats per class on the matplotlib canvas."""
        if not MATPLOTLIB_AVAILABLE:
            return

        summary_data = self.calculate_class_stats()
        
        # Filter out classes with no creatures
        plot_data = [row for row in summary_data if row[1] > 0]
        if not plot_data:
            messagebox.showinfo("No Data", "There are no creatures to plot.")
            return

        classes = [row[0] for row in plot_data]
        avg_hp = [float(row[2]) for row in plot_data]
        avg_def = [float(row[3]) for row in plot_data]
        avg_att = [float(row[4]) for row in plot_data]

        self.ax.clear()
        
        x = range(len(classes))
        width = 0.25

        self.ax.bar([i - width for i in x], avg_hp, width, label='Avg HP', color='#2980b9')
        self.ax.bar(x, avg_def, width, label='Avg Def', color='#27ae60')
        self.ax.bar([i + width for i in x], avg_att, width, label='Avg Att', color='#c0392b')

        self.ax.set_ylabel('Stat Value', color='white')
        self.ax.set_title('Average Creature Stats by Class', color='white')
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(classes, color='white')
        self.ax.tick_params(axis='y', colors='white')
        
        self.ax.set_facecolor('#34495e')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        
        legend = self.ax.legend()
        for text in legend.get_texts():
            text.set_color("white")

        self.fig.tight_layout()
        self.canvas.draw()
    
    def add_creature(self):
        if not self.validate_inputs():
            return
        
        creature_data = self.get_creature_data()
        self.creatures.append(creature_data)
        
        self.refresh_all_views()
        self.sort_creature_list(self._sort_column) # re-apply sort
        
        # Find and select the new creature
        for i, item_id in enumerate(self.creature_tree.get_children()):
             if self.creatures[i] == creature_data:
                self.creature_tree.selection_set(item_id)
                self.creature_tree.focus(item_id)
                break
        
        self.update_status(f"Added creature: {creature_data['name']}")
    
    def remove_creature(self):
        selection = self.creature_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a creature to remove.")
            return

        selected_iid = selection[0]
        self.current_creature_index = self.creature_tree.index(selected_iid)
        
        creature_name = self.creatures[self.current_creature_index]['name']
        if messagebox.askyesno("Confirm Removal", f"Remove creature '{creature_name}'?"):
            del self.creatures[self.current_creature_index]
            self.refresh_all_views()
            self.clear_form()
            self.update_status(f"Removed creature: {creature_name}")
    
    def on_creature_select(self, event):
        selection = self.creature_tree.selection()
        if selection:
            index_in_view = self.creature_tree.index(selection[0])
            
            # Find the actual index in self.creatures list based on view
            visible_creatures = [self.creatures[self.creature_tree.index(iid)] for iid in self.creature_tree.get_children()]
            selected_creature_data = visible_creatures[index_in_view]
            
            self.current_creature_index = self.creatures.index(selected_creature_data)
            creature = self.creatures[self.current_creature_index]

            self.load_creature_data(creature)
            self.update_status(f"Editing: {creature.get('name', 'Unnamed')}")
    
    def save_creature_changes(self):
        if self.current_creature_index is None:
            messagebox.showwarning("No Selection", "Select a creature to save changes.")
            return
        
        if not self.validate_inputs():
            return
        
        creature_data = self.get_creature_data()
        self.creatures[self.current_creature_index] = creature_data
        self.refresh_all_views()
        
        # Reselect the updated creature
        self.creature_tree.selection_set(str(self.current_creature_index))
        
        self.update_status(f"Saved changes to: {creature_data['name']}")
    
    def new_project(self):
        if not self.creatures or messagebox.askyesno("New Project", "This will clear all creatures. Continue?"):
            self.creatures.clear()
            self.refresh_all_views()
            self.clear_form()
            self.current_file_path = None
            self.root.title("Creature JSON Manager")
            self.update_status("New project started")
    
    def validate_inputs(self) -> bool:
        if not self.name_var.get().strip():
            messagebox.showerror("Validation Error", "Creature name is required!")
            return False
        
        for var, name in [(self.hp_var, "HP"), (self.def_var, "Defense"), (self.attack_var, "Attack")]:
            try:
                val = int(var.get())
                if val < 0: raise ValueError()
            except ValueError:
                if var.get(): # Allow empty fields
                    messagebox.showerror("Validation Error", f"Base {name} must be a valid non-negative integer!")
                    return False
        
        try:
            class_val = int(self.class_var.get())
            if not 1 <= class_val <= 10: raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Class must be between 1 and 10!")
            return False
        
        return True
    
    def get_creature_data(self) -> Dict[str, Any]:
        data = {
            "name": self.name_var.get().strip(),
            "class": int(self.class_var.get())
        }
        
        if self.hp_var.get(): data["baseHp"] = int(self.hp_var.get())
        if self.def_var.get(): data["baseDef"] = int(self.def_var.get())
        if self.attack_var.get(): data["baseAttack"] = int(self.attack_var.get())
        
        return data
    
    def load_creature_data(self, data: Dict[str, Any]):
        self.name_var.set(data.get("name", ""))
        self.hp_var.set(str(data.get("baseHp", "")))
        self.def_var.set(str(data.get("baseDef", "")))
        self.attack_var.set(str(data.get("baseAttack", "")))
        self.class_var.set(str(data.get("class", 1)))
    
    def load_creatures(self):
        file_path = filedialog.askopenfilename(
            title="Load Creatures JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path: return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.creatures = [data] if isinstance(data, dict) else data
            self.current_file_path = file_path
            self.root.title(f"Creature JSON Manager - {os.path.basename(file_path)}")
            self.refresh_all_views()
            self.clear_form()
            self.update_status(f"Loaded {len(self.creatures)} creatures")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load creatures:\n{str(e)}")
    
    def save_creatures(self):
        if self.current_file_path:
            self._save_to_file(self.current_file_path)
        else:
            self.save_creatures_as()
    
    def save_creatures_as(self):
        if not self.creatures:
            messagebox.showwarning("No Data", "No creatures to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Creatures JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self._save_to_file(file_path)
    
    def _save_to_file(self, file_path: str):
        if not self.creatures:
            messagebox.showwarning("No Data", "No creatures to save!")
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.creatures, f, indent=2)
            
            self.current_file_path = file_path
            self.root.title(f"Creature JSON Manager - {os.path.basename(file_path)}")
            self.update_status(f"Saved {len(self.creatures)} creatures")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save creatures:\n{str(e)}")
    
    def export_selected_creature(self):
        if self.current_creature_index is None:
            messagebox.showwarning("No Selection", "Please select a creature to export.")
            return
        
        creature = self.creatures[self.current_creature_index]
        file_path = filedialog.asksaveasfilename(
            title="Export Creature JSON",
            defaultextension=".json",
            initialfile=f"{creature.get('name', 'creature')}.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(creature, f, indent=2)
                self.update_status(f"Exported: {creature.get('name', 'creature')}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export creature:\n{str(e)}")

def main():
    root = tk.Tk()
    app = CreatureManager(root)
    
    def on_closing():
        if app.creatures and messagebox.askyesno("Quit", "You have unsaved work. Are you sure you want to quit?"):
            root.destroy()
        elif not app.creatures:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()