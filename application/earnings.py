import json
from datetime import datetime

EARNINGS_FILE = "earnings.json"

class EarningsManager:
    @staticmethod
    def add_earning(username, amount, description):
        try:
            with open(EARNINGS_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Get current date
        date = datetime.now().strftime("%Y-%m-%d")

        # Create entry with amount, date, and description
        entry = {"amount": amount, "date": date, "description": description}

        # Append to user data
        user_data = data.get(username, [])
        user_data.append(entry)
        data[username] = user_data

        with open(EARNINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def get_user_earnings(username):
        try:
            with open(EARNINGS_FILE, "r") as f:
                data = json.load(f)
            return data.get(username, [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def get_all_earnings():
        try:
            with open(EARNINGS_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
