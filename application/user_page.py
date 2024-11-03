import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from earnings import EarningsManager
from spendings import SpendingsManager


class UserPage:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.show_user_home()

    def show_user_home(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a navigation bar at the top
        nav_frame = tk.Frame(self.root, bg="lightgray")
        nav_frame.pack(side="top", fill="x")

        # Add navigation buttons to the navigation bar
        tk.Button(nav_frame, text="Add Expense", command=self.add_expense).pack(side="left", padx=10, pady=5)
        tk.Button(nav_frame, text="Add Earning", command=self.add_earning).pack(side="left", padx=10, pady=5)
        tk.Button(nav_frame, text="Analyze Expense", command=self.analyze_expense).pack(side="left", padx=10, pady=5)
        tk.Button(nav_frame, text="Set Expense Limit", command=self.set_expense_limit).pack(side="left", padx=10,
                                                                                            pady=5)
        tk.Button(nav_frame, text="Logout", command=self.on_logout).pack(side="right", padx=10, pady=5)

        # Welcome message frame
        welcome_frame = tk.Frame(self.root)
        welcome_frame.pack(fill="x", pady=5)
        welcome_message = f"Welcome, {self.username}"
        tk.Label(welcome_frame, text=welcome_message, font=("Arial", 12), anchor="center").pack()

        # Main content area below the welcome message, divided into left and right frames
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, pady=10)

        # Left frame for spendings list
        self.left_frame = tk.Frame(self.content_frame, width=200, bg="lightgray")
        self.left_frame.pack(side="left", fill="y")

        # Right frame for dynamic content
        self.right_frame = tk.Frame(self.content_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.show_default_content()
        self.show_spendings_list()

    def show_default_content(self):
        tk.Label(self.right_frame, text="You have xxx amount left this month", font=("Arial", 10)).pack(pady=5)
        tk.Label(self.right_frame, text="You can spend: xxx", font=("Arial", 10)).pack(pady=5)

    def show_spendings_list(self):
        # Clear the left frame
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Load and display spendings for the current user
        tk.Label(self.left_frame, text="Your Spendings:", bg="lightgray", font=("Arial", 10, "bold")).pack(anchor="w",
                                                                                                           padx=10,
                                                                                                           pady=5)

        spendings = SpendingsManager.get_user_spendings(self.username)
        for entry in spendings:
            spending_text = f"Amount: {entry['amount']}, Date: {entry['date']}, Category: {entry['category']}"
            tk.Label(self.left_frame, text=spending_text, bg="lightgray", anchor="w").pack(fill="x", padx=10, pady=2)

    # Functionality Methods
    def add_earning(self):
        self.clear_content(self.right_frame)

        # Current date
        today = datetime.now().strftime("%Y-%m-%d")

        # Collect earning details
        tk.Label(self.right_frame, text="Amount").pack()
        amount_entry = tk.Entry(self.right_frame)
        amount_entry.pack()

        tk.Label(self.right_frame, text="Description").pack()
        description_entry = tk.Entry(self.right_frame)
        description_entry.pack()

        tk.Label(self.right_frame, text="Date (YYYY-MM-DD)").pack()
        date_entry = tk.Entry(self.right_frame)
        date_entry.insert(0, today)  # Set default date to today
        date_entry.pack()

        def save_earning():
            try:
                amount = float(amount_entry.get())
                description = description_entry.get()
                date = date_entry.get()  # Get date from entry field
                EarningsManager.add_earning(self.username, amount, date, description)
                tk.Label(self.right_frame, text="Earning Added!").pack()
                amount_entry.delete(0, tk.END)
                description_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                date_entry.insert(0, today)  # Reset date to today's date
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid amount.")

        tk.Button(self.right_frame, text="Save Earning", command=save_earning).pack()

    def add_expense(self):
        self.clear_content(self.right_frame)

        # Current date
        today = datetime.now().strftime("%Y-%m-%d")

        # Collect spending details
        tk.Label(self.right_frame, text="Amount").pack()
        amount_entry = tk.Entry(self.right_frame)
        amount_entry.pack()

        tk.Label(self.right_frame, text="Description").pack()
        description_entry = tk.Entry(self.right_frame)
        description_entry.pack()

        tk.Label(self.right_frame, text="Category").pack()
        category_entry = tk.Entry(self.right_frame)
        category_entry.pack()

        tk.Label(self.right_frame, text="Date (YYYY-MM-DD)").pack()
        date_entry = tk.Entry(self.right_frame)
        date_entry.insert(0, today)  # Set default date to today
        date_entry.pack()

        def save_spending():
            try:
                amount = float(amount_entry.get())
                description = description_entry.get()
                category = category_entry.get()
                date = date_entry.get()  # Get date from entry field
                SpendingsManager.add_spending(self.username, amount, description, category, date)
                tk.Label(self.right_frame, text="Spending Added!").pack()
                amount_entry.delete(0, tk.END)
                description_entry.delete(0, tk.END)
                category_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                date_entry.insert(0, today)  # Reset date to today's date
                self.show_spendings_list()  # Refresh spendings list on the left
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid amount.")

        tk.Button(self.right_frame, text="Save Spending", command=save_spending).pack()

    def analyze_expense(self):
        self.clear_content(self.right_frame)
        tk.Label(self.right_frame, text="Analyze Expense functionality goes here.", font=("Arial", 12)).pack()

    def set_expense_limit(self):
        self.clear_content(self.right_frame)
        tk.Label(self.right_frame, text="Set Expense Limit functionality goes here.", font=("Arial", 12)).pack()

    def clear_content(self, frame=None):
        target_frame = frame if frame else self.right_frame
        for widget in target_frame.winfo_children():
            widget.destroy()
