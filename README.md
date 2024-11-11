# Cash Track

Cash Track is a comprehensive financial management application designed for nuclear families with multiple earners. This platform allows family members to efficiently track their individual earnings and expenses while managing shared financial responsibilities, such as monthly bills and recurring costs. By providing tools for real-time financial tracking, expense analysis, and detailed reporting, Cash Track aims to simplify financial management for households with multiple contributors.

## Introduction

In today’s fast-paced world, managing household finances can be challenging, especially for nuclear families with several income sources. Cash Track helps address common pain points by providing an automated system to track earnings, expenses, and financial transactions. It ensures that all family members contribute fairly to shared expenses, and allows for transparent and real-time financial management.

## Objectives

- **Track individual earnings and expenses**: Each family member can securely manage their own finances.
- **Manage shared expenses**: Admins can configure recurring shared expenses (e.g., rent, utilities) and distribute them among selected family members.
- **Expense limits**: Users and admins can set limits for personal expenses, with notifications if the limit is exceeded.
- **Expense reports**: Visualize spending patterns and generate reports for detailed analysis.
- **Role-based access**: Admins have the ability to manage settings and configure shared responsibilities, while users can only access their own financial data.

## Scope

### Target Users:
The primary focus of this project is on nuclear families with multiple earners. It caters to households where more than one individual contributes to the family income and needs help managing finances efficiently.

### Functional Scope:
1. **Earnings and Expenses Management**: Track both individual and shared finances.
2. **Recurring Expenses**: Automate the distribution of recurring household bills.
3. **Expense Limits**: Set and monitor spending limits to avoid overspending.
4. **Reporting and Analysis**: Generate detailed reports and visual charts to track spending patterns and financial health.

### Exclusions:
The project focuses solely on household financial management, excluding advanced features like investment tracking, tax filing, or complex budgeting.

## Application Tools

### Programming Language: Python
Python is used for its readability, ease of use, and strong support for libraries related to data management, GUI creation, and visualization.

### IDE: PyCharm
PyCharm is used as the primary IDE, providing features such as intelligent code completion, error checking, and version control integration.

### Libraries and Packages:
- **Tkinter**: For creating the graphical user interface.
- **ttkbootstrap**: Enhances Tkinter with modern themes and styling options.
- **Matplotlib**: For generating visual reports and charts.
- **Datetime**: For managing and manipulating date-related information.
- **JSON**: For data storage in a lightweight, human-readable format.

### Version Control: Git
Git is used for version control, ensuring efficient tracking of changes and collaboration. The project is hosted on GitHub: [GitHub Repository](https://github.com/Deepak284090/CashTrack.git)

### File Management:
JSON files are used for storing user data, earnings, expenses, and other settings. This simple, file-based approach eliminates the need for a complex database system.

## Project Design

### Core Components:

1. **Authentication (Auth Class)**:
   - Manages login and role-based access control (user and admin).
   - Functions: load_credentials(), login(), set_expense_limit().

2. **Earnings Management (EarningsManager Class)**:
   - Manages individual earnings.
   - Functions: add_earning(), get_user_earnings(), update_recurring_earnings().

3. **Expense Management (SpendingsManager Class)**:
   - Manages individual and shared expenses.
   - Functions: add_spending(), get_user_spendings(), set_expense_limit(), submit_monthly_bill().

4. **Expense Analysis (ExpenseAnalysis Class)**:
   - Analyzes and reports user expenses.
   - Functions: analyze_expenses(), generate_expense_chart(), calculate_monthly_balance().

5. **User Interface (CashTrackApp Class)**:
   - Manages the main application interface.
   - Functions: show_login_screen(), show_admin_home(), show_user_home(), clear_screen().

### Interaction:
- **User Authentication**: The Auth class validates credentials and redirects users to the appropriate interface (admin or user).
- **Financial Management**: EarningsManager and SpendingsManager handle all data related to earnings and expenses.
- **Reports and Visualization**: The ExpenseAnalysis class generates reports and visualizes financial data for better decision-making.
- **User Navigation**: CashTrackApp coordinates the flow between different components and ensures a smooth user experience.

## Getting Started

### Prerequisites:
To run this project, you need to have Python 3.x installed on your machine.

### Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/Deepak284090/CashTrack.git
