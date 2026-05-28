import tkinter as tk
from services.inflation import get_latest_inflation


def show_dashboard(app):
    app.clear_main_content()

    tk.Label(app.main_content_frame, text="Dashboard Overview",
             font=("Helvetica", 24, "bold"), fg="black", bg="#939393").pack(pady=20, anchor=tk.W, padx=20)

    nominal_balance = app.db.get_balance()

    inflation_pct = get_latest_inflation()

    if inflation_pct is not None:
        real_value = nominal_balance / (1 + (inflation_pct / 100))
        inflation_text = f"Latest inflation (GUS, year-on-year): {inflation_pct:.1f}%"
        real_text = f"Real Value (inflation-adjusted): {real_value:.2f} PLN"
    else:
        inflation_text = "Latest inflation: unavailable (could not reach GUS API)"
        real_text = "Real Value: unavailable"

    tk.Label(app.main_content_frame, text=f"Nominal Balance: {nominal_balance:.2f} PLN",
             font=("Poppins", 16), fg="black", bg="#939393").pack(pady=10, anchor=tk.W, padx=20)
    tk.Label(app.main_content_frame, text=inflation_text,
             font=("Poppins", 14), fg="black", bg="#939393").pack(pady=5, anchor=tk.W, padx=20)
    tk.Label(app.main_content_frame, text=real_text,
             font=("Poppins", 16, "bold"), fg="black", bg="#939393").pack(pady=10, anchor=tk.W, padx=20)