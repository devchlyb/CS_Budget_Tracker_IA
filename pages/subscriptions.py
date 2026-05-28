import tkinter as tk

def show_subscriptions(app):
    app.clear_main_content()
    tk.Label(app.main_content_frame, text="Subscription Manager", font=("Helvetica", 24, "bold"), fg="black", bg="#939393").pack(pady=20, anchor=tk.W, padx=20)
    tk.Label(app.main_content_frame, text="Your recurring bills will go here.", font=("Helvetica", 14), fg="black", bg="#939393").pack(pady=10, anchor=tk.W, padx=20)