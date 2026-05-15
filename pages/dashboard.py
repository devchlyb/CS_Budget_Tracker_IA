import tkinter as tk

def show_dashboard(app):
    app.clear_main_content()
    tk.Label(app.main_content_frame, text="Dashboard Overview", font=("Poppins", 24, "bold"), fg="black", bg="#939393").pack(pady=20, anchor=tk.W, padx=20)
    tk.Label(app.main_content_frame, text="charts and real value api", font=("Poppins", 14), fg="black", bg="#939393").pack(pady=10, anchor=tk.W, padx=20)