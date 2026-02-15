import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app import Bill, db

class BillCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Sunway Solar - Create Bill")
        self.root.geometry("1100x750")
        self.root.configure(bg='#f5f5f5')
        
        # Store bill items
        self.bill_items = []
        
        # Colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
        
        # Setup UI
        self.setup_ui()
        
        # Load products
        self.load_products()
        
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#f5f5f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, 
                text="☀️ SUNWAY SOLAR INVOICE CREATOR", 
                font=('Arial', 20, 'bold'),
                fg='white',
                bg=self.colors['primary']).pack(pady=15)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg='#f5f5f5')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Customer & Product Selection
        left_panel = tk.Frame(content_frame, bg='white', relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Customer Information
        customer_frame = tk.LabelFrame(left_panel, 
                                      text=" CUSTOMER INFORMATION ", 
                                      font=('Arial', 11, 'bold'),
                                      bg='white',
                                      fg=self.colors['primary'],
                                      padx=15,
                                      pady=15)
        customer_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        tk.Label(customer_frame, 
                text="Customer Name:", 
                font=('Arial', 10, 'bold'),
                bg='white').grid(row=0, column=0, sticky=tk.W, pady=8)
        
        self.customer_name = ttk.Entry(customer_frame, width=40, font=('Arial', 10))
        self.customer_name.grid(row=0, column=1, pady=8, padx=(10, 0))
        
        tk.Label(customer_frame, 
                text="Bill Date:", 
                font=('Arial', 10, 'bold'),
                bg='white').grid(row=1, column=0, sticky=tk.W, pady=8)
        
        self.bill_date = ttk.Entry(customer_frame, width=40, font=('Arial', 10))
        self.bill_date.grid(row=1, column=1, pady=8, padx=(10, 0))
        self.bill_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Product Selection
        product_frame = tk.LabelFrame(left_panel, 
                                     text=" ADD PRODUCTS ", 
                                     font=('Arial', 11, 'bold'),
                                     bg='white',
                                     fg=self.colors['primary'],
                                     padx=15,
                                     pady=15)
        product_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Product Type
        tk.Label(product_frame, 
                text="Product Type:", 
                font=('Arial', 10, 'bold'),
                bg='white').grid(row=0, column=0, sticky=tk.W, pady=8)
        
        self.product_type = ttk.Combobox(product_frame, 
                                        values=['Solar Panel', 'Battery', 'Inverter'],
                                        state='readonly',
                                        width=25,
                                        font=('Arial', 10))
        self.product_type.grid(row=0, column=1, pady=8, padx=(10, 0))
        self.product_type.bind('<<ComboboxSelected>>', self.on_product_type_change)
        
        # Product Name
        tk.Label(product_frame, 
                text="Product Name:", 
                font=('Arial', 10, 'bold'),
                bg='white').grid(row=1, column=0, sticky=tk.W, pady=8)
        
        self.product_name = ttk.Combobox(product_frame, 
                                        state='readonly',
                                        width=25,
                                        font=('Arial', 10))
        self.product_name.grid(row=1, column=1, pady=8, padx=(10, 0))
        self.product_name.bind('<<ComboboxSelected>>', self.on_product_name_change)
        
        # Specifications Frame
        self.spec_frame = tk.Frame(product_frame, bg='white')
        self.spec_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=15)
        
        # Quantity
        tk.Label(product_frame, 
                text="Quantity:", 
                font=('Arial', 10, 'bold'),
                bg='white').grid(row=3, column=0, sticky=tk.W, pady=8)
        
        self.quantity = ttk.Spinbox(product_frame, 
                                   from_=1, 
                                   to=100, 
                                   width=10,
                                   font=('Arial', 10))
        self.quantity.grid(row=3, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        self.quantity.set(1)
        
        # Add to Bill Button
        add_button = tk.Button(product_frame,
                              text="➕ ADD TO INVOICE",
                              command=self.add_to_bill,
                              bg=self.colors['secondary'],
                              fg='white',
                              font=('Arial', 10, 'bold'),
                              padx=20,
                              pady=8,
                              bd=0,
                              cursor='hand2',
                              activebackground='#2980b9')
        add_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Right panel - Bill Preview
        right_panel = tk.Frame(content_frame, bg='white', relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Bill Items Header
        bill_header = tk.Frame(right_panel, bg=self.colors['dark'])
        bill_header.pack(fill=tk.X)
        
        tk.Label(bill_header,
                text="INVOICE ITEMS",
                font=('Arial', 12, 'bold'),
                fg='white',
                bg=self.colors['dark']).pack(pady=10)
        
        # Bill Items Table
        table_frame = tk.Frame(right_panel, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create treeview with custom style
        style = ttk.Style()
        style.configure("Custom.Treeview",
                       background="white",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="white")
        style.map('Custom.Treeview',
                 background=[('selected', self.colors['secondary'])])
        
        columns = ('Description', 'Qty', 'Unit Price', 'Total')
        self.bill_tree = ttk.Treeview(table_frame,
                                        columns=columns,
                                        show='headings',
                                        style="Custom.Treeview",
                                        height=12)
        
        # Configure columns
        self.bill_tree.heading('Description', text='DESCRIPTION')
        self.bill_tree.heading('Qty', text='QTY')
        self.bill_tree.heading('Unit Price', text='UNIT PRICE')
        self.bill_tree.heading('Total', text='TOTAL')
        
        self.bill_tree.column('Description', width=250, anchor='w')
        self.bill_tree.column('Qty', width=80, anchor='center')
        self.bill_tree.column('Unit Price', width=120, anchor='e')
        self.bill_tree.column('Total', width=120, anchor='e')
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.bill_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.bill_tree.xview)
        self.bill_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.bill_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Totals Section
        totals_frame = tk.Frame(right_panel, bg='white')
        totals_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.subtotal_var = tk.StringVar(value="$0.00")
        self.tax_var = tk.StringVar(value="$0.00")
        
        tk.Label(totals_frame,
                text="TOTAL:",
                font=('Arial', 12, 'bold'),
                fg=self.colors['primary'],
                bg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        self.total_var = tk.StringVar(value="$0.00")
        tk.Label(totals_frame,
                textvariable=self.total_var,
                font=('Arial', 14, 'bold'),
                fg=self.colors['danger'],
                bg='white').pack(side=tk.LEFT)
        
        # Action Buttons
        action_frame = tk.Frame(right_panel, bg='white')
        action_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        clear_btn = tk.Button(action_frame,
                            text="🗑️ CLEAR ALL",
                            command=self.clear_bill,
                            bg=self.colors['light'],
                            fg=self.colors['dark'],
                            font=('Arial', 10, 'bold'),
                            padx=15,
                            pady=8,
                            bd=1,
                            cursor='hand2',
                            activebackground='#bdc3c7')
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        remove_btn = tk.Button(action_frame,
                             text="❌ REMOVE SELECTED",
                             command=self.remove_selected_item,
                             bg=self.colors['light'],
                             fg=self.colors['dark'],
                             font=('Arial', 10, 'bold'),
                             padx=15,
                             pady=8,
                             bd=1,
                             cursor='hand2',
                             activebackground='#bdc3c7')
        remove_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        generate_btn = tk.Button(action_frame,
                               text="💰 GENERATE INVOICE",
                               command=self.generate_bill,
                               bg=self.colors['success'],
                               fg='white',
                               font=('Arial', 11, 'bold'),
                               padx=25,
                               pady=10,
                               bd=0,
                               cursor='hand2',
                               activebackground='#229954')
        generate_btn.pack(side=tk.RIGHT)
        
        # Status Bar
        self.status_bar = tk.Label(self.root,
                                 text="Ready to create bill",
                                 bg=self.colors['primary'],
                                 fg='white',
                                 anchor=tk.W,
                                 font=('Arial', 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_products(self):
        """Load products from database"""
        try:
            self.solar_panels = db.get_data("solar_panels")
            self.batteries = db.get_data("batteries")
            self.inverters = db.get_data("inverters")
            self.update_status("Products loaded successfully")
        except Exception as e:
            self.update_status(f"Error loading products: {str(e)}", error=True)
    
    def on_product_type_change(self, event=None):
        """Update product names based on selected type"""
        ptype = self.product_type.get()
        self.product_name.set('')
        self.product_name['values'] = []
        
        # Clear spec frame
        for widget in self.spec_frame.winfo_children():
            widget.destroy()
        
        if ptype == 'Solar Panel':
            products = self.solar_panels
            unique_names = sorted(set([p[1] for p in products if len(p) > 1]))
            self.product_name['values'] = unique_names
            
            tk.Label(self.spec_frame, 
                    text="Wattage (W):", 
                    font=('Arial', 9, 'bold'),
                    bg='white').grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
            self.spec1 = ttk.Combobox(self.spec_frame, state='readonly', width=15, font=('Arial', 9))
            self.spec1.grid(row=0, column=1)
            
        elif ptype == 'Battery':
            products = self.batteries
            unique_names = sorted(set([p[1] for p in products if len(p) > 1]))
            self.product_name['values'] = unique_names
            
            tk.Label(self.spec_frame, 
                    text="Capacity (Ah):", 
                    font=('Arial', 9, 'bold'),
                    bg='white').grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
            self.spec1 = ttk.Combobox(self.spec_frame, state='readonly', width=15, font=('Arial', 9))
            self.spec1.grid(row=0, column=1)
            
            tk.Label(self.spec_frame, 
                    text="Voltage (V):", 
                    font=('Arial', 9, 'bold'),
                    bg='white').grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
            self.spec2 = ttk.Combobox(self.spec_frame, state='readonly', width=15, font=('Arial', 9))
            self.spec2.grid(row=1, column=1, pady=(5, 0))
            
        elif ptype == 'Inverter':
            products = self.inverters
            unique_names = sorted(set([p[1] for p in products if len(p) > 1]))
            self.product_name['values'] = unique_names
            
            tk.Label(self.spec_frame, 
                    text="Power (W):", 
                    font=('Arial', 9, 'bold'),
                    bg='white').grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
            self.spec1 = ttk.Combobox(self.spec_frame, state='readonly', width=15, font=('Arial', 9))
            self.spec1.grid(row=0, column=1)
    
    def on_product_name_change(self, event=None):
        """Update specifications based on selected product"""
        ptype = self.product_type.get()
        pname = self.product_name.get()
        
        if not pname:
            return
        
        if ptype == 'Solar Panel':
            products = self.solar_panels
            wattages = []
            for p in products:
                if len(p) > 2 and p[1] == pname:
                    wattages.append(str(p[2]))
            wattages = sorted(set(wattages))
            self.spec1['values'] = wattages
            if wattages:
                self.spec1.set(wattages[0])
                
        elif ptype == 'Battery':
            products = self.batteries
            capacities = []
            voltages = []
            for p in products:
                if len(p) > 3 and p[1] == pname:
                    capacities.append(str(p[2]))
                    voltages.append(str(p[3]))
            
            capacities = sorted(set(capacities))
            voltages = sorted(set(voltages))
            
            self.spec1['values'] = capacities
            self.spec2['values'] = voltages
            
            if capacities:
                self.spec1.set(capacities[0])
            if voltages:
                self.spec2.set(voltages[0])
                
        elif ptype == 'Inverter':
            products = self.inverters
            powers = []
            for p in products:
                if len(p) > 2 and p[1] == pname:
                    powers.append(str(p[2]))
            powers = sorted(set(powers))
            self.spec1['values'] = powers
            if powers:
                self.spec1.set(powers[0])

    def add_to_bill(self):
        """Add selected product to bill"""
        if not self.customer_name.get():
            messagebox.showwarning("Warning", "Please enter customer name")
            return
        
        ptype = self.product_type.get()
        pname = self.product_name.get()
        
        if not ptype or not pname:
            messagebox.showwarning("Warning", "Please select a product")
            return
        
        try:
            qty = int(self.quantity.get())
            if qty <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Warning", "Please enter valid quantity")
            return
        
        try:
            if ptype == 'Solar Panel':
                if not hasattr(self, 'spec1') or not self.spec1.get():
                    messagebox.showwarning("Warning", "Please select wattage")
                    return
                wattage = int(self.spec1.get())
                item_tuple = (pname, wattage, qty)
                description = f"{pname} {wattage}W"
                
            elif ptype == 'Battery':
                if not hasattr(self, 'spec1') or not self.spec1.get():
                    messagebox.showwarning("Warning", "Please select capacity")
                    return
                if not hasattr(self, 'spec2') or not self.spec2.get():
                    messagebox.showwarning("Warning", "Please select voltage")
                    return
                capacity = int(self.spec1.get())
                voltage = int(self.spec2.get())
                item_tuple = (pname, capacity, voltage, qty)
                description = f"{pname} {capacity}Ah/{voltage}V"
                
            elif ptype == 'Inverter':
                if not hasattr(self, 'spec1') or not self.spec1.get():
                    messagebox.showwarning("Warning", "Please select power")
                    return
                power = int(float(self.spec1.get()))
                item_tuple = (pname, power, qty)
                description = f"{pname} {power}W"
            
            else:
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid specification value")
            return
        
        try:
            temp_bill = Bill(self.customer_name.get(), [item_tuple])
            prices = temp_bill.get_prices()
            price = prices.get(item_tuple, 0)
            
            if price == 0:
                messagebox.showerror("Error", "Could not find price for selected product")
                return
                
        except Exception as e:
            messagebox.showerror("Error", f"Error getting price: {str(e)}")
            return
        
        self.bill_items.append(item_tuple)
        
        total = price * qty
        tags = ('evenrow',) if len(self.bill_tree.get_children()) % 2 == 0 else ('oddrow',)
        self.bill_tree.insert('', 'end', 
                                values=(description, qty, f"${price:,.2f}", f"${total:,.2f}"),
                                tags=tags)
        
        self.bill_tree.tag_configure('evenrow', background='#f9f9f9')
        self.bill_tree.tag_configure('oddrow', background='white')
        
        self.update_totals()
        
        self.product_name.set('')
        self.quantity.set(1)
        
        self.update_status(f"Added {description} to bill")

    def update_totals(self):
        """Update bill totals"""
        subtotal = 0
        for child in self.bill_tree.get_children():
            values = self.bill_tree.item(child)['values']
            total_str = values[3].replace('$', '').replace(',', '')
            subtotal += float(total_str)
        
        tax = subtotal * 0
        total = subtotal + tax
        
        self.subtotal_var.set(f"${subtotal:,.2f}")
        self.tax_var.set(f"${tax:,.2f}")
        self.total_var.set(f"${total:,.2f}")

    def clear_bill(self):
        """Clear all items from bill"""
        if not self.bill_items:
            return
        
        if messagebox.askyesno("Clear Bill", 
                              "Are you sure you want to clear all items from the bill?"):
            self.bill_tree.delete(*self.bill_tree.get_children())
            self.bill_items.clear()
            self.update_totals()
            self.update_status("Bill cleared")

    def remove_selected_item(self):
        """Remove selected item from bill"""
        selection = self.bill_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        item = selection[0]
        index = self.bill_tree.index(item)
        
        if index < len(self.bill_items):
            self.bill_items.pop(index)
        
        self.bill_tree.delete(item)
        self.update_totals()
        self.update_status("Item removed from bill")
        
        for i, child in enumerate(self.bill_tree.get_children()):
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            self.bill_tree.item(child, tags=tags)
    
    def generate_bill(self):
        """Generate bill using your Bill class"""
        if not self.customer_name.get():
            messagebox.showwarning("Warning", "Please enter customer name")
            return
        
        if not self.bill_items:
            messagebox.showwarning("Warning", "Please add items to the bill")
            return
        
        customer = self.customer_name.get().strip()
        date = self.bill_date.get().strip()
        
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
            return
        
        subtotal = float(self.subtotal_var.get().replace('$', '').replace(',', ''))
        tax = float(self.tax_var.get().replace('$', '').replace(',', ''))
        total = float(self.total_var.get().replace('$', '').replace(',', ''))
        
        confirm_msg = (
            f"Generate bill for {customer}?\n\n"
            f"Date: {date}\n"
            f"Items: {len(self.bill_items)}\n"
            f"Subtotal: ${subtotal:,.2f}\n"
            f"Total: ${total:,.2f}\n\n"
            f"This will save to database and generate PDF."
        )
        
        if not messagebox.askyesno("Confirm Bill", confirm_msg):
            return
        
        try:
            bill = Bill(
                customer_name=customer,
                items=self.bill_items,
                date=date
            )
            
            bill.generate_bill()
            
            pdf_path = f"{customer} Bill.pdf"
            messagebox.showinfo("Success", 
                              f"✅ Bill generated successfully!\n\n"
                              f"Customer: {customer}\n"
                              f"Total Amount: ${total:,.2f}\n"
                              f"PDF saved as: {pdf_path}")
            
            self.clear_bill()
            self.customer_name.delete(0, tk.END)
            self.bill_date.delete(0, tk.END)
            self.bill_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
            
            self.update_status("✅ Bill generated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bill:\n\n{str(e)}")
            self.update_status(f"❌ Error: {str(e)}", error=True)
    
    def update_status(self, message, error=False):
        """Update status bar"""
        if error:
            self.status_bar.config(text=f"❌ {message}", fg='#e74c3c')
        else:
            self.status_bar.config(text=f"✓ {message}", fg='#27ae60')
        
        if not error:
            self.root.after(5000, lambda: self.status_bar.config(text="Ready to create bill", fg='white'))
