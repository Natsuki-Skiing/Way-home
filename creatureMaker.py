import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from typing import Dict, Any, List, Optional

class CreatureManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Creature JSON Manager")
        self.root.geometry("1000x700")
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
        
        # Configure colors and styles
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       background='#2c3e50',
                       foreground='#ecf0f1')
        
        style.configure('Heading.TLabel',
                       font=('Arial', 11, 'bold'),
                       background='#2c3e50',
                       foreground='#3498db')
        
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
                       relief='solid')
        
        style.configure('Modern.Treeview.Heading',
                       background='#2c3e50',
                       foreground='#3498db',
                       font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create the main interface widgets"""
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Creature JSON Manager", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Main content frame (horizontal layout)
        content_frame = tk.Frame(main_frame, bg='#2c3e50')
        content_frame.pack(fill='both', expand=True)
        
        # Left side - Creature List
        self.create_creature_list(content_frame)
        
        # Right side - Creature Editor
        self.create_creature_editor(content_frame)
        
        # Bottom - File operations
        self.create_file_operations(main_frame)
    
    def create_creature_list(self, parent):
        """Create the creature list panel"""
        list_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # List header
        list_header = tk.Frame(list_frame, bg='#34495e')
        list_header.pack(fill='x', padx=20, pady=(15, 10))
        
        list_title = ttk.Label(list_header, text="Creatures List", style='Heading.TLabel')
        list_title.pack(side='left')
        
        # List buttons
        list_buttons = tk.Frame(list_header, bg='#34495e')
        list_buttons.pack(side='right')
        
        add_btn = ttk.Button(list_buttons, text="Add", command=self.add_creature, style='Success.TButton')
        add_btn.pack(side='left', padx=(0, 5))
        
        remove_btn = ttk.Button(list_buttons, text="Remove", command=self.remove_creature, style='Warning.TButton')
        remove_btn.pack(side='left')
        
        # Creature listbox with scrollbar
        list_container = tk.Frame(list_frame, bg='#34495e')
        list_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create treeview for better display
        self.creature_tree = ttk.Treeview(list_container, style='Modern.Treeview', height=15)
        self.creature_tree['columns'] = ('Name', 'Class', 'HP', 'Def', 'Att')
        self.creature_tree['show'] = 'headings'
        
        # Configure columns
        self.creature_tree.heading('Name', text='Name')
        self.creature_tree.heading('Class', text='Class')
        self.creature_tree.heading('HP', text='HP')
        self.creature_tree.heading('Def', text='Def')
        self.creature_tree.heading('Att', text='Att')
        
        self.creature_tree.column('Name', width=120)
        self.creature_tree.column('Class', width=50)
        self.creature_tree.column('HP', width=50)
        self.creature_tree.column('Def', width=50)
        self.creature_tree.column('Att', width=50)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(list_container, orient='vertical', command=self.creature_tree.yview)
        self.creature_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.creature_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        # Bind selection event
        self.creature_tree.bind('<<TreeviewSelect>>', self.on_creature_select)
    
    def create_creature_editor(self, parent):
        """Create the creature editor panel"""
        editor_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        editor_frame.pack(side='right', fill='both', expand=True)
        
        # Editor header
        editor_header = tk.Frame(editor_frame, bg='#34495e')
        editor_header.pack(fill='x', padx=20, pady=(15, 10))
        
        editor_title = ttk.Label(editor_header, text="Creature Editor", style='Heading.TLabel')
        editor_title.pack(side='left')
        
        # Save button in header
        save_changes_btn = ttk.Button(editor_header, text="Save Changes", command=self.save_creature_changes, style='Success.TButton')
        save_changes_btn.pack(side='right')
        
        # Form content
        form_content = tk.Frame(editor_frame, bg='#34495e', padx=30, pady=20)
        form_content.pack(fill='both', expand=True)
        
        # Creature Name
        name_label = ttk.Label(form_content, text="Creature Name:", style='Heading.TLabel')
        name_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(form_content, textvariable=self.name_var, style='Modern.TEntry', width=25, font=('Arial', 11))
        name_entry.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        
        # Stats section
        stats_label = ttk.Label(form_content, text="Base Statistics:", style='Heading.TLabel')
        stats_label.grid(row=2, column=0, columnspan=2, sticky='w', pady=(10, 5))
        
        # Base HP
        hp_label = ttk.Label(form_content, text="Base HP:", background='#34495e', foreground='#ecf0f1')
        hp_label.grid(row=3, column=0, sticky='w', padx=(0, 10))
        
        self.hp_var = tk.StringVar()
        hp_entry = ttk.Entry(form_content, textvariable=self.hp_var, style='Modern.TEntry', width=15)
        hp_entry.grid(row=3, column=1, sticky='w', pady=2)
        
        # Base Defense
        def_label = ttk.Label(form_content, text="Base Defense:", background='#34495e', foreground='#ecf0f1')
        def_label.grid(row=4, column=0, sticky='w', padx=(0, 10))
        
        self.def_var = tk.StringVar()
        def_entry = ttk.Entry(form_content, textvariable=self.def_var, style='Modern.TEntry', width=15)
        def_entry.grid(row=4, column=1, sticky='w', pady=2)
        
        # Base Attack
        attack_label = ttk.Label(form_content, text="Base Attack:", background='#34495e', foreground='#ecf0f1')
        attack_label.grid(row=5, column=0, sticky='w', padx=(0, 10))
        
        self.attack_var = tk.StringVar()
        attack_entry = ttk.Entry(form_content, textvariable=self.attack_var, style='Modern.TEntry', width=15)
        attack_entry.grid(row=5, column=1, sticky='w', pady=2)
        
        # Class selection
        class_label = ttk.Label(form_content, text="Class (1-10):", background='#34495e', foreground='#ecf0f1')
        class_label.grid(row=6, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        
        self.class_var = tk.StringVar()
        class_combo = ttk.Combobox(form_content, textvariable=self.class_var, style='Modern.TCombobox', width=12, state='readonly')
        class_combo['values'] = tuple(str(i) for i in range(1, 11))
        class_combo.grid(row=6, column=1, sticky='w', pady=(10, 0))
        
        # Configure grid weights
        form_content.columnconfigure(1, weight=1)
        
        # Status label
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
        
        # Export individual creature
        export_btn = ttk.Button(file_buttons, text="Export Selected", command=self.export_selected_creature, style='Action.TButton')
        export_btn.pack(side='left', padx=5)
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_var.set("")
        self.hp_var.set("")
        self.def_var.set("")
        self.attack_var.set("")
        self.class_var.set("1")
        self.current_creature_index = None
        self.update_status("Ready to create new creature")
    
    def update_status(self, message: str):
        """Update the status label"""
        self.status_label.config(text=message)
    
    def refresh_creature_list(self):
        """Refresh the creature list display"""
        # Clear existing items
        for item in self.creature_tree.get_children():
            self.creature_tree.delete(item)
        
        # Add creatures to the list
        for i, creature in enumerate(self.creatures):
            name = creature.get('name', 'Unnamed')
            class_val = creature.get('class', 1)
            hp = creature.get('baseHp', '-')
            defense = creature.get('baseDef', '-')
            attack = creature.get('baseAttack', '-')
            
            self.creature_tree.insert('', 'end', iid=str(i), values=(name, class_val, hp, defense, attack))
    
    def add_creature(self):
        """Add a new creature to the list"""
        if not self.validate_inputs():
            return
        
        creature_data = self.get_creature_data()
        self.creatures.append(creature_data)
        self.refresh_creature_list()
        
        # Select the newly added creature
        new_index = len(self.creatures) - 1
        self.creature_tree.selection_set(str(new_index))
        self.current_creature_index = new_index
        
        self.update_status(f"Added creature: {creature_data['name']}")
    
    def remove_creature(self):
        """Remove selected creature from the list"""
        if self.current_creature_index is None:
            messagebox.showwarning("No Selection", "Please select a creature to remove.")
            return
        
        creature_name = self.creatures[self.current_creature_index]['name']
        if messagebox.askyesno("Confirm Removal", f"Remove creature '{creature_name}'?"):
            del self.creatures[self.current_creature_index]
            self.refresh_creature_list()
            self.clear_form()
            self.update_status(f"Removed creature: {creature_name}")
    
    def on_creature_select(self, event):
        """Handle creature selection from the list"""
        selection = self.creature_tree.selection()
        if selection:
            index = int(selection[0])
            self.current_creature_index = index
            creature = self.creatures[index]
            self.load_creature_data(creature)
            self.update_status(f"Editing: {creature.get('name', 'Unnamed')}")
    
    def save_creature_changes(self):
        """Save changes to the currently selected creature"""
        if self.current_creature_index is None:
            messagebox.showwarning("No Selection", "Please select a creature to save changes to.")
            return
        
        if not self.validate_inputs():
            return
        
        creature_data = self.get_creature_data()
        self.creatures[self.current_creature_index] = creature_data
        self.refresh_creature_list()
        
        # Reselect the updated creature
        self.creature_tree.selection_set(str(self.current_creature_index))
        
        self.update_status(f"Saved changes to: {creature_data['name']}")
    
    def new_project(self):
        """Start a new project (clear all creatures)"""
        if self.creatures and messagebox.askyesno("New Project", "This will clear all creatures. Continue?"):
            self.creatures.clear()
            self.refresh_creature_list()
            self.clear_form()
            self.current_file_path = None
            self.root.title("Creature JSON Manager")
            self.update_status("New project started")
    
    def validate_inputs(self) -> bool:
        """Validate all input fields"""
        if not self.name_var.get().strip():
            messagebox.showerror("Validation Error", "Creature name is required!")
            return False
        
        try:
            hp = int(self.hp_var.get()) if self.hp_var.get() else None
            if hp is not None and hp < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Base HP must be a valid non-negative integer!")
            return False
        
        try:
            defense = int(self.def_var.get()) if self.def_var.get() else None
            if defense is not None and defense < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Base Defense must be a valid non-negative integer!")
            return False
        
        try:
            attack = int(self.attack_var.get()) if self.attack_var.get() else None
            if attack is not None and attack < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Base Attack must be a valid non-negative integer!")
            return False
        
        try:
            class_val = int(self.class_var.get())
            if not 1 <= class_val <= 10:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Class must be between 1 and 10!")
            return False
        
        return True
    
    def get_creature_data(self) -> Dict[str, Any]:
        """Get current creature data as dictionary"""
        data = {
            "name": self.name_var.get().strip(),
            "class": int(self.class_var.get())
        }
        
        # Add optional fields only if they have values
        if self.hp_var.get():
            data["baseHp"] = int(self.hp_var.get())
        if self.def_var.get():
            data["baseDef"] = int(self.def_var.get())
        if self.attack_var.get():
            data["baseAttack"] = int(self.attack_var.get())
        
        return data
    
    def load_creature_data(self, data: Dict[str, Any]):
        """Load creature data into form"""
        self.name_var.set(data.get("name", ""))
        self.hp_var.set(str(data.get("baseHp", "")))
        self.def_var.set(str(data.get("baseDef", "")))
        self.attack_var.set(str(data.get("baseAttack", "")))
        self.class_var.set(str(data.get("class", 1)))
    
    def load_creatures(self):
        """Load creatures from JSON file"""
        file_path = filedialog.askopenfilename(
            title="Load Creatures JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Handle both single creature and array of creatures
                if isinstance(data, dict):
                    self.creatures = [data]
                elif isinstance(data, list):
                    self.creatures = data
                else:
                    raise ValueError("Invalid JSON format")
                
                self.refresh_creature_list()
                self.current_file_path = file_path
                self.root.title(f"Creature JSON Manager - {os.path.basename(file_path)}")
                self.clear_form()
                self.update_status(f"Loaded {len(self.creatures)} creatures")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load creatures:\n{str(e)}")
    
    def save_creatures(self):
        """Save creatures to current file or prompt for new file"""
        if self.current_file_path:
            self._save_to_file(self.current_file_path)
        else:
            self.save_creatures_as()
    
    def save_creatures_as(self):
        """Save creatures to a new file"""
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
        """Save creatures data to specified file"""
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
        """Export the currently selected creature as individual JSON"""
        if self.current_creature_index is None:
            messagebox.showwarning("No Selection", "Please select a creature to export.")
            return
        
        creature = self.creatures[self.current_creature_index]
        file_path = filedialog.asksaveasfilename(
            title="Export Creature JSON",
            defaultextension=".json",
            initialvalue=f"{creature.get('name', 'creature')}.json",
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
    
    # Handle window closing
    def on_closing():
        if app.creatures and messagebox.askyesno("Quit", "Are you sure you want to quit? Make sure to save your work!"):
            root.destroy()
        elif not app.creatures:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()