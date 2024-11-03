import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from earnings import EarningsManager
from spendings import SpendingsManager
from expense_analysis import ExpenseAnalysis
from auth import Auth
from PIL import Image, ImageTk


class UserPage:
    def __init__(self, root, username, on_logout, auth_instance):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.auth = auth_instance  # Store the Auth instance
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
        self.clear_content(self.right_frame)

        # Calculate the monthly balance
        monthly_balance = ExpenseAnalysis.calculate_monthly_balance(self.username)
        tk.Label(self.right_frame, text=f"Your monthly balance: ${monthly_balance:.2f}", font=("Arial", 10)).pack(
            pady=5)

    def show_spendings_list(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()

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

        # Checkbox for recurring earning
        recurring_var = tk.BooleanVar()
        tk.Checkbutton(self.right_frame, text="Recurring Monthly", variable=recurring_var).pack()

        def save_earning():
            try:
                amount = float(amount_entry.get())
                description = description_entry.get()
                date = date_entry.get()  # Get date from entry field
                recurring = recurring_var.get()  # Check if recurring checkbox is selected
                EarningsManager.add_earning(self.username, amount, description, date, recurring)
                tk.Label(self.right_frame, text="Earning Added!").pack()

                # Clear entries
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

        # Collect expense details
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

        tk.Label(self.right_frame, text="Category").pack()
        category_entry = tk.Entry(self.right_frame)
        category_entry.pack()

        def save_expense():
            try:
                amount = float(amount_entry.get())
                description = description_entry.get()
                date = date_entry.get()  # Get date from entry field
                category = category_entry.get()  # Get category from entry field

                # Validate date format
                datetime.strptime(date, "%Y-%m-%d")  # Will raise ValueError if format is incorrect

                # Check if the expense exceeds the limit
                expense_limit = self.auth.get_expense_limit(self.username)
                if expense_limit is not None and amount > expense_limit:
                    messagebox.showwarning("Expense Limit Exceeded",
                                           f"You are exceeding your expense limit of ${expense_limit:.2f}.")

                # Save the spending with a validated date and category
                SpendingsManager.add_spending(self.username, amount, description, date, category)
                tk.Label(self.right_frame, text="Expense Added!").pack()

                # Clear entries
                amount_entry.delete(0, tk.END)
                description_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                category_entry.delete(0, tk.END)
                date_entry.insert(0, today)  # Reset date to today's date

            except ValueError as e:
                if "time data" in str(e):
                    messagebox.showerror("Input Error", "Please enter a valid date (YYYY-MM-DD).")
                else:
                    messagebox.showerror("Input Error", "Please enter valid values.")

        tk.Button(self.right_frame, text="Save Expense", command=save_expense).pack()

    def analyze_expense(self):
        self.clear_content(self.right_frame)

        # Title and period selection setup
        tk.Label(self.right_frame, text="Analyze Expenses", font=("Arial", 12, "bold")).pack(pady=5)

        period_options = ["Monthly", "Quarterly", "Annually"]
        period_var = tk.StringVar(value="Monthly")
        period_dropdown = ttk.Combobox(self.right_frame, textvariable=period_var, values=period_options,
                                       state="readonly")
        period_dropdown.pack(pady=5)

        def show_analysis():
            period = period_var.get()
            # Generate and display the chart
            chart_path = ExpenseAnalysis.generate_expense_chart(self.username, period)
            self.display_chart(chart_path)

        tk.Button(self.right_frame, text="Show Analysis", command=show_analysis).pack(pady=10)

    def display_chart(self, chart_path):
        # Calculate the total amount spent this month
        monthly_spent = ExpenseAnalysis.get_monthly_spending(self.username)

        # Create a new Toplevel window for the chart
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Analysis Chart")

        # Set the size of the new window if needed
        chart_window.geometry("600x500")

        # Display the amount spent this month at the top
        tk.Label(chart_window, text=f"Amount Spent This Month: ${monthly_spent:.2f}", font=("Arial", 12, "bold")).pack(
            pady=10)

        # Load and display the chart image
        chart_image = Image.open(chart_path)
        chart_photo = ImageTk.PhotoImage(chart_image)

        # Add the image to the new window
        chart_label = tk.Label(chart_window, image=chart_photo)
        chart_label.image = chart_photo  # Store a reference to avoid garbage collection
        chart_label.pack()

        # Optional: Add a close button
        tk.Button(chart_window, text="Close", command=chart_window.destroy).pack(pady=10)
    def set_expense_limit(self):
        self.clear_content(self.right_frame)

        tk.Label(self.right_frame, text="Set your Expense Limit:").pack()
        limit_entry = tk.Entry(self.right_frame)
        limit_entry.pack()

        def save_limit():
            try:
                limit = float(limit_entry.get())
                self.auth.set_expense_limit(self.username, limit)
                tk.Label(self.right_frame, text=f"Expense limit set to: ${limit:.2f}").pack()
                limit_entry.delete(0, tk.END)  # Clear entry
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid limit.")

        tk.Button(self.right_frame, text="Save Limit", command=save_limit).pack()

    def clear_content(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
