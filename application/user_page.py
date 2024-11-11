from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
from earnings import EarningsManager
from spendings import SpendingsManager
from expense_analysis import ExpenseAnalysis
from PIL import Image, ImageTk


class UserPage:
    def __init__(self, root, username, on_logout, auth_instance):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.auth = auth_instance
        self.show_user_home()

    def show_user_home(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a navigation bar at the top
        nav_frame = ttk.Frame(self.root, bootstyle="secondary")
        nav_frame.pack(side="top", fill="x")

        # Add navigation buttons to the navigation bar
        ttk.Button(
            nav_frame, text="Add Expense", command=self.add_expense, bootstyle=PRIMARY
        ).pack(side="left", padx=10, pady=5)
        ttk.Button(
            nav_frame, text="Add Earning", command=self.add_earning, bootstyle=SUCCESS
        ).pack(side="left", padx=10, pady=5)
        ttk.Button(
            nav_frame,
            text="Analyze Expense",
            command=self.analyze_expense,
            bootstyle=INFO,
        ).pack(side="left", padx=10, pady=5)
        ttk.Button(
            nav_frame,
            text="Set Expense Limit",
            command=self.set_expense_limit,
            bootstyle=WARNING,
        ).pack(side="left", padx=10, pady=5)
        ttk.Button(
            nav_frame, text="Logout", command=self.on_logout, bootstyle=DANGER
        ).pack(side="right", padx=10, pady=5)

        # Welcome message frame
        welcome_frame = ttk.Frame(self.root)
        welcome_frame.pack(fill="x", pady=5)
        welcome_message = f"Welcome, {self.username}"
        ttk.Label(
            welcome_frame, text=welcome_message, font=("Arial", 12), anchor="center"
        ).pack()

        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, pady=10)

        # Left frame for spendings list
        self.left_frame = ttk.Frame(self.content_frame, bootstyle="info")
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Right frame for dynamic content
        self.right_frame = ttk.Frame(self.content_frame, bootstyle="light")
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.show_default_content()
        self.show_spendings_list()

    def show_default_content(self):
        self.clear_content(self.right_frame)

        # Calculate the monthly balance
        monthly_balance = ExpenseAnalysis.calculate_balance(self.username, "Monthly")
        ttk.Label(
            self.right_frame,
            text=f"Your monthly balance: ${monthly_balance:.2f}",
            font=("Arial", 10),
        ).pack(pady=5)

    def show_spendings_list(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        ttk.Label(
            self.left_frame,
            text="Your Spendings:",
            bootstyle="info-inverse",
            font=("Arial", 10, "bold"),
        ).pack(anchor="w", padx=10, pady=5)

        spendings = SpendingsManager.get_user_spendings(self.username)
        for entry in spendings:
            spending_text = f"Amount: {entry['amount']}, Date: {entry['date']}, Category: {entry['category']}"
            ttk.Label(
                self.left_frame,
                text=spending_text,
                bootstyle="info-inverse",
                anchor="w",
            ).pack(fill="x", padx=10, pady=2)

    # Functionality Methods
    def add_earning(self):
        self.clear_content(self.right_frame)
        today = datetime.now().strftime("%Y-%m-%d")

        ttk.Label(self.right_frame, text="Amount").pack()
        amount_entry = ttk.Entry(self.right_frame)
        amount_entry.pack()

        ttk.Label(self.right_frame, text="Description").pack()
        description_entry = ttk.Entry(self.right_frame)
        description_entry.pack()

        ttk.Label(self.right_frame, text="Date (YYYY-MM-DD)").pack()
        date_entry = ttk.Entry(self.right_frame)
        date_entry.insert(0, today)
        date_entry.pack()

        recurring_var = ttk.BooleanVar()
        ttk.Checkbutton(
            self.right_frame, text="Recurring Monthly", variable=recurring_var
        ).pack(pady=5)

        def save_earning():
            try:
                amount = float(amount_entry.get())
                description = description_entry.get()
                date = date_entry.get()
                recurring = recurring_var.get()
                EarningsManager.add_earning(
                    self.username, amount, description, date, recurring
                )
                ttk.Label(
                    self.right_frame, text="Earning Added!", bootstyle="success"
                ).pack()

                amount_entry.delete(0, ttk.END)
                description_entry.delete(0, ttk.END)
                date_entry.delete(0, ttk.END)
                date_entry.insert(0, today)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid amount.")

        ttk.Button(
            self.right_frame,
            text="Save Earning",
            command=save_earning,
            bootstyle=SUCCESS,
        ).pack()

    def add_expense(self):
        self.clear_content(self.right_frame)
        today = datetime.now().strftime("%Y-%m-%d")

        ttk.Label(self.right_frame, text="Amount").pack()
        amount_entry = ttk.Entry(self.right_frame)
        amount_entry.pack()

        ttk.Label(self.right_frame, text="Description").pack()
        description_entry = ttk.Entry(self.right_frame)
        description_entry.pack()

        ttk.Label(self.right_frame, text="Date (YYYY-MM-DD)").pack()
        date_entry = ttk.Entry(self.right_frame)
        date_entry.insert(0, today)
        date_entry.pack()

        ttk.Label(self.right_frame, text="Category").pack()
        category_entry = ttk.Entry(self.right_frame)
        category_entry.pack()

        def save_expense():
            try:
                amount = float(amount_entry.get())
                description = description_entry.get()
                date = date_entry.get()
                category = category_entry.get()
                datetime.strptime(date, "%Y-%m-%d")

                expense_limit = self.auth.get_expense_limit(self.username)
                if expense_limit is not None and amount > expense_limit:
                    messagebox.showwarning(
                        "Expense Limit Exceeded",
                        f"You are exceeding your expense limit of ${expense_limit:.2f}.",
                    )

                SpendingsManager.add_spending(
                    self.username, amount, description, date, category
                )
                ttk.Label(
                    self.right_frame, text="Expense Added!", bootstyle="danger"
                ).pack()

                amount_entry.delete(0, ttk.END)
                description_entry.delete(0, ttk.END)
                date_entry.delete(0, ttk.END)
                category_entry.delete(0, ttk.END)
                date_entry.insert(0, today)
            except ValueError as e:
                if "time data" in str(e):
                    messagebox.showerror(
                        "Input Error", "Please enter a valid date (YYYY-MM-DD)."
                    )
                else:
                    messagebox.showerror("Input Error", "Please enter valid values.")

        ttk.Button(
            self.right_frame,
            text="Save Expense",
            command=save_expense,
            bootstyle=DANGER,
        ).pack()

    def analyze_expense(self):
        self.clear_content(self.right_frame)

        ttk.Label(
            self.right_frame, text="Analyze Expenses", font=("Arial", 12, "bold")
        ).pack(pady=5)

        period_options = ["Monthly", "Quarterly", "Annually"]
        period_var = ttk.StringVar(value="Monthly")
        period_dropdown = ttk.Combobox(
            self.right_frame,
            textvariable=period_var,
            values=period_options,
            state="readonly",
        )
        period_dropdown.pack(pady=5)

        def show_analysis():
            period = period_var.get()
            chart_path = ExpenseAnalysis.generate_expense_chart(self.username, period)
            self.display_chart(chart_path, period)

        ttk.Button(
            self.right_frame,
            text="Show Analysis",
            command=show_analysis,
            bootstyle=INFO,
        ).pack(pady=80)

    def display_chart(self, chart_path, period):
        total_savings = ExpenseAnalysis.calculate_balance(self.username, period)

        chart_window = ttk.Toplevel(self.root)
        chart_window.title(f"{period} Expense Analysis Chart")
        chart_window.geometry("600x500")

        # Display the total savings for the period
        ttk.Label(
            chart_window,
            text=f"Total Savings {period}: ${total_savings:.2f}",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        try:
            chart_image = Image.open(chart_path)
            chart_photo = ImageTk.PhotoImage(chart_image)
            chart_label = ttk.Label(chart_window, image=chart_photo)
            chart_label.image = chart_photo
            chart_label.pack()
        except Exception as e:
            ttk.Label(
                chart_window, text="Error loading chart image.", font=("Arial", 10)
            ).pack()

        # Close button
        ttk.Button(
            chart_window,
            text="Close",
            command=chart_window.destroy,
            bootstyle="secondary",
        ).pack(pady=10)

    def set_expense_limit(self):
        self.clear_content(self.right_frame)
        ttk.Label(self.right_frame, text="Set your Expense Limit:").pack()
        limit_entry = ttk.Entry(self.right_frame)
        limit_entry.pack()

        def save_limit():
            try:
                limit = float(limit_entry.get())
                self.auth.set_expense_limit(self.username, limit)
                ttk.Label(
                    self.right_frame,
                    text=f"Expense limit set to: ${limit:.2f}",
                    bootstyle="success",
                ).pack()
                limit_entry.delete(0, ttk.END)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid limit.")

        ttk.Button(
            self.right_frame, text="Save Limit", command=save_limit, bootstyle=SUCCESS
        ).pack(pady=10)

    def clear_content(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
