import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it)
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Create table for expenses if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
''')
conn.commit()

def add_expense():
    """Add a new expense to the database"""
    date = input("Enter the date (YYYY-MM-DD): ")
    category = input("Enter the category (e.g., Food, Transport): ")
    amount = float(input("Enter the amount: "))
    description = input("Enter a description (optional): ")

    cursor.execute('''
    INSERT INTO expenses (date, category, amount, description)
    VALUES (?, ?, ?, ?)
    ''', (date, category, amount, description))
    conn.commit()
    print("Expense added successfully!")

def view_expenses():
    """View all expenses stored in the database"""
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()

    if expenses:
        for expense in expenses:
            print(f"ID: {expense[0]} | Date: {expense[1]} | Category: {expense[2]} | Amount: {expense[3]} | Description: {expense[4]}")
    else:
        print("No expenses found.")

def generate_report():
    """Generate a summary report of expenses by category"""
    cursor.execute('''
    SELECT category, SUM(amount) FROM expenses GROUP BY category
    ''')
    report = cursor.fetchall()

    if report:
        print("\nExpense Report by Category:")
        for category, total in report:
            print(f"{category}: ${total:.2f}")
    else:
        print("No expenses to generate a report.")

def delete_expense():
    """Delete an expense by its ID"""
    expense_id = int(input("Enter the expense ID to delete: "))
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    print(f"Expense with ID {expense_id} has been deleted.")

def main():
    """Main menu for the Expense Tracker app"""
    while True:
        print("\nExpense Tracker - Choose an option:")
        print("1. Add a new expense")
        print("2. View all expenses")
        print("3. Generate expense report")
        print("4. Delete an expense")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()

    # Close the database connection
    conn.close()
