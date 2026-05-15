import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Budget Tracker")
        self.root.geometry("1280x720")
        
        # database
        self.init_db()

        # sidebar
        self.build_layout()
        
        # dashboard
        self.show_dashboard()

    def init_db(self):
        """database and tables"""
        self.conn = sqlite3.connect("budget_tracker.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Categories (
                CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                CategoryName TEXT NOT NULL,
                Type TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT NOT NULL,
                Amount REAL NOT NULL,
                CategoryID INTEGER,
                FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Subscriptions (
                SubscriptionID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Amount REAL NOT NULL,
                DueDate INTEGER NOT NULL,
                CategoryID INTEGER,
                FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
            )
        ''')
        self.conn.commit()

        # categories in categories table to be added
        self.cursor.execute("SELECT COUNT(*) FROM Categories")
        if self.cursor.fetchone()[0] == 0:
            defaults = [("Food", "Expense"), ("Transport", "Expense"), ("Salary", "Income")]
            self.cursor.executemany("INSERT INTO Categories (CategoryName, Type) VALUES (?, ?)", defaults)
            self.conn.commit()

    def build_layout(self):
        # left sidebar
        self.sidebar_frame = tk.Frame(self.root, bg="#B0B0B0", width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # dont shrink sidebar
        self.sidebar_frame.pack_propagate(False) 

        # sidebar Title
        tk.Label(self.sidebar_frame, text="Desktop Budget Tracker", bg="#B0B0B0", fg="black", font=("Poppins", 16, "bold")).pack(pady=30)

        # navigation Buttons
        btn_style = {"bg": "#34495E", "fg": "black", "font": ("Poppins", 12), "borderwidth": 0, "pady": 10}
        
        tk.Button(self.sidebar_frame, text="Dashboard", command=self.show_dashboard, **btn_style).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self.sidebar_frame, text="Transactions", command=self.show_transactions, **btn_style).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self.sidebar_frame, text="Subscriptions", command=self.show_subscriptions, **btn_style).pack(fill=tk.X, padx=10, pady=5)

        # right screen
        self.main_content_frame = tk.Frame(self.root, bg="#939393")
        self.main_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def clear_main_content(self):
        """wipes the right side of the screen"""
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()


    # PAGE 1: DASHBOARD / to be completed

    def show_dashboard(self):
        self.clear_main_content()
        
        tk.Label(self.main_content_frame, text="Dashboard Overview", font=("Poppins", 24, "bold"),fg="black", bg="#939393").pack(pady=20, anchor=tk.W, padx=20)
        tk.Label(self.main_content_frame, text="charts and real value api", font=("Poppins", 14),fg="black", bg="#939393").pack(pady=10, anchor=tk.W, padx=20)


    # PAGE 2: TRANSACTIONS 

    def show_transactions(self):
        self.clear_main_content()
        
        tk.Label(self.main_content_frame, text="Manage Transactions", font=("Poppins", 24, "bold"), fg="black", bg="#939393").pack(pady=20, anchor=tk.W, padx=20)

        # inputs
        input_frame = tk.Frame(self.main_content_frame, bg="#939393")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Date (DD/MM/YYYY):", fg="black", bg="#939393").grid(row=0, column=0, padx=5)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Category:", fg="black", bg="#939393").grid(row=0, column=4, padx=5)

        self.cursor.execute("SELECT CategoryID, CategoryName FROM Categories")
        categories = self.cursor.fetchall()
        self.category_map = {name: cid for cid, name in categories}
        
        self.category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(input_frame, textvariable=self.category_var, values=list(self.category_map.keys()), state="readonly", width=12)
        category_dropdown.grid(row=0, column = 5, padx = 5)

        self.cursor.execute("SELECT CategoryID, CategoryName FROM Categories")
        categories = self.cursor.fetchall()
        self.category_map = {name: cid for cid, name in categories}

        tk.Label(input_frame, text="Amount:", fg="black", bg="#939393").grid(row=0, column=2, padx=5)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=3, padx=5)

        tk.Button(input_frame, text="Add Transaction", fg="black", bg="#939393", command=self.add_transaction).grid(row=0, column=6, padx=15)

        # table area
        table_frame = tk.Frame(self.main_content_frame)
        table_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)

        # treeview 
        columns = ("ID", "Date", "Amount")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("ID", text="Trans. ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Amount", text="Amount (PLN)")
        
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Date", width=200, anchor=tk.CENTER)
        self.tree.column("Amount", width=200, anchor=tk.E)
        self.tree.pack(fill=tk.BOTH, expand=True)

        
        self.load_transactions()

        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Date", width=200, anchor=tk.CENTER)
        self.tree.column("Amount", width=200, anchor=tk.E)
        self.tree.pack(fill=tk.BOTH, expand=True)

        tk.Button(table_frame, text="Edit Selected Transaction", fg="black", bg="#939393", command=self.edit_transaction).pack(pady=5)
        tk.Button(table_frame, text="Delete Selected Transation", fg="black", bg="#939393", command=self.delete_transation).pack(pady=5)

        self.load_transactions()

    
    # PAGE 3: SUBSCRIPTIONS / UI to be completed
   
    def show_subscriptions(self):
        self.clear_main_content()
        
        tk.Label(self.main_content_frame, text="Subscription Manager", font=("Poppins", 24, "bold"), fg="black", bg="#939393").pack(pady=20, anchor=tk.W, padx=20)
        tk.Label(self.main_content_frame, text="Your recurring bills will go here.", font=("Poppins", 14), fg="black", bg="#939393").pack(pady=10, anchor=tk.W, padx=20)

    
    # DATABASE FUNCTIONS
    
    def add_transaction(self): 
        date_val = self.date_entry.get()
        amount_val = self.amount_entry.get()
        category_name = self.category_var.get()
        category_id = self.category_map.get(category_name)
        
        if date_val == "" or amount_val == "":
            messagebox.showwarning("Missing Input", "Please fill in all fields before adding a transaction. ")
            return
        
        try:
            amount_val = float(amount_val)
        except ValueError:
            messagebox.showerror("Invalid Amount", "The Amount must contain only numbers!" )
            return
        
        import re 
        if not re.match(r'\d{2}/\d{2}/\d{4}$', date_val):
            messagebox.showerror("Invalid Date", "Please enter the date in DD/MM/YYYY format. ")
            return
            
        self.cursor.execute("INSERT INTO Transactions (Date, Amount, CategoryID) VALUES (?, ?, ?)", (date_val, amount_val, category_id))
        self.conn.commit()
        
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        
        self.load_transactions()

    def load_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.cursor.execute("SELECT TransactionID, Date, Amount FROM Transactions")
        records = self.cursor.fetchall()
        
        for row in records:
            self.tree.insert("", tk.END, values=row)

    def delete_transation(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a transation from the table to delete. ")
            return
        
        confirm = messagebox.askyesno("Confirm Deletion" , "Are you sure you want to permanently delete this transaction? ")

        if confirm:
            item_values = self.tree.item(selected_item, "values")
            transaction_id = item_values[0]

            self.cursor.execute("DELETE FROM Transactions WHERE TransactionID = ?", (transaction_id,))
            self.conn.commit()

            self.load_transactions()

    def edit_transaction(self):
        
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a transaction from the table to edit.")
            return

        
        item_values = self.tree.item(selected_item, "values")
        transaction_id = item_values[0]

        
        self.cursor.execute("""
            SELECT Transactions.Date, Transactions.Amount, Categories.CategoryName 
            FROM Transactions 
            JOIN Categories ON Transactions.CategoryID = Categories.CategoryID 
            WHERE TransactionID = ?
        """, (transaction_id,))
        record = self.cursor.fetchone()
        
        if not record:
            return
            
        current_date, current_amount, current_category = record

        # pop up window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Transaction")
        edit_window.configure(bg="#939393")
        
        
        edit_window.transient(self.root)
        edit_window.grab_set()
        edit_window.focus_force()
        

        tk.Label(edit_window, text="Edit Transaction", font=("Poppins", 16, "bold"), bg="#939393", fg="black").pack(pady=15)

        
        tk.Label(edit_window, text="Date (DD/MM/YYYY):", bg="#939393", fg="black").pack()
        date_edit = tk.Entry(edit_window)
        date_edit.insert(0, current_date)
        date_edit.pack(pady=5)

        
        tk.Label(edit_window, text="Amount:", bg="#939393", fg="black").pack()
        amount_edit = tk.Entry(edit_window)
        amount_edit.insert(0, current_amount)
        amount_edit.pack(pady=5)

        
        tk.Label(edit_window, text="Category:", bg="#939393", fg="black").pack()
        
        
        category_edit_var = tk.StringVar(edit_window, value=current_category) 
        category_edit_dropdown = ttk.Combobox(edit_window, textvariable=category_edit_var, values=list(self.category_map.keys()), state="readonly")
        category_edit_dropdown.pack(pady=5)

        # save
        def save_edits(event=None):
            new_date = date_edit.get()
            new_amount = amount_edit.get()
            
            
            new_cat_name = category_edit_dropdown.get() 
            
            
            if new_date == "" or new_amount == "" or new_cat_name == "":
                messagebox.showwarning("Missing Input", "Please fill in all fields.")
                return
            try:
                new_amount = float(new_amount)
            except ValueError:
                messagebox.showerror("Invalid Amount", "Amount must be a number!")
                return
            import re 
            if not re.match(r'\d{2}/\d{2}/\d{4}$', new_date):
                messagebox.showerror("Invalid Date", "Format must be DD/MM/YYYY.")
                return
                
            new_cat_id = self.category_map.get(new_cat_name)
            
            if new_cat_id is None:
                messagebox.showerror("Error", "Please select a valid category.")
                return

            # update
            self.cursor.execute("UPDATE Transactions SET Date = ?, Amount = ?, CategoryID = ? WHERE TransactionID = ?", 
                                (new_date, new_amount, new_cat_id, transaction_id))
            self.conn.commit()
            
            # refresh main table and close the pop up
            self.load_transactions()
            edit_window.destroy()
            messagebox.showinfo("Success", "Transaction updated successfully!")


        
        
        edit_window.bind('<Return>', save_edits)

        # 5. save the changes
        def save_edits(event=None):
            new_date = date_edit.get()
            new_amount = amount_edit.get()
            new_cat_name = category_edit_var.get()
            
            # validation
            if new_date == "" or new_amount == "":
                messagebox.showwarning("Missing Input", "Please fill in all fields.")
                return
            try:
                new_amount = float(new_amount)
            except ValueError:
                messagebox.showerror("Invalid Amount", "Amount must be a number!")
                return
            import re 
            if not re.match(r'\d{2}/\d{2}/\d{4}$', new_date):
                messagebox.showerror("Invalid Date", "Format must be DD/MM/YYYY.")
                return
                
            new_cat_id = self.category_map.get(new_cat_name)

            # update the validation
            self.cursor.execute("UPDATE Transactions SET Date = ?, Amount = ?, CategoryID = ? WHERE TransactionID = ?", 
                                (new_date, new_amount, new_cat_id, transaction_id))
            self.conn.commit()
            
            
            self.load_transactions()
            edit_window.destroy()
            messagebox.showinfo("Success", "Transaction updated successfully!")

       
        tk.Button(edit_window, text="Save Changes", command=save_edits).pack(pady=20)
        
        
        edit_window.bind('<Return>', save_edits)


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()