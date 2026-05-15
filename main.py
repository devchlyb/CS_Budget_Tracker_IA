import tkinter as tk
from app import BudgetTrackerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()