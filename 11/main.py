"""
Personal Finance Tracker - Main Application
"""

from datetime import datetime
from finance_tracker import FinanceTracker
from transaction import Transaction
from utils import (
    get_float_input, get_yes_no_input, get_string_input,
    format_currency, clear_screen, pause
)


class FinanceApp:
    """Main application class."""
    
    def __init__(self):
        self.tracker = FinanceTracker()
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*40)
        print("    Personal Finance Tracker")
        print("="*40)
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. View Summary")
        print("4. Generate Report")
        print("5. Exit")
        print("-"*40)
    
    def add_transaction(self):
        """Add a new transaction."""
        print("\n--- Add New Transaction ---")
        
        try:
            amount = get_float_input("Enter amount: $")
            description = get_string_input("Enter description: ")
            category = get_string_input("Enter category: ")
            is_income = get_yes_no_input("Is this income? (y/n): ")
            
            transaction = Transaction(amount, description, category, is_income)
            self.tracker.add_transaction(transaction)
            
            transaction_type = "Income" if is_income else "Expense"
            print(f"\n✓ {transaction_type} of {format_currency(amount)} added successfully!")
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
    
    def view_transactions(self):
        """Display all transactions."""
        transactions = self.tracker.get_transactions()
        
        if not transactions:
            print("\nNo transactions found.")
            return
        
        print(f"\n--- Transaction History ({len(transactions)} transactions) ---")
        print("-" * 80)
        
        # Sort by date (newest first)
        sorted_transactions = sorted(transactions, 
                                   key=lambda t: t.date, reverse=True)
        
        for transaction in sorted_transactions:
            print(transaction)
    
    def view_summary(self):
        """Display financial summary."""
        total_income = self.tracker.get_total_income()
        total_expenses = self.tracker.get_total_expenses()
        balance = self.tracker.get_balance()
        
        print("\n--- Financial Summary ---")
        print(f"Total Income:  {format_currency(total_income)}")
        print(f"Total Expenses: {format_currency(total_expenses)}")
        print(f"Net Balance:   {format_currency(balance)}")
        
        if balance < 0:
            print("⚠️  You're spending more than you earn!")
        elif balance > 0:
            print("✓ You're saving money!")
        
        # Category breakdown
        category_summary = self.tracker.get_category_summary()
        if category_summary:
            print("\n--- Spending by Category ---")
            for category, amounts in category_summary.items():
                if amounts['expenses'] > 0 or amounts['income'] > 0:
                    print(f"{category}:")
                    if amounts['income'] > 0:
                        print(f"  Income:   {format_currency(amounts['income'])}")
                    if amounts['expenses'] > 0:
                        print(f"  Expenses: {format_currency(amounts['expenses'])}")
                    print(f"  Net:      {format_currency(amounts['net'])}")
                    print()
    
    def generate_report(self):
        """Generate detailed financial report."""
        transactions = self.tracker.get_transactions()
        
        if not transactions:
            print("\nNo data available for report.")
            return
        
        print("\n--- Detailed Financial Report ---")
        
        # Basic stats
        total_transactions = len(transactions)
        income_transactions = len([t for t in transactions if t.is_income])
        expense_transactions = total_transactions - income_transactions
        
        print(f"Total Transactions: {total_transactions}")
        print(f"Income Transactions: {income_transactions}")
        print(f"Expense Transactions: {expense_transactions}")
        
        # Financial summary
        total_income = self.tracker.get_total_income()
        total_expenses = self.tracker.get_total_expenses()
        
        print(f"\nTotal Income: {format_currency(total_income)}")
        print(f"Total Expenses: {format_currency(total_expenses)}")
        print(f"Net Balance: {format_currency(total_income - total_expenses)}")
        
        if total_income > 0:
            savings_rate = ((total_income - total_expenses) / total_income) * 100
            print(f"Savings Rate: {savings_rate:.1f}%")
        
        # Top spending categories
        category_summary = self.tracker.get_category_summary()
        expense_categories = [(cat, data['expenses']) for cat, data in category_summary.items() 
                            if data['expenses'] > 0]
        
        if expense_categories:
            expense_categories.sort(key=lambda x: x[1], reverse=True)
            print(f"\n--- Top Spending Categories ---")
            for i, (category, amount) in enumerate(expense_categories[:5], 1):
                percentage = (amount / total_expenses) * 100 if total_expenses > 0 else 0
                print(f"{i}. {category}: {format_currency(amount)} ({percentage:.1f}%)")
    
    def run(self):
        """Run the main application loop."""
        print("Welcome to Personal Finance Tracker!")
        
        while True:
            try:
                self.display_menu()
                choice = input("Enter your choice (1-5): ").strip()
                
                if choice == '1':
                    self.add_transaction()
                elif choice == '2':
                    self.view_transactions()
                elif choice == '3':
                    self.view_summary()
                elif choice == '4':
                    self.generate_report()
                elif choice == '5':
                    print("\nThank you for using Personal Finance Tracker!")
                    print("Your data has been saved.")
                    break
                else:
                    print("\n✗ Invalid choice. Please enter 1-5.")
                
                if choice in ['2', '3', '4']:
                    pause()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\n✗ An error occurred: {e}")
                pause()


if __name__ == "__main__":
    app = FinanceApp()
    app.run()