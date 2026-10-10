import sqlite3
from datetime import datetime, date

DB_NAME = "expense_tracker.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn


def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            source TEXT,
            category TEXT,
            description TEXT,
            date TEXT
        )
    """)
    conn.commit()


def get_amount():
    while True:
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number.")


def get_type():
    while True:
        t = input("Enter the type (expense/income): ").strip().lower()
        if t in ("income", "expense"):
            return t
        print("Invalid type. Please enter expense or income.")


def get_required_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def add_transaction(conn):
    amount = get_amount()
    t_type = get_type()

    source = None
    category = None
    if t_type == "income":
        source = get_required_text("Enter income source: ")
    else:
        category = get_required_text("Enter expense category: ")
    description = get_required_text("Enter description: ")

    conn.execute(
        """
        INSERT INTO transactions (amount, type, source, category, description, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (amount, t_type, source, category, description, date.today().isoformat()),
    )
    conn.commit()


def ask_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "n"):
            return choice
        print("Please enter y or n.")

def format_date(value):
    if not value:
        return "Not available"

    try:
        return datetime.strptime(
            value, "%Y-%m-%d"
        ).strftime("%d-%m-%Y")
    except (ValueError, TypeError):
        return "Invalid date"


def print_transaction_details(row):
    print(f"Transaction ID : {row['id']}")
    print(f"Type           : {row['type'].upper()}")
    print(f"Amount         : ₹{row['amount']:,.2f}")

    if row["type"] == "income":
        print(f"Source         : {row['source'] or 'N/A'}")
    else:
        print(f"Category       : {row['category'] or 'N/A'}")

    print(f"Description    : {row['description'] or 'N/A'}")
    print(f"Date           : {format_date(row['date'])}")


def print_report(conn):
    rows = conn.execute(
        "SELECT * FROM transactions ORDER BY id DESC"
    ).fetchall()

    print("\n" + "=" * 55)
    print("                 TRANSACTION HISTORY")
    print("=" * 55)

    if not rows:
        print("No transactions found.")
        return

    for row in rows:
     print_transaction_details(row)
     print("-" * 55)

    print(f"\nTotal transactions: {len(rows)}")



def print_totals(conn):
    total_income = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'income'
        """
    ).fetchone()[0]

    total_expense = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'expense'
        """
    ).fetchone()[0]

    balance = total_income - total_expense

    print("\n" + "=" * 42)
    print("          FINANCIAL SUMMARY")
    print("=" * 42)
    print(f"Total Income   : ₹{total_income:,.2f}")
    print(f"Total Expense  : ₹{total_expense:,.2f}")
    print("-" * 42)
    print(f"Net Balance    : ₹{balance:,.2f}")
    print("=" * 42)

    if total_income == 0 and total_expense == 0:
        print("No financial activity recorded yet.")
    elif balance < 0:
        print("Warning: Your expenses exceed your income.")
    else:
        print("Summary generated successfully.")



def update_transaction(conn):
    input_id = input("Enter transaction ID to update: ").strip()

    if not input_id.isdigit() or int(input_id) <= 0:
        print("Invalid ID. Enter a positive numeric ID.")
        return

    input_id = int(input_id)

    row = conn.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (input_id,)
    ).fetchone()

    if row is None:
        print(f"No transaction found with ID {input_id}.")
        return

    print("\nWhat do you want to update?")
    print("1. Amount")
    print("2. Description")
    print("3. Category / Income Source")

    choice = input("Enter your choice: ").strip()

    try:
        if choice == "1":
            new_amount = float(input("Enter new amount: ").strip())

            if new_amount <= 0:
                print("Amount must be greater than zero.")
                return

            conn.execute(
                "UPDATE transactions SET amount = ? WHERE id = ?",
                (new_amount, input_id)
            )

        elif choice == "2":
            new_description = input(
                "Enter new description: "
            ).strip()

            conn.execute(
                "UPDATE transactions SET description = ? WHERE id = ?",
                (new_description, input_id)
            )

        elif choice == "3":
            if row["type"] == "income":
                new_source = input("Enter new income source: ").strip()

                conn.execute(
                    "UPDATE transactions SET source = ? WHERE id = ?",
                    (new_source, input_id)
                )
            else:
                new_category = input("Enter new expense category: ").strip()

                conn.execute(
                    "UPDATE transactions SET category = ? WHERE id = ?",
                    (new_category, input_id)
                )

        else:
            print("Invalid choice. Select 1, 2, or 3.")
            return

        conn.commit()
        print(f"Transaction ID {input_id} updated successfully.")

    except ValueError:
        print("Invalid amount. Please enter a valid number.")

    except sqlite3.Error as error:
        conn.rollback()
        print(f"Database error: {error}")



def delete_transaction(conn):
    input_id = input("Enter transaction ID to delete: ").strip()

    if not input_id.isdigit() or int(input_id) <= 0:
        print("Invalid ID. Enter a positive numeric ID.")
        return

    input_id = int(input_id)

    row = conn.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (input_id,)
    ).fetchone()

    if row is None:
        print(f"No transaction found with ID {input_id}.")
        return

    # Display the transaction before deletion
    print("\nTransaction details")
    print("-" * 35)
    print_transaction_details(row)
    print("-" * 35)
    confirm = ask_yes_no(
        "Are you sure you want to delete this transaction? (y/n): "
    )

    if confirm == "n":
        print("Deletion cancelled.")
        return

    try:
        conn.execute(
            "DELETE FROM transactions WHERE id = ?",
            (input_id,)
        )
        conn.commit()
        print(f"Transaction ID {input_id} deleted successfully.")

    except sqlite3.Error as error:
        conn.rollback()
        print(f"Database error: {error}")


def filter_transactions(conn):
    print("\n--- Filter Transactions ---")
    print("1. Show Income")
    print("2. Show Expenses")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        transaction_type = "income"
    elif choice == "2":
        transaction_type = "expense"
    else:
        print("Invalid choice. Please select 1 or 2.")
        return

    rows = conn.execute(
        """
        SELECT * FROM transactions
        WHERE type = ?
        ORDER BY id DESC
        """,
        (transaction_type,)
    ).fetchall()

    print(f"\n--- {transaction_type.upper()} TRANSACTIONS ---")

    if not rows:
        print(f"No {transaction_type} transactions found.")
        return

    for row in rows:
        print(f"\nID          : {row['id']}")
        print(f"Type        : {row['type'].upper()}")
        print(f"Amount      : ₹{row['amount']:,.2f}")

        if row["type"] == "income":
            print(f"Source      : {row['source'] or 'N/A'}")
        else:
            print(f"Category    : {row['category'] or 'N/A'}")

        print(f"Description : {row['description'] or 'N/A'}")
        print(f"Date        : {format_date(row['date'])}")
        print("-" * 40)

    print(f"\nTotal matching transactions: {len(rows)}")

def show_menu():
    print("\n========================================")
    print("           EXPENSE TRACKER")
    print("========================================")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Update Transaction")
    print("4. Delete Transaction")
    print("5. View Financial Summary")
    print("6. Filter Transactions")
    print("7. Exit")
    print("========================================")


def reset_transaction_ids(conn):
    count = conn.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    if count == 0:
        conn.execute(
            "DELETE FROM sqlite_sequence WHERE name = 'transactions'"
        )
        conn.commit()


def main():
    conn = get_connection()

    try:
        create_table(conn)
        reset_transaction_ids(conn)
        while True:
            show_menu()

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                add_transaction(conn)

            elif choice == "2":
                print_report(conn)

            elif choice == "3":
                update_transaction(conn)

            elif choice == "4":
                delete_transaction(conn)

            elif choice == "5":
                print_totals(conn)

            elif choice == "6":
                filter_transactions(conn)

            elif choice == "7":
                print("Thank you for using Expense Tracker.")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 7.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()


