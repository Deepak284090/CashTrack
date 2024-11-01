import tkinter as tk
from tkinter import messagebox


class AdminPage:
    def __init__(self, root, on_logout):
        self.root = root
        self.on_logout = on_logout
        self.show_admin_home()

    def show_admin_home(self):
        tk.Label(self.root, text="Admin Home Page").pack(pady=10)
        tk.Label(self.root,
                 text="Welcome to CashTrack\nA solution to money management needs of a nuclear family.").pack(pady=10)

        tk.Button(self.root, text="Add User", command=self.add_user).pack(pady=5)
        tk.Button(self.root, text="Set Admin", command=self.set_admin).pack(pady=5)
        tk.Button(self.root, text="Track Expense", command=self.track_expense).pack(pady=5)
        tk.Button(self.root, text="Update User Details", command=self.update_user).pack(pady=5)

        tk.Button(self.root, text="Logout", command=self.on_logout).pack(pady=10)

    def add_user(self):
        messagebox.showinfo("Add User", "Add User functionality goes here.")

    def set_admin(self):
        messagebox.showinfo("Set Admin", "Set Admin functionality goes here.")

    def track_expense(self):
        messagebox.showinfo("Track Expense", "Track Expense functionality goes here.")

    def update_user(self):
        messagebox.showinfo("Update User Details", "Update User functionality goes here.")
