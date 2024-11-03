import tkinter as tk
from tkinter import messagebox
import json
import os


CREDENTIALS_FILE = "credentials.json"

class AdminPage:
    def __init__(self, root, on_logout):
        self.root = root
        self.on_logout = on_logout
        self.show_admin_home()

    def show_admin_home(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a navigation bar at the top
        nav_frame = tk.Frame(self.root, bg="lightgray")
        nav_frame.pack(side="top", fill="x")

        # Add navigation buttons to the navigation bar
        tk.Button(nav_frame, text="Add User", command=self.add_user).pack(side="left", padx=10, pady=5)
        tk.Button(nav_frame, text="Set Admin", command=self.set_admin).pack(side="left", padx=10, pady=5)
        tk.Button(nav_frame, text="Track Expense", command=self.track_expense).pack(side="left", padx=10, pady=5)
        tk.Button(nav_frame, text="Update User Details", command=self.update_user).pack(side="left", padx=10, pady=5)

        tk.Button(nav_frame, text="Logout", command=self.on_logout).pack(side="right", padx=10, pady=5)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, pady=20)

        self.show_default_content()

    def show_default_content(self):
        tk.Label(self.content_frame, text="Welcome to CashTrack", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.content_frame, text="A solution to money management needs of a nuclear family.",
                 font=("Arial", 10)).pack(pady=5)

    def add_user(self):
        self.clear_content()

        tk.Label(self.content_frame, text="Add or Update User", font=("Arial", 12)).pack(pady=10)

        tk.Label(self.content_frame, text="Username").pack()
        username_entry = tk.Entry(self.content_frame)
        username_entry.pack()

        tk.Label(self.content_frame, text="Password").pack()
        password_entry = tk.Entry(self.content_frame, show="*")
        password_entry.pack()

        tk.Label(self.content_frame, text="Role (admin/user)").pack()
        role_entry = tk.Entry(self.content_frame)
        role_entry.pack()

        tk.Button(self.content_frame, text="Save User",
                  command=lambda: self.save_user(username_entry.get(), password_entry.get(), role_entry.get())).pack(
            pady=10)

    def save_user(self, username, password, role):
        credentials = self.load_credentials()

        if role not in ["admin", "user"]:
            tk.messagebox.showerror("Error", "Role must be 'admin' or 'user'")
            return
        credentials[username] = {
            "password": password,
            "role": role
        }

        self.save_credentials(credentials)
        tk.messagebox.showinfo("Success", f"User '{username}' added/updated successfully.")

    def set_admin(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Set Admin functionality goes here.", font=("Arial", 12)).pack()

    def track_expense(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Track Expense functionality goes here.", font=("Arial", 12)).pack()

    def update_user(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Update User Details functionality goes here.", font=("Arial", 12)).pack()

    def load_credentials(self):
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, "r") as file:
                return json.load(file)
        else:
            return {}

    def save_credentials(self, credentials):
        with open(CREDENTIALS_FILE, "w") as file:
            json.dump(credentials, file, indent=4)

    def clear_content(self):
        # Clear the content frame before loading new content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
