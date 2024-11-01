import tkinter as tk
from tkinter import messagebox


class Auth:
    def __init__(self, root, on_admin_login, on_user_login):
        self.root = root
        self.on_admin_login = on_admin_login
        self.on_user_login = on_user_login

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Cash Track").pack(pady=10)

        tk.Label(self.root, text="User Name:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Admin Login", command=self.admin_login).pack(pady=5)
        tk.Button(self.root, text="User Login", command=self.user_login).pack(pady=5)

    def admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simple check for credentials
        if username == "admin" and password == "admin123":
            self.on_admin_login()
        else:
            messagebox.showerror("Login Failed", "Invalid Admin Credentials")

    def user_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "user" and password == "user123":
            self.on_user_login()
        else:
            messagebox.showerror("Login Failed", "Invalid User Credentials")
