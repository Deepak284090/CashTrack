import tkinter as tk
from tkinter import messagebox


class UserPage:
    def __init__(self, root, on_logout):
        self.root = root
        self.on_logout = on_logout
        self.show_user_home()

    def show_user_home(self):
        tk.Label(self.root, text="User Home Page").pack(pady=10)
        tk.Label(self.root, text="Welcome, username, your spendings:").pack(pady=5)

        tk.Button(self.root, text="Add Expense", command=self.add_expense).pack(pady=5)
        tk.Button(self.root, text="Delete Expense", command=self.delete_expense).pack(pady=5)
        tk.Button(self.root, text="Analyze Expense", command=self.analyze_expense).pack(pady=5)
        tk.Button(self.root, text="Set Expense Limit", command=self.set_expense_limit).pack(pady=5)

        tk.Label(self.root, text="You have xxx amount left this month").pack(pady=5)
        tk.Label(self.root, text="You can spend: xxx").pack(pady=5)

        tk.Button(self.root, text="Logout", command=self.on_logout).pack(pady=10)

    def add_expense(self):
        messagebox.showinfo("Add Expense", "Add Expense functionality goes here.")

    def delete_expense(self):
        messagebox.showinfo("Delete Expense", "Delete Expense functionality goes here.")

    def analyze_expense(self):
        messagebox.showinfo("Analyze Expense", "Analyze Expense functionality goes here.")

    def set_expense_limit(self):
        messagebox.showinfo("Set Expense Limit", "Set Expense Limit functionality goes here.")
