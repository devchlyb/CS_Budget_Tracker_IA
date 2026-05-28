import tkinter as tk
from tkinter import ttk, messagebox
import re
from tkcalendar import DateEntry
from datetime import datetime

def show_transactions(app):
    app.clear_main_content()

    tk.Label(app.main_content_frame, text="Manage Transactions", font=("Helvetica", 24, "bold"), fg="black", bg="#939393").pack(pady=20, anchor=tk.W, padx=20)

    input_frame = tk.Frame(app.main_content_frame, bg="#939393")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Date:", fg="black", bg="#939393").grid(row=0, column=0, padx=5)
    app.date_entry = DateEntry(input_frame, width=12, background='darkblue',
                                foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
    app.date_entry.grid(row=0, column=1, padx=5)


    tk.Label(input_frame, text="Amount:", fg="black", bg="#939393").grid(row=0, column=2, padx=5)
    app.amount_entry = tk.Entry(input_frame)
    app.amount_entry.grid(row=0, column=3, padx=5)

    tk.Label(input_frame, text="Category:", fg="black", bg="#939393").grid(row=0, column=4, padx=5)

    categories = app.db.get_categories()
    app.category_map = {name: cid for cid, name in categories}

    app.category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(input_frame, textvariable=app.category_var, values=list(app.category_map.keys()), state="readonly", width=12)
    category_dropdown.grid(row=0, column=5, padx=5)

    tk.Button(input_frame, text="Add Transaction", fg="black", bg="#939393", command=lambda: _add_transaction(app)).grid(row=0, column=6, padx=15)

    table_frame = tk.Frame(app.main_content_frame)
    table_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)

    columns = ("ID", "Date", "Amount")
    app.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
    app.tree.heading("ID", text="Trans. ID")
    app.tree.heading("Date", text="Date")
    app.tree.heading("Amount", text="Amount (PLN)")

    app.tree.column("ID", width=100, anchor=tk.CENTER)
    app.tree.column("Date", width=200, anchor=tk.CENTER)
    app.tree.column("Amount", width=200, anchor=tk.E)
    app.tree.pack(fill=tk.BOTH, expand=True)

    tk.Button(table_frame, text="Edit Selected Transaction",   fg="black", bg="#939393", command=lambda: _edit_transaction(app)).pack(pady=5)
    tk.Button(table_frame, text="Delete Selected Transaction", fg="black", bg="#939393", command=lambda: _delete_transaction(app)).pack(pady=5)

    app.date_entry = DateEntry(input_frame, 
                               width=12, 
                               background='darkblue', 
                               foreground='white', 
                               borderwidth=2, 
                               date_pattern='dd/mm/yyyy')
    app.date_entry.grid(row=0, column=1, padx=5)


    app.date_entry.bind("<Key>", lambda e: "break")
    _load_transactions(app)


def _add_transaction(app):
    date_val = app.date_entry.get_date().strftime('%d/%m/%Y')
    amount_val = app.amount_entry.get()
    category_name = app.category_var.get()
    category_id = app.category_map.get(category_name)

    if date_val == "" or amount_val == "":
        messagebox.showwarning("Missing Input", "Please fill in all fields before adding a transaction.")
        return

    try:
        amount_val = float(amount_val)
    except ValueError:
        messagebox.showerror("Invalid Amount", "The Amount must contain only numbers!")
        return

    if not re.match(r'\d{2}/\d{2}/\d{4}$', date_val):
        messagebox.showerror("Invalid Date", "Please enter the date in DD/MM/YYYY format.")
        return

    app.db.add_transaction(date_val, amount_val, category_id)
    app.amount_entry.delete(0, tk.END)
    _load_transactions(app)


def _load_transactions(app):
    for item in app.tree.get_children():
        app.tree.delete(item)
    for row in app.db.get_transactions():
        app.tree.insert("", tk.END, values=row)


def _delete_transaction(app):
    selected_item = app.tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a transaction from the table to delete.")
        return

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to permanently delete this transaction?")
    if confirm:
        transaction_id = app.tree.item(selected_item, "values")[0]
        app.db.delete_transaction(transaction_id)
        _load_transactions(app)


def _edit_transaction(app):
    selected_item = app.tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a transaction from the table to edit.")
        return

    transaction_id = app.tree.item(selected_item, "values")[0]
    record = app.db.get_transaction_by_id(transaction_id)
    if not record:
        return

    current_date, current_amount, current_category = record

    edit_window = tk.Toplevel(app.root)
    edit_window.title("Edit Transaction")
    edit_window.configure(bg="#939393")
    edit_window.transient(app.root)
    edit_window.grab_set()
    edit_window.focus_force()

    tk.Label(edit_window, text="Edit Transaction", font=("Helvetica", 16, "bold"), bg="#939393", fg="black").pack(pady=15)

    tk.Label(edit_window, text="Date:", bg="#939393").pack()
    date_edit = DateEntry(edit_window, width=12, date_pattern='dd/mm/yyyy')

    date_edit.bind("<Key>", lambda e: "break")
    
    date_obj = datetime.strptime(current_date, '%d/%m/%Y')
    date_edit.set_date(date_obj)
    date_edit.pack(pady=5)

    tk.Label(edit_window, text="Amount:", bg="#939393", fg="black").pack()
    amount_edit = tk.Entry(edit_window)
    amount_edit.insert(0, current_amount)
    amount_edit.pack(pady=5)

    tk.Label(edit_window, text="Category:", bg="#939393", fg="black").pack()
    category_edit_var = tk.StringVar(edit_window, value=current_category)
    category_edit_dropdown = ttk.Combobox(edit_window, textvariable=category_edit_var, values=list(app.category_map.keys()), state="readonly")
    category_edit_dropdown.pack(pady=5)

    def save_edits(event=None):
        new_date = date_edit.get()
        new_amount = amount_edit.get()
        new_cat_name = category_edit_var.get()

        if new_date == "" or new_amount == "" or new_cat_name == "":
            messagebox.showwarning("Missing Input", "Please fill in all fields.")
            return
        try:
            new_amount = float(new_amount)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Amount must be a number!")
            return
        if not re.match(r'\d{2}/\d{2}/\d{4}$', new_date):
            messagebox.showerror("Invalid Date", "Format must be DD/MM/YYYY.")
            return

        new_cat_id = app.category_map.get(new_cat_name)
        app.db.update_transaction(transaction_id, new_date, new_amount, new_cat_id)
        _load_transactions(app)
        edit_window.destroy()
        messagebox.showinfo("Success", "Transaction updated successfully!")

    tk.Button(edit_window, text="Save Changes", command=save_edits).pack(pady=20)
    edit_window.bind('<Return>', save_edits)