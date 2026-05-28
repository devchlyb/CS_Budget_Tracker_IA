import tkinter as tk
from database import DatabaseManager
from pages.dashboard import show_dashboard
from pages.transactions import show_transactions
from pages.subscriptions import show_subscriptions

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Budget Tracker")
        self.root.geometry("1280x720")

        self.db = DatabaseManager() 

        self._build_layout()
        show_dashboard(self)

    def _build_layout(self):
        self.sidebar_frame = tk.Frame(self.root, bg="#B0B0B0", width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        tk.Label(self.sidebar_frame, text="Desktop Budget Tracker", bg="#B0B0B0", fg="black", font=("Helvetica", 16, "bold")).pack(pady=30)

        btn_style = {"bg": "#34495E", "fg": "black", "font": ("Helvetica", 12), "borderwidth": 0, "pady": 10}

        tk.Button(self.sidebar_frame, text="Dashboard",     command=lambda: show_dashboard(self),     **btn_style).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self.sidebar_frame, text="Transactions",  command=lambda: show_transactions(self),  **btn_style).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self.sidebar_frame, text="Subscriptions", command=lambda: show_subscriptions(self), **btn_style).pack(fill=tk.X, padx=10, pady=5)

        self.main_content_frame = tk.Frame(self.root, bg="#939393")
        self.main_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def clear_main_content(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()