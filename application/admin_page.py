from tkinter import messagebox
import ttkbootstrap as ttk
from docutils.nodes import description
from ttkbootstrap.constants import *
from datetime import datetime
from earnings import EarningsManager
from spendings import SpendingsManager
import json
import os

CREDENTIALS_FILE = "credentials.json"


class AdminPage:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.show_admin_home()

    def show_admin_home(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a navigation bar at the top
        nav_frame = ttk.Frame(self.root, bootstyle="secondary")
        nav_frame.pack(side="top", fill="x")

        # Add navigation buttons to the navigation bar
        ttk.Button(
            nav_frame, text="Add User", command=self.add_user, bootstyle=PRIMARY
        ).pack(side="left", padx=10, pady=5)
        ttk.Button(
            nav_frame, text="Monthly Bills", command=self.bills, bootstyle=INFO
        ).pack(side="left", padx=10, pady=5)
        ttk.Button(
            nav_frame,
            text="Track Expense",
            command=self.track_expense,
            bootstyle=SUCCESS,
        ).pack(side="left", padx=10, pady=5)
        ttk.Button(
            nav_frame,
            text="Track Earnings",
            command=self.track_earnings,
            bootstyle=SUCCESS,
        ).pack(side="left", padx=10, pady=5)
        ttk.Button(
            nav_frame, text="Logout", command=self.on_logout, bootstyle=DANGER
        ).pack(side="right", padx=10, pady=5)

        # Welcome message frame
        welcome_frame = ttk.Frame(self.root)
        welcome_frame.pack(fill="x", pady=5)
        welcome_message = f"Welcome to CashTrack, {self.username}"
        ttk.Label(
            welcome_frame, text=welcome_message, font=("Arial", 12), anchor="center"
        ).pack()

        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, pady=10)

        # Left frame for total user-wise expense list
        self.left_frame = ttk.Frame(
            self.content_frame, width=200, bootstyle="secondary"
        )
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Right frame for dynamic content
        self.right_frame = ttk.Frame(self.content_frame, bootstyle="light")
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Show user-wise expense list on the left frame and default content on the right
        self.show_user_expense_list()
        self.show_default_content()

    def show_user_expense_list(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Title for the expense list
        ttk.Label(
            self.left_frame,
            text="User-wise Expenses:",
            bootstyle="secondary-inverse",
            font=("Arial", 10, "bold"),
        ).pack(anchor="w", padx=10, pady=5)

        # Get current month and year for filtering
        current_month = datetime.now().month
        current_year = datetime.now().year

        all_spendings = SpendingsManager.get_all_spendings()
        for user, spendings in all_spendings.items():
            if user != "admin":  # Skip the admin user
                # Filter out the spending entries that are for the current month and year
                monthly_spendings = [
                    entry
                    for entry in spendings
                    if datetime.strptime(entry["date"], "%Y-%m-%d").month
                    == current_month
                    and datetime.strptime(entry["date"], "%Y-%m-%d").year
                    == current_year
                ]

                # Only display users with spendings for the current month
                if monthly_spendings:
                    total_expense = sum(entry["amount"] for entry in monthly_spendings)
                    ttk.Label(
                        self.left_frame,
                        text=f"{user}: Total Expense for {current_month}/{current_year}: {total_expense}",
                        font=("Arial", 10, "bold"),
                    ).pack(anchor="w", padx=10, pady=2)

    def show_default_content(self):
        self.clear_content(self.right_frame)
        ttk.Label(
            self.right_frame, text="Welcome to Admin Panel", font=("Arial", 12, "bold")
        ).pack(pady=10)

    def add_user(self):
        self.clear_content(self.right_frame)
        ttk.Label(self.right_frame, text="Add User", font=("Arial", 12, "bold")).pack(
            pady=10
        )

        ttk.Label(self.right_frame, text="Username").pack()
        username_entry = ttk.Entry(self.right_frame)
        username_entry.pack()

        ttk.Label(self.right_frame, text="Password").pack()
        password_entry = ttk.Entry(self.right_frame, show="*")
        password_entry.pack()

        def on_toggle():
            if role.get():
                role.set("admin")
            else:
                role.set("user")

        role = ttk.StringVar(value="user")
        checkbutton = ttk.Checkbutton(
            self.right_frame,
            text="admin",
            variable=role,
            onvalue="admin",
            offvalue="user",
            command=on_toggle,
        )
        checkbutton.pack()

        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            is_admin = role.get()

            if username and password:
                credentials = self.load_credentials()
                credentials[username] = {
                    "password": password,
                    "role": is_admin,
                    "expense_limit": 0.0,
                }
                self.save_credentials(credentials)
                ttk.Label(
                    self.right_frame,
                    text="User added successfully!",
                    bootstyle="success",
                ).pack(pady=5)
                self.show_user_expense_list()  # Refresh user list on left frame
                username_entry.delete(0, ttk.END)
                password_entry.delete(0, ttk.END)
            else:
                messagebox.showerror(
                    "Input Error", "Username and password cannot be empty."
                )

        ttk.Button(
            self.right_frame, text="Save User", command=save_user, bootstyle=SUCCESS
        ).pack(pady=10)

    def bills(self):
        self.clear_content(self.right_frame)

        ttk.Label(
            self.right_frame, text="Add Monthly Bill", font=("Arial", 12, "bold")
        ).pack(pady=10)

        ttk.Label(self.right_frame, text="Bill Name").pack()
        bill_name_entry = ttk.Entry(self.right_frame)
        bill_name_entry.pack()

        ttk.Label(self.right_frame, text="Amount").pack()
        amount_entry = ttk.Entry(self.right_frame)
        amount_entry.pack()

        def distribute_bill():
            try:
                # Validate inputs
                bill_name = bill_name_entry.get().strip()
                if not bill_name:
                    raise ValueError("Bill name cannot be empty.")

                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be greater than zero.")

                # Load users and create checkboxes
                credentials = self.load_credentials()
                user_list = [
                    user for user, data in credentials.items() if data["role"] == "user"
                ]

                if not user_list:
                    raise ValueError("No eligible users to distribute the bill.")

                # Create a new Toplevel window
                distribution_window = ttk.Toplevel(self.root)
                distribution_window.title("Distribute Bill")
                distribution_window.geometry("400x400")

                # Add instructions and checkboxes to the new window
                ttk.Label(
                    distribution_window,
                    text=f"Distribute '{bill_name}' (${amount}) among users:",
                    font=("Arial", 10, "bold")
                ).pack(pady=10)

                user_checkbuttons = {}
                for user in user_list:
                    user_var = ttk.BooleanVar()
                    ttk.Checkbutton(
                        distribution_window, text=user, variable=user_var
                    ).pack(anchor="center", padx=10, pady=2)
                    user_checkbuttons[user] = user_var

                # Confirm distribution function
                def confirm_distribution():
                    selected_users = [
                        user for user, var in user_checkbuttons.items() if var.get()
                    ]

                    if not selected_users:
                        messagebox.showerror("Selection Error", "No users selected.")
                        return

                    split_amount = amount / len(selected_users)
                    for user in selected_users:
                        SpendingsManager.add_spending(
                            user,
                            split_amount,
                            f"Monthly Bill: {bill_name}",
                            datetime.now().strftime("%Y-%m-%d"),
                            "Bills",
                        )

                    messagebox.showinfo("Success", "Bill distributed successfully!")
                    distribution_window.destroy()  # Close the new window

                # Confirm button in the new window
                ttk.Button(
                    distribution_window,
                    text="Confirm Distribution",
                    command=confirm_distribution,
                    bootstyle=SUCCESS,
                ).pack(pady=20)

            except ValueError as e:
                messagebox.showerror("Input Error", str(e))


        ttk.Button(
            self.right_frame,
            text="Distribute Bill",
            command=distribute_bill,
            bootstyle=INFO,
        ).pack(pady=10)

    def track_expense(self):
        self.clear_content(self.right_frame)
        ttk.Label(
            self.right_frame, text="Track Expense", font=("Arial", 12, "bold")
        ).pack(pady=10)

        def show_user_expenses(username):
            # Create a new window for displaying expenses
            expense_window = ttk.Toplevel(self.right_frame)
            expense_window.title(f"Expenses for {username}")
            expense_window.geometry("400x300")

            # Add a Canvas and Scrollbar for scrolling capability
            canvas = ttk.Canvas(expense_window)
            scroll_y = ttk.Scrollbar(
                expense_window, orient="vertical", command=canvas.yview
            )

            # Frame inside the Canvas for holding the list of expenses
            frame = ttk.Frame(canvas)

            # Configure the Canvas
            canvas.create_window((0, 0), window=frame, anchor="nw")
            canvas.configure(yscrollcommand=scroll_y.set)

            # Populate expenses in the frame
            expenses = SpendingsManager.get_user_spendings(username)
            ttk.Label(
                frame, text=f"Expenses for {username}", font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=5)
            for entry in expenses:
                expense_text = f"Amount: {entry['amount']}, Date: {entry['date']}, Category: {entry['category']},\ndescription: {entry['description']}"
                ttk.Label(frame, text=expense_text, anchor="w").pack(
                    fill="x", padx=10, pady=2
                )

            # Pack Canvas and Scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scroll_y.pack(side="right", fill="y")

            # Update the scrollable region
            frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        credentials = self.load_credentials()
        for user, info in credentials.items():
            if info.get("role") == "user":
                ttk.Button(
                    self.right_frame,
                    text=user,
                    command=lambda u=user: show_user_expenses(u),
                    bootstyle="info-outline",
                ).pack(anchor="center", padx=10, pady=5)

    def track_earnings(self):
        self.clear_content(self.right_frame)
        ttk.Label(
            self.right_frame, text="Track Earnings", font=("Arial", 12, "bold")
        ).pack(pady=10)

        def show_user_earnings(username):
            # Create a new window for displaying earnings
            earnings_window = ttk.Toplevel(self.right_frame)
            earnings_window.title(f"Earnings for {username}")
            earnings_window.geometry("400x300")

            # Add a Canvas and Scrollbar for scrolling capability
            canvas = ttk.Canvas(earnings_window)
            scroll_y = ttk.Scrollbar(
                earnings_window, orient="vertical", command=canvas.yview
            )

            # Frame inside the Canvas for holding the list of earnings
            frame = ttk.Frame(canvas)

            # Configure the Canvas
            canvas.create_window((0, 0), window=frame, anchor="nw")
            canvas.configure(yscrollcommand=scroll_y.set)

            # Populate earnings in the frame
            earnings = EarningsManager.get_user_earnings(username)
            ttk.Label(
                frame, text=f"Earnings for {username}", font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=5)
            for entry in earnings:
                earning_text = f"Amount: {entry['amount']}, Date: {entry['date']}, Description: {entry['description']}"
                ttk.Label(frame, text=earning_text, anchor="w").pack(
                    fill="x", padx=10, pady=2
                )

            # Pack Canvas and Scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scroll_y.pack(side="right", fill="y")

            # Update the scrollable region
            frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        credentials = self.load_credentials()
        for user, info in credentials.items():
            if info.get("role") == "user":
                ttk.Button(
                    self.right_frame,
                    text=user,
                    command=lambda u=user: show_user_earnings(u),
                    bootstyle="info-outline",
                ).pack(anchor="center", padx=10, pady=5)

    def clear_content(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def load_credentials(self):
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, "r") as file:
                return json.load(file)
        else:
            return {}

    def save_credentials(self, credentials):
        with open(CREDENTIALS_FILE, "w") as file:
            json.dump(credentials, file, indent=4)


