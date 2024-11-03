import matplotlib.pyplot as plt
from datetime import datetime
from spendings import SpendingsManager
from earnings import EarningsManager

class ExpenseAnalysis:
    @staticmethod
    def analyze_expenses(username, period):

        expenses = SpendingsManager.get_user_spendings(username)
        report = {}

        now = datetime.now()
        if period == "Monthly":
            start_date = now.replace(day=1)
        elif period == "Quarterly":
            month = (now.month - 1) // 3 * 3 + 1
            start_date = now.replace(month=month, day=1)
        elif period == "Annually":
            start_date = now.replace(month=1, day=1)
        else:
            raise ValueError("Invalid period selected.")

        total = 0
        category_totals = {}
        for expense in expenses:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            if expense_date >= start_date:
                amount = expense["amount"]
                category = expense["category"]
                total += amount
                category_totals[category] = category_totals.get(category, 0) + amount

        report["total"] = total
        report["category_totals"] = category_totals
        report["period"] = period
        return report

    @staticmethod
    def generate_expense_chart(username, period):
        # Analyze expenses for the given period
        report = ExpenseAnalysis.analyze_expenses(username, period)

        categories = list(report["category_totals"].keys())
        amounts = list(report["category_totals"].values())

        # Generate the bar chart
        plt.figure(figsize=(6, 4))
        plt.bar(categories, amounts, color='skyblue')
        plt.xlabel("Categories")
        plt.ylabel("Amount Spent ($)")
        plt.title(f"{period} Expense Breakdown for {username}")

        # Save the plot as an image
        chart_path = "expense_chart.png"
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()

        return chart_path

    @staticmethod
    def calculate_monthly_balance(username):
        # Calculate total earnings and spendings for the current month
        current_month = datetime.now().strftime("%Y-%m")
        total_earnings = sum(
            e["amount"] for e in EarningsManager.get_user_earnings(username)
            if e["date"].startswith(current_month)
        )
        total_spendings = sum(
            s["amount"] for s in SpendingsManager.get_user_spendings(username)
            if s["date"].startswith(current_month)
        )
        return total_earnings - total_spendings

    @staticmethod
    def get_monthly_spending(username):
        # Get all spendings for the user
        spendings = SpendingsManager.get_user_spendings(username)

        # Get current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Calculate total spending for the current month
        monthly_spent = sum(
            entry['amount'] for entry in spendings
            if datetime.strptime(entry['date'], "%Y-%m-%d").month == current_month and
            datetime.strptime(entry['date'], "%Y-%m-%d").year == current_year
        )

        return monthly_spent