# Personal Finance Tracker

A web-based personal finance tracker that helps you manage expenses, income, and view spending analytics with a beautiful dashboard.

## Features

- 🌐 **Web Interface** - Clean, responsive web dashboard
- 💰 **Transaction Management** - Add income and expense transactions
- 📊 **Visual Analytics** - Interactive charts and graphs
- 📈 **Financial Summary** - Balance, savings rate, category breakdown
- 📱 **Mobile Friendly** - Works on all devices
- 💾 **Data Persistence** - Automatic JSON storage
- ✅ **Input Validation** - Error handling and validation

## Requirements

- Python 3.7+
- Flask 2.3.3

## How to Run

### Option 1: Web Application (Recommended)

1. **Install Flask:**

   ```bash
   pip install Flask==2.3.3
   ```

   Or install from requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the web application:**

   ```bash
   python app.py
   ```

3. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

### Option 2: Command Line Version

```bash
python main.py
```

## Usage

The application provides an interactive menu with the following options:

1. **Add Transaction** - Record income or expenses
2. **View Transactions** - See all recorded transactions
3. **View Summary** - Get spending breakdown by category
4. **Generate Report** - View detailed analytics
5. **Exit** - Save and quit

## Project Structure

```
finance_tracker/
├── main.py              # Main application entry point
├── transaction.py       # Transaction class definition
├── finance_tracker.py   # Core tracker functionality
├── utils.py            # Utility functions
├── data/               # Data storage directory
│   └── transactions.json
└── README.md
```

## Example Usage

```
=== Personal Finance Tracker ===
1. Add Transaction
2. View Transactions
3. View Summary
4. Generate Report
5. Exit

Enter your choice (1-5): 1
Enter amount: 50.00
Enter description: Grocery shopping
Enter category: Food
Is this income? (y/n): n
Transaction added successfully!
```
