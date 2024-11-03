import json
from datetime import datetime

SPENDINGS_FILE = "spendings.json"

class SpendingsManager:
    @staticmethod
    def add_spending(username, amount, description, category):
        try:
            with open(SPENDINGS_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Get current date
        date = datetime.now().strftime("%Y-%m-%d")

        # Create entry with amount, description, date, and category
        entry = {
            "amount": amount,
            "description": description,
            "date": date,
            "category": category
        }

        # Append to user data
        user_data = data.get(username, [])
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
