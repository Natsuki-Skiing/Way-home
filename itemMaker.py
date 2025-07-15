import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# --- Item class definitions ---
class Item:
    def __init__(self, name: str, class_level: int, value: int, description: str):
        self.name = name
        self.class_level = class_level  # renamed from level to class
        self.value = value
        self.description = description

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__dict__}

class Armour(Item):
    def __init__(self, name: str, class_level: int, protection: int, value: int, description: str):
        super().__init__(name, class_level, value, description)
        self.protection = protection

class Fish(Item):
    def __init__(self, name: str, class_level: int, value: int, description: str, hp: int, dayRot: int):
        super().__init__(name, class_level, value, description)
        self.hp = hp
        self.dayTillRot = dayRot

class Food(Fish):
    def __init__(self, name: str, class_level: int, value: int, description: str, hp: int, dayRot: int):
        super().__init__(name, class_level, value, description, hp, dayRot)

class Helmet(Armour):
    def __init__(self, name: str, class_level: int, protection: int, value: int, description: str):
        super().__init__(name, class_level, protection, value, description)

class Weapon(Item):
    def __init__(self, name: str, class_level: int, damage: int, maxCondition: int, value: int, description: str):
        super().__init__(name, class_level, value, description)
        self.damage = damage
        self.maxCondition = maxCondition
        self.condition = self.maxCondition

class Book(Item):
    def __init__(self, name: str, class_level: int, value: int, description: str):
        super().__init__(name, class_level, value, description)
        self.path = f"books/{name}.txt"
        self.page = 0

class FishingRod(Item):
    def __init__(self, name: str, class_level: int, value: int, description: str, distMod: float, maxCondition: int):
        super().__init__(name, class_level, value, description)
        self.distMod = distMod
        self.maxCon = maxCondition
        self.condition = self.maxCon
    
class Potion(Item):
    def __init__(self, name: str, class_level: int = 1, value: int = 0, description: str = ""):
        super().__init__(name, class_level, value, description)

# Mapping for type names to classes and their fields (including base class)
# This dictionary is the central point for defining new item types.
# To add a new item type:
# 1. Define the class for the new item (e.g., class NewItem(Item): ...).
# 2. Add an entry to type_map with the item's name, its class, and a list of its fields.
#    Make sure to include all fields required by its constructor, including inherited ones.
type_map = {
    'Armour': (Armour, ['name', 'class', 'protection', 'value', 'description']),
    'Helmet': (Helmet, ['name', 'class', 'protection', 'value', 'description']),
    'Weapon': (Weapon, ['name', 'class', 'damage', 'maxCondition', 'value', 'description']),
    'Fish': (Fish, ['name', 'class', 'value', 'description', 'hp', 'dayTillRot']),
    'Food': (Food, ['name', 'class', 'value', 'description', 'hp', 'dayTillRot']), # Added Food class
    'Book': (Book, ['name', 'class', 'value', 'description']),
    'FishingRod': (FishingRod, ['name', 'class', 'value', 'description', 'distMod', 'maxCondition']), # Updated FishingRod fields
    'Potion': (Potion, ['name', 'class', 'value', 'description']),
}

class ItemEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Item JSON Editor")
        self.geometry("900x600")
        self.items = []
        self.current_file = None
        self.selected_index = None
        self.create_widgets()

    def create_widgets(self):
        # File controls
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=5)
        ttk.Button(toolbar, text="Open JSON", command=self.open_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Save JSON", command=self.save_file).pack(side=tk.LEFT)

        # Item list
        self.listbox = tk.Listbox(self)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        # Detail pane
        detail_frame = ttk.Frame(self)
        detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Type dropdown
        ttk.Label(detail_frame, text="Item Type:").grid(row=0, column=0, sticky=tk.W)
        self.type_var = tk.StringVar()
        self.type_menu = ttk.Combobox(
            detail_frame,
            textvariable=self.type_var,
            values=list(type_map.keys()),
            state='readonly'
        )
        self.type_menu.grid(row=0, column=1, sticky=tk.W)
        self.type_menu.bind('<<ComboboxSelected>>', lambda e: self.build_fields())

        self.fields_frame = ttk.Frame(detail_frame)
        self.fields_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        detail_frame.rowconfigure(1, weight=1)
        detail_frame.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ttk.Frame(detail_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="New", command=self.new_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save_item).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=5)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files","*.json")])
        if not path:
            return
        try:
            with open(path, 'r') as f:
                text = f.read().strip()
                if not text:
                    raise json.JSONDecodeError("Empty file", text, 0)
                data = json.loads(text)
                if not isinstance(data, list):
                    messagebox.showwarning(
                        "Unexpected Format",
                        "JSON did not contain a list; starting with empty list."
                    )
                    data = []
        except (json.JSONDecodeError, ValueError):
            data = []
        self.items = data
        self.current_file = path
        self.refresh_list()

    def save_file(self):
        if not self.current_file:
            path = filedialog.asksaveasfilename(
                defaultextension='.json',
                filetypes=[("JSON files","*.json")]
            )
            if not path:
                return
            self.current_file = path
        with open(self.current_file, 'w') as f:
            json.dump(self.items, f, indent=2)
        messagebox.showinfo("Saved","Items JSON saved.")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for idx, item in enumerate(self.items):
            class_level = item.get('class', item.get('level', 1))  # backward compatibility
            self.listbox.insert(
                tk.END,
                f"{idx}: {item.get('name')} (Class {class_level}) - {item.get('type')}"
            )

    def build_fields(self, item_data=None):
        # clear existing inputs
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        t = self.type_var.get()
        if not t:
            return

        cls, fields = type_map[t]
        self.field_vars = {}
        self.text_widgets = {}
        self.spinbox_widgets = {}

        for i, field in enumerate(fields):
            ttk.Label(self.fields_frame, text=f"{field}:").grid(row=i, column=0, sticky=tk.NW, pady=2)
            
            if field == 'description':
                text = tk.Text(self.fields_frame, height=4, wrap=tk.WORD)
                text.grid(row=i, column=1, sticky=tk.EW, pady=2)
                if item_data and 'description' in item_data:
                    text.insert('1.0', item_data['description'])
                self.text_widgets['description'] = text
            elif field == 'class':
                # Special spinbox for class (1-10 range)
                spinbox = tk.Spinbox(self.fields_frame, from_=1, to=10, width=5)
                spinbox.grid(row=i, column=1, sticky=tk.W, pady=2)
                if item_data:
                    # Check for both 'class' and 'level' for backward compatibility
                    class_val = item_data.get('class', item_data.get('level', 1))
                    spinbox.delete(0, tk.END)
                    spinbox.insert(0, str(class_val))
                else:
                    spinbox.delete(0, tk.END)
                    spinbox.insert(0, "1")
                self.spinbox_widgets['class'] = spinbox
            else:
                var = tk.StringVar()
                entry = ttk.Entry(self.fields_frame, textvariable=var)
                entry.grid(row=i, column=1, sticky=tk.EW, pady=2)
                if item_data and field in item_data:
                    var.set(str(item_data[field]))
                self.field_vars[field] = var

        # let entries expand
        for col in range(2):
            self.fields_frame.columnconfigure(col, weight=1)

    def on_select(self, event):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        item_data = self.items[idx]
        self.type_var.set(item_data['type'])
        self.build_fields(item_data)
        self.selected_index = idx

    def new_item(self):
        self.selected_index = None
        self.type_var.set('')
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

    def save_item(self):
        t = self.type_var.get()
        if not t:
            messagebox.showerror("Error","Select an item type.")
            return

        data = {'type': t}
        
        # Handle class field separately
        if 'class' in self.spinbox_widgets:
            try:
                class_val = int(self.spinbox_widgets['class'].get())
                if class_val < 1 or class_val > 10:
                    messagebox.showerror("Error", "Class must be between 1 and 10.")
                    return
                data['class'] = class_val
            except ValueError:
                messagebox.showerror("Error", "Class must be a valid integer between 1 and 10.")
                return
        
        # gather other field values
        for field, var in self.field_vars.items():
            val = var.get()
            # Special handling for numerical fields
            if field in ['value', 'protection', 'damage', 'maxCondition', 'hp', 'dayTillRot', 'distMod', 'maxCon']:
                try:
                    if field == 'distMod':
                        val = float(val)
                    else:
                        val = int(val)
                except ValueError:
                    messagebox.showerror("Error", f"{field} must be a valid number.")
                    return
            data[field] = val

        # description separately
        desc_widget = self.text_widgets.get('description')
        if desc_widget:
            desc = desc_widget.get('1.0', tk.END).strip()
            data['description'] = desc

        if self.selected_index is None:
            self.items.append(data)
        else:
            self.items[self.selected_index] = data

        self.refresh_list()

    def delete_item(self):
        if self.selected_index is not None:
            del self.items[self.selected_index]
            self.selected_index = None
            self.refresh_list()

if __name__ == '__main__':
    app = ItemEditorApp()
    app.mainloop()