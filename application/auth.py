import tkinter as tk
from tkinter import messagebox
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
        # Set the expense limit for the user
        if username in self.credentials:
            self.credentials[username]["expense_limit"] = limit
            self.save_credentials()  # Save updated credentials back to the file
        else:
            raise ValueError("User does not exist.")

    def get_expense_limit(self, username):
        # Return the expense limit for the user
        return self.credentials.get(username, {}).get("expense_limit")

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=20)

        tk.Label(login_frame, text="Welcome to Cash Track", font=("Arial", 14)).pack(pady=10)

        # Radio buttons for selecting Admin or User
        self.user_role = tk.StringVar(value="user")
        role_frame = tk.Frame(login_frame)
        role_frame.pack(pady=5)
        tk.Radiobutton(role_frame, text="Admin", variable=self.user_role, value="admin").grid(row=0, column=0, padx=5)
        tk.Radiobutton(role_frame, text="User", variable=self.user_role, value="user").grid(row=0, column=1, padx=5)

        tk.Label(login_frame, text="User Name").pack(pady=5)
        self.username_entry = tk.Entry(login_frame)
        self.username_entry.pack()

        tk.Label(login_frame, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.pack()

        tk.Button(login_frame, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.credentials:
            if self.credentials[username]["password"] == password:
                if self.credentials[username]["role"] == "admin" and self.user_role.get() == "admin":
                    self.on_admin_login(username)  # Pass the username to admin login
                elif self.credentials[username]["role"] == "user" and self.user_role.get() == "user":
                    self.on_user_login(username)  # Pass the username to user login
                else:
                    messagebox.showerror("Login Failed", "Incorrect role selected.")
            else:
                messagebox.showerror("Login Failed", "Invalid Password.")
        else:
            messagebox.showerror("Login Failed", "User does not exist.")
