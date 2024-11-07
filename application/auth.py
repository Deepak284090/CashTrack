import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

CREDENTIALS_FILE = "credentials.json"

class Auth:
    def __init__(self, root, on_admin_login, on_user_login):
        self.root = root
        self.on_admin_login = on_admin_login
        self.on_user_login = on_user_login
        self.credentials = self.load_credentials()

    def load_credentials(self):
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, "r") as file:
                return json.load(file)
        else:
            return {}

    def save_credentials(self):
        with open(CREDENTIALS_FILE, "w") as file:
            json.dump(self.credentials, file, indent=4)

    def set_expense_limit(self, username, limit):
        if username in self.credentials:
            self.credentials[username]["expense_limit"] = limit
            self.save_credentials()
        else:
            raise ValueError("User does not exist.")

    def get_expense_limit(self, username):
        return self.credentials.get(username, {}).get("expense_limit")

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = ttk.Frame(self.root, padding=20)
        login_frame.pack(pady=20)

        # Title label
        title_label = ttk.Label(login_frame, text="Welcome to Cash Track", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 15))

        # User role selection with radio buttons
        self.user_role = tk.StringVar(value="user")
        role_frame = ttk.Frame(login_frame)
        role_frame.pack(pady=10)
        ttk.Radiobutton(role_frame, text="Admin", variable=self.user_role, value="admin").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(role_frame, text="User", variable=self.user_role, value="user").grid(row=0, column=1, padx=5)

        # Username and password entry fields
        ttk.Label(login_frame, text="Username:", font=("Arial", 10)).pack(anchor="w", pady=(10, 2))
        self.username_entry = ttk.Entry(login_frame, width=25)
        self.username_entry.pack(pady=(0, 5))

        ttk.Label(login_frame, text="Password:", font=("Arial", 10)).pack(anchor="w", pady=(10, 2))
        self.password_entry = ttk.Entry(login_frame, show="*", width=25)
        self.password_entry.pack(pady=(0, 5))

        # Login button
        login_button = ttk.Button(login_frame, text="Login", command=self.login, style="Accent.TButton")
        login_button.pack(pady=15)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.credentials:
            if self.credentials[username]["password"] == password:
                if self.credentials[username]["role"] == "admin" and self.user_role.get() == "admin":
                    self.on_admin_login(username)
                elif self.credentials[username]["role"] == "user" and self.user_role.get() == "user":
                    self.on_user_login(username)
                else:
                    messagebox.showerror("Login Failed", "Incorrect role selected.")
            else:
                messagebox.showerror("Login Failed", "Invalid Password.")
        else:
            messagebox.showerror("Login Failed", "User does not exist.")
