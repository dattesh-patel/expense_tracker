# Expense Tracker

A command-line expense tracking application built with Python and SQLite to manage income and expenses, maintain transaction history, and calculate financial summaries.

## Features

- Add income and expense transactions
- View transaction history with unique transaction IDs
- Update transaction amounts, descriptions, and categories or income sources
- Delete transactions with confirmation
- Filter transactions by income or expense type
- Calculate total income, total expenses, and net balance
- Store transactions persistently using SQLite
- Validate user input and handle invalid entries
- Display transaction dates in `DD-MM-YYYY` format

## Technologies Used

- **Python 3** — Application logic and user interaction
- **SQLite** — Persistent local database
- **sqlite3** — Python database interface

## Requirements

- Python 3.10 or later recommended
- No third-party packages required for the current application

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/dattesh-patel/expense_tracker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd expense-tracker
   ```

3. Run the application:

   ```bash
   python expense_tracker.py
   ```

The application creates the SQLite database and transactions table automatically when needed.

## Usage

Launch the application and select an option from the main menu to add, view, update, delete, or filter transactions, or to view the financial summary.

## Data Storage

Transactions are stored locally in `expense_tracker.db`. Keep a backup of this file if you want to preserve your records.

## Future Improvements

- Automated tests using `pytest`
- Category-wise spending analysis
- CSV export
- Improved reporting and application structure

## Author

Dattesh Patel,https://github.com/dattesh-patel