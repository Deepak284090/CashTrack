import json
from datetime import datetime, timedelta

EARNINGS_FILE = "earnings.json"


class EarningsManager:
    @staticmethod
    def add_earning(username, amount, description, date, recurring=False):
        try:
            with open(EARNINGS_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Create entry with amount, date, description, and recurring flag
        entry = {
            "amount": amount,
            "date": date,
            "description": description,
            "recurring": recurring,
        }

        # Append to user data
        user_data = data.get(username, [])
        user_data.append(entry)
        data[username] = user_data

        # Save back to file
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

    @staticmethod
    def update_recurring_earnings():
        """
        Checks each user's earnings and adds a new entry if any earning
        is set to recur on the same day each month.
        """
        try:
            with open(EARNINGS_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        today = datetime.now().date()

        for username, earnings in data.items():
            for entry in earnings:
                # Check for recurring entries and calculate the next entry date
                if entry.get("recurring"):
                    entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                    while entry_date < today:
                        entry_date += timedelta(
                            days=30
                        )  # Advance by one month (approx.)

                    # Add a new entry if due
                    if entry_date == today:
                        new_entry = entry.copy()
                        new_entry["date"] = today.strftime("%Y-%m-%d")
                        earnings.append(new_entry)

        # Save updated earnings back to file
        with open(EARNINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)
