import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from DBOps import DataBaseManager
import pandas as pd
from datetime import datetime

class DatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sunway Database Manager")
        self.root.geometry("1400x800")
        
        # Initialize database
        self.db = DataBaseManager("data/storage copy.db")
        
        # Style configuration
        self.setup_styles()
        
        # Build UI
        self.setup_ui()
        
        # Load tables initially
        self.load_tables()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Browse Data
        self.browse_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.browse_tab, text='Browse Data')
        self.setup_browse_tab()
        
        # Tab 2: SQL Query
        self.query_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.query_tab, text='SQL Query')
        self.setup_query_tab()
        
        # Tab 3: Add/Edit Data
        self.edit_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.edit_tab, text='Edit Data')
        self.setup_edit_tab()
        
        # Tab 4: Table Management
        self.table_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.table_tab, text='Manage Tables')
        self.setup_table_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status("Ready")
        
    def setup_browse_tab(self):
        left_frame = ttk.LabelFrame(self.browse_tab, text="Tables", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.table_listbox = tk.Listbox(left_frame, width=25, height=20)
        self.table_listbox.pack(fill=tk.BOTH, expand=True)
        self.table_listbox.bind('<<ListboxSelect>>', self.on_table_select)
        
        ttk.Button(left_frame, text="Refresh Tables", 
                  command=self.load_tables).pack(pady=(10, 0))
        
        right_frame = ttk.Frame(self.browse_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Button(search_frame, text="Clear", 
                  command=self.clear_search).pack(side=tk.LEFT, padx=(5, 0))
        
        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.data_tree = ttk.Treeview(tree_frame, yscrollcommand=vsb.set, 
                                     xscrollcommand=hsb.set)
        
        vsb.config(command=self.data_tree.yview)
        hsb.config(command=self.data_tree.xview)
        
        self.data_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        export_frame = ttk.Frame(right_frame)
        export_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(export_frame, text="Export to CSV", 
                  command=self.export_to_csv).pack(side=tk.LEFT)
        ttk.Button(export_frame, text="Export to Excel", 
                  command=self.export_to_excel).pack(side=tk.LEFT, padx=(5, 0))
        
    def setup_query_tab(self):
        top_frame = ttk.Frame(self.query_tab)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(top_frame, text="SQL Query:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        
        self.query_text = scrolledtext.ScrolledText(top_frame, height=8, 
                                                   font=('Consolas', 10))
        self.query_text.pack(fill=tk.X)
        
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(btn_frame, text="Execute", 
                  command=self.execute_custom_query).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Clear", 
                  command=lambda: self.query_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(btn_frame, text="Format", 
                  command=self.format_query).pack(side=tk.LEFT, padx=(5, 0))
        
        quick_frame = ttk.LabelFrame(top_frame, text="Quick Queries", padding="10")
        quick_frame.pack(fill=tk.X, pady=(10, 0))
        
        quick_queries = [
            ("Show all tables", "SELECT name FROM sqlite_master WHERE type='table'"),
            ("Show table schema", "SELECT sql FROM sqlite_master WHERE sql IS NOT NULL"),
            ("Count all rows", "SELECT 'Total rows: ' || COUNT(*) FROM {}")
        ]
        
        for text, query in quick_queries:
            ttk.Button(quick_frame, text=text, 
                      command=lambda q=query: self.insert_query(q)).pack(side=tk.LEFT, padx=(0, 5))
        
        results_frame = ttk.LabelFrame(self.query_tab, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(results_frame, height=15,
                                                    font=('Consolas', 9))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_edit_tab(self):
        main_frame = ttk.Frame(self.edit_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(selection_frame, text="Select Table:", 
                 font=('Arial', 11)).pack(side=tk.LEFT)
        
        self.edit_table_var = tk.StringVar()
        self.edit_table_combo = ttk.Combobox(selection_frame, 
                                           textvariable=self.edit_table_var,
                                           width=30, state='readonly')
        self.edit_table_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.edit_table_combo.bind('<<ComboboxSelected>>', self.on_edit_table_select)
        
        self.form_frame = ttk.LabelFrame(main_frame, text="Record Details", padding="20")
        self.form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.form_frame, text="Select a table to edit records").pack()
        
    def setup_table_tab(self):
        left_frame = ttk.LabelFrame(self.table_tab, text="Create New Table", padding="20")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Table Name:").pack(anchor=tk.W)
        self.new_table_name = ttk.Entry(left_frame)
        self.new_table_name.pack(fill=tk.X, pady=(0, 10))
        
        columns_frame = ttk.LabelFrame(left_frame, text="Columns", padding="10")
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        self.column_entries = []
        self.add_column_entry(columns_frame)
        
        ttk.Button(columns_frame, text="Add Column", 
                  command=lambda: self.add_column_entry(columns_frame)).pack(pady=(10, 0))
        
        ttk.Button(left_frame, text="Create Table", 
                  command=self.create_new_table).pack(pady=(20, 0))
        
        right_frame = ttk.LabelFrame(self.table_tab, text="Existing Tables", padding="20")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.existing_tables_tree = ttk.Treeview(right_frame, columns=('name', 'columns'))
        self.existing_tables_tree.heading('#0', text='')
        self.existing_tables_tree.heading('name', text='Table Name')
        self.existing_tables_tree.heading('columns', text='Columns')
        
        vsb = ttk.Scrollbar(right_frame, orient="vertical", 
                           command=self.existing_tables_tree.yview)
        self.existing_tables_tree.configure(yscrollcommand=vsb.set)
        
        self.existing_tables_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(right_frame, text="Delete Selected Table", 
                  command=self.delete_table).pack(pady=(10, 0))
        
    def add_column_entry(self, parent_frame):
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=tk.X, pady=(0, 5))
        
        name_entry = ttk.Entry(frame, width=20)
        name_entry.pack(side=tk.LEFT, padx=(0, 5))
        name_entry.insert(0, f"column_{len(self.column_entries) + 1}")
        
        type_combo = ttk.Combobox(frame, values=['INTEGER', 'TEXT', 'REAL', 'BLOB'], 
                                 width=15, state='readonly')
        type_combo.pack(side=tk.LEFT, padx=(0, 5))
        type_combo.set('TEXT')
        
        constraints_entry = ttk.Entry(frame, width=20)
        constraints_entry.pack(side=tk.LEFT, padx=(0, 5))
        constraints_entry.insert(0, "")
        
        ttk.Button(frame, text="X", width=3, 
                  command=lambda f=frame: self.remove_column_entry(f)).pack(side=tk.LEFT)
        
        self.column_entries.append((name_entry, type_combo, constraints_entry))
    
    def remove_column_entry(self, frame):
        for i, (name_entry, type_combo, const_entry) in enumerate(self.column_entries):
            if name_entry.master == frame:
                self.column_entries.pop(i)
                frame.destroy()
                break
    
    def load_tables(self):
        try:
            tables = self.db.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
            table_names = [table[0] for table in tables]
            
            self.table_listbox.delete(0, tk.END)
            for name in table_names:
                self.table_listbox.insert(tk.END, name)
            
            self.edit_table_combo['values'] = table_names
            
            self.existing_tables_tree.delete(*self.existing_tables_tree.get_children())
            for table in table_names:
                columns = self.db.execute_query(f"PRAGMA table_info({table})")
                columns_str = ", ".join([col[1] for col in columns])
                self.existing_tables_tree.insert('', 'end', values=(table, columns_str))
            
            self.update_status(f"Loaded {len(table_names)} tables")
            
        except Exception as e:
            self.update_status(f"Error loading tables: {str(e)}", error=True)
    
    def on_table_select(self, event):
        selection = self.table_listbox.curselection()
        if selection:
            table_name = self.table_listbox.get(selection[0])
            self.display_table_data(table_name)
    
    def display_table_data(self, table_name):
        try:
            for col in self.data_tree['columns']:
                self.data_tree.heading(col, text='')
                self.data_tree.column(col, width=0)
            
            self.data_tree['columns'] = []
            
            columns = self.db.execute_query(f"PRAGMA table_info({table_name})")
            column_names = [col[1] for col in columns]
            
            self.data_tree['columns'] = column_names
            for col in column_names:
                self.data_tree.heading(col, text=col)
                self.data_tree.column(col, width=100, minwidth=50)
            
            data = self.db.get_data(table_name)
            
            self.data_tree.delete(*self.data_tree.get_children())
            
            for row in data:
                self.data_tree.insert('', 'end', values=row)
            
            self.update_status(f"Displaying {len(data)} rows from '{table_name}'")
            
        except Exception as e:
            self.update_status(f"Error displaying table: {str(e)}", error=True)
    
    def on_search(self, event=None):
        search_term = self.search_var.get().lower()
        if not search_term:
            return
        
        for item in self.data_tree.get_children():
            values = self.data_tree.item(item)['values']
            if any(search_term in str(value).lower() for value in values):
                self.data_tree.selection_set(item)
                self.data_tree.see(item)
                break
    
    def clear_search(self):
        self.search_var.set("")
        self.data_tree.selection_remove(self.data_tree.selection())
    
    def export_to_csv(self):
        try:
            selection = self.table_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a table first")
                return
            
            table_name = self.table_listbox.get(selection[0])
            data = self.db.get_data(table_name)
            
            columns = self.db.execute_query(f"PRAGMA table_info({table_name})")
            column_names = [col[1] for col in columns]
            
            df = pd.DataFrame(data, columns=column_names)
            
            filename = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            
            self.update_status(f"Exported to {filename}")
            messagebox.showinfo("Success", f"Data exported to {filename}")
            
        except Exception as e:
            self.update_status(f"Export error: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_to_excel(self):
        try:
            selection = self.table_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a table first")
                return
            
            table_name = self.table_listbox.get(selection[0])
            data = self.db.get_data(table_name)
            
            columns = self.db.execute_query(f"PRAGMA table_info({table_name})")
            column_names = [col[1] for col in columns]
            
            df = pd.DataFrame(data, columns=column_names)
            
            filename = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(filename, index=False)
            
            self.update_status(f"Exported to {filename}")
            messagebox.showinfo("Success", f"Data exported to {filename}")
            
        except Exception as e:
            self.update_status(f"Export error: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def execute_custom_query(self):
        query = self.query_text.get(1.0, tk.END).strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a SQL query")
            return
        
        try:
            result = self.db.execute_query(query)
            
            self.result_text.delete(1.0, tk.END)
            
            if result:
                if isinstance(result[0], tuple):
                    try:
                        cols = self.db.cursor.description
                        if cols:
                            column_names = [col[0] for col in cols]
                            header = "\t".join(column_names)
                            self.result_text.insert(tk.END, header + "\n")
                            self.result_text.insert(tk.END, "-" * len(header) + "\n")
                    except:
                        pass
                
                for row in result:
                    if isinstance(row, tuple):
                        row_str = "\t".join(str(val) for val in row)
                    else:
                        row_str = str(row)
                    self.result_text.insert(tk.END, row_str + "\n")
            else:
                self.result_text.insert(tk.END, "Query executed successfully (no rows returned)")
            
            self.update_status(f"Query executed successfully")
            
        except Exception as e:
            error_msg = f"Query Error: {str(e)}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, error_msg)
            self.update_status(error_msg, error=True)
    
    def format_query(self):
        query = self.query_text.get(1.0, tk.END)
        keywords = ['SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'UPDATE', 
                   'SET', 'DELETE', 'CREATE', 'TABLE', 'DROP', 'ALTER',
                   'AND', 'OR', 'NOT', 'NULL', 'ORDER', 'BY', 'GROUP',
                   'HAVING', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER']
        
        formatted = query.upper()
        for kw in keywords:
            formatted = formatted.replace(kw + ' ', f'\n    {kw} ')
            formatted = formatted.replace(' ' + kw + ' ', f' {kw} ')
        
        self.query_text.delete(1.0, tk.END)
        self.query_text.insert(1.0, formatted.strip())
    
    def insert_query(self, query_template):
        selection = self.table_listbox.curselection()
        if selection and '{}' in query_template:
            table_name = self.table_listbox.get(selection[0])
            query = query_template.format(table_name)
            self.query_text.delete(1.0, tk.END)
            self.query_text.insert(1.0, query)
        else:
            self.query_text.delete(1.0, tk.END)
            self.query_text.insert(1.0, query_template)
    
    def on_edit_table_select(self, event):
        table_name = self.edit_table_var.get()
        if not table_name:
            return
        
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        columns = self.db.execute_query(f"PRAGMA table_info({table_name})")
        
        self.edit_entries = {}
        row = 0
        
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            
            ttk.Label(self.form_frame, text=f"{col_name} ({col_type}):").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=5)
            
            if col_type.upper() in ['TEXT', 'VARCHAR']:
                entry = ttk.Entry(self.form_frame, width=30)
                if default_val:
                    entry.insert(0, default_val)
            elif col_type.upper() in ['INTEGER', 'INT']:
                entry = ttk.Spinbox(self.form_frame, from_=-2147483648, 
                                   to=2147483647, width=27)
            elif col_type.upper() in ['REAL', 'FLOAT']:
                entry = ttk.Entry(self.form_frame, width=30)
            elif col_type.upper() in ['DATE', 'DATETIME']:
                entry = ttk.Entry(self.form_frame, width=30)
                entry.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                entry = ttk.Entry(self.form_frame, width=30)
            
            entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
            self.edit_entries[col_name] = entry
            
            row += 1
        
        btn_frame = ttk.Frame(self.form_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Insert Record", 
                  command=lambda: self.insert_record(table_name)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Record", 
                  command=lambda: self.update_record(table_name)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Record", 
                  command=lambda: self.delete_record(table_name)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", 
                  command=self.clear_edit_form).pack(side=tk.LEFT, padx=5)
    
    def insert_record(self, table_name):
        try:
            data = {}
            for col_name, entry in self.edit_entries.items():
                value = entry.get()
                if value:
                    data[col_name] = value
            
            if data:
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['?' for _ in data])
                values = tuple(data.values())
                
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                self.db.execute_query(query, values)
                
                self.update_status(f"Record inserted into {table_name}")
                messagebox.showinfo("Success", "Record inserted successfully")
                self.clear_edit_form()
                
                self.display_table_data(table_name)
                
        except Exception as e:
            self.update_status(f"Insert error: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to insert record: {str(e)}")
    
    def update_record(self, table_name):
        try:
            condition = simpledialog.askstring("Update Condition", 
                                              f"Enter WHERE condition for {table_name}:\nExample: id = 1")
            if not condition:
                return
            
            updates = {}
            for col_name, entry in self.edit_entries.items():
                value = entry.get()
                if value:
                    updates[col_name] = value
            
            if updates:
                self.db.update_data(table_name, updates, condition)
                self.update_status(f"Record updated in {table_name}")
                messagebox.showinfo("Success", "Record updated successfully")
                self.clear_edit_form()
                
                self.display_table_data(table_name)
                
        except Exception as e:
            self.update_status(f"Update error: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to update record: {str(e)}")
    
    def delete_record(self, table_name):
        try:
            condition = simpledialog.askstring("Delete Condition", 
                                              f"Enter WHERE condition for {table_name}:\nExample: id = 1")
            if not condition:
                return
            
            if messagebox.askyesno("Confirm Delete", 
                                  f"Delete records from {table_name} WHERE {condition}?"):
                self.db.delete_data(table_name, condition)
                self.update_status(f"Records deleted from {table_name}")
                messagebox.showinfo("Success", "Records deleted successfully")
                
                self.display_table_data(table_name)
                
        except Exception as e:
            self.update_status(f"Delete error: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to delete records: {str(e)}")
    
    def clear_edit_form(self):
        for entry in self.edit_entries.values():
            entry.delete(0, tk.END)
    
    def create_new_table(self):
        table_name = self.new_table_name.get().strip()
        if not table_name:
            messagebox.showwarning("Warning", "Please enter a table name")
            return
        
        if not self.column_entries:
            messagebox.showwarning("Warning", "Please add at least one column")
            return
        
        try:
            columns = {}
            for name_entry, type_combo, const_entry in self.column_entries:
                col_name = name_entry.get().strip()
                col_type = type_combo.get()
                constraints = const_entry.get().strip()
                
                if col_name:
                    col_def = f"{col_type}"
                    if constraints:
                        col_def += f" {constraints}"
                    columns[col_name] = col_def
            
            self.db.create_table(table_name, columns)
            
            self.update_status(f"Table '{table_name}' created successfully")
            messagebox.showinfo("Success", f"Table '{table_name}' created")
            
            self.new_table_name.delete(0, tk.END)
            for frame in self.column_entries[0][0].master.master.winfo_children():
                if isinstance(frame, ttk.Frame):
                    frame.destroy()
            self.column_entries.clear()
            self.add_column_entry(self.column_entries[0][0].master.master if self.column_entries else None)
            
            self.load_tables()
            
        except Exception as e:
            self.update_status(f"Create table error: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to create table: {str(e)}")
    
    def delete_table(self):
        selection = self.existing_tables_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a table to delete")
            return
        
        table_name = self.existing_tables_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete table '{table_name}'? \n\nThis action cannot be undone!"):
            try:
                self.db.execute_query(f"DROP TABLE {table_name}")
                self.update_status(f"Table '{table_name}' deleted")
                messagebox.showinfo("Success", f"Table '{table_name}' deleted")
                self.load_tables()
                
            except Exception as e:
                self.update_status(f"Delete error: {str(e)}", error=True)
                messagebox.showerror("Error", f"Failed to delete table: {str(e)}")
    
    def update_status(self, message, error=False):
        self.status_var.set(message)
        if error:
            self.status_bar.configure(foreground='red')
        else:
            self.status_bar.configure(foreground='black')
    
    def on_closing(self):
        self.db.close()
        self.root.destroy()
