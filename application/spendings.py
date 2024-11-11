import json
from datetime import datetime
from tkinter import messagebox

SPENDINGS_FILE = "spendings.json"


class SpendingsManager:
    @staticmethod
    def add_spending(username, amount, description, date, category):
        try:
            with open(SPENDINGS_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Create entry with amount, description, date, and category
        entry = {
            "amount": amount,
            "description": description,
            "date": date,
            "category": category,
        }

        # Append to user data
        user_data = data.setdefault(username, [])
        user_data.append(entry)
        data[username] = user_data

        with open(SPENDINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def get_user_spendings(username):
        try:
            with open(SPENDINGS_FILE, "r") as f:
                data = json.load(f)
            return data.get(username, [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def get_all_spendings():
        try:
            with open(SPENDINGS_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def set_expense_limit(username, limit):
        try:
            with open(SPENDINGS_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Ensure user data is initialized
        user_data = data.setdefault(username, {})
        user_data["limit"] = limit
        data[username] = user_data

        with open(SPENDINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def get_expense_limit(username):
        try:
            with open(SPENDINGS_FILE, "r") as f:
                data = json.load(f)
            user_data = data.get(username, {})
            return user_data.get("limit", None)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def submit_monthly_bill(self, bill_name, total_amount, selected_users):
        try:
            amount_per_user = float(total_amount) / sum(
                var.get() for var in selected_users.values()
            )
        except ZeroDivisionError:
            messagebox.showerror("Error", "No users selected.")
            return

        for user, var in selected_users.items():
            if var.get():  # If user is selected
                SpendingsManager.add_spending(
                    username=user,
                    amount=amount_per_user,
                    description=bill_name,
                    date=f"{datetime.now().year}-{datetime.now().month:02d}-01",
                    category="Monthly Bill",
                )
        messagebox.showinfo("Success", "Monthly bill distributed successfully.")
