"""
Core finance tracker functionality.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict

from transaction import Transaction
from utils import ensure_data_directory, format_currency


class FinanceTracker:
    """Main finance tracker class."""
    
    def __init__(self, data_file: str = "transactions.json"):
        """
        Initialize the finance tracker.
        
        Args:
            data_file: Name of the JSON file to store transactions
        """
        self.data_dir = ensure_data_directory()
        self.data_file = os.path.join(self.data_dir, data_file)
        self.transactions: List[Transaction] = []
        self.load_transactions()
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a new transaction."""
        # Add unique ID to transaction
        transaction.id = len(self.transactions) + 1
        self.transactions.append(transaction)
        self.save_transactions()
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction by ID."""
        for i, transaction in enumerate(self.transactions):
            if hasattr(transaction, 'id') and transaction.id == transaction_id:
                del self.transactions[i]
                self.save_transactions()
                return True
        return False
    
    def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        """Get a transaction by ID."""
        for transaction in self.transactions:
            if hasattr(transaction, 'id') and transaction.id == transaction_id:
                return transaction
        return None
    
    def update_transaction(self, transaction_id: int, updated_transaction: Transaction) -> bool:
        """Update a transaction by ID."""
        for i, transaction in enumerate(self.transactions):
            if hasattr(transaction, 'id') and transaction.id == transaction_id:
                updated_transaction.id = transaction_id
                self.transactions[i] = updated_transaction
                self.save_transactions()
                return True
        return False
    
    def reset_all_transactions(self) -> bool:
        """Delete all transactions."""
        self.transactions = []
        self.save_transactions()
        return True
    
    def get_transactions(self, room: str = None) -> List[Transaction]:
        """Get all transactions, optionally filtered by room."""
        if room:
            return [t for t in self.transactions if t.room == room]
        return self.transactions.copy()
    
    def get_rooms(self) -> List[str]:
        """Get list of all unique rooms."""
        rooms = list(set(t.room for t in self.transactions))
        return sorted(rooms) if rooms else ["Personal"]
    
    def get_transactions_by_category(self) -> Dict[str, List[Transaction]]:
        """Group transactions by category."""
        categories = defaultdict(list)
        for transaction in self.transactions:
            categories[transaction.category].append(transaction)
        return dict(categories)
    
    def get_balance(self, room: str = None, currency: str = None) -> Dict[str, float]:
        """Calculate current balance by currency, optionally filtered by room."""
        balances = {"USD": 0.0, "INR": 0.0}
        transactions = self.get_transactions(room) if room else self.transactions
        
        for transaction in transactions:
            if currency and transaction.currency != currency:
                continue
                
            if transaction.is_income:
                balances[transaction.currency] += transaction.amount
            else:
                balances[transaction.currency] -= transaction.amount
        
        return balances if not currency else {currency: balances[currency]}
    
    def get_total_income(self, room: str = None, currency: str = None) -> Dict[str, float]:
        """Calculate total income by currency, optionally filtered by room."""
        totals = {"USD": 0.0, "INR": 0.0}
        transactions = self.get_transactions(room) if room else self.transactions
        
        for t in transactions:
            if t.is_income:
                if not currency or t.currency == currency:
                    totals[t.currency] += t.amount
        
        return totals if not currency else {currency: totals[currency]}
    
    def get_total_expenses(self, room: str = None, currency: str = None) -> Dict[str, float]:
        """Calculate total expenses by currency, optionally filtered by room."""
        totals = {"USD": 0.0, "INR": 0.0}
        transactions = self.get_transactions(room) if room else self.transactions
        
        for t in transactions:
            if not t.is_income:
                if not currency or t.currency == currency:
                    totals[t.currency] += t.amount
        
        return totals if not currency else {currency: totals[currency]}
    
    def get_category_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Get spending summary by category.
        
        Returns:
            Dictionary with category names as keys and spending info as values
        """
        summary = defaultdict(lambda: {'income': 0.0, 'expenses': 0.0, 'net': 0.0})
        
        for transaction in self.transactions:
            category = transaction.category
            if transaction.is_income:
                summary[category]['income'] += transaction.amount
            else:
                summary[category]['expenses'] += transaction.amount
            
            summary[category]['net'] = summary[category]['income'] - summary[category]['expenses']
        
        return dict(summary)
    
    def save_transactions(self) -> None:
        """Save transactions to JSON file."""
        try:
            data = [transaction.to_dict() for transaction in self.transactions]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving transactions: {e}")
    
    def load_transactions(self) -> None:
        """Load transactions from JSON file."""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            self.transactions = [Transaction.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error loading transactions: {e}")
            self.transactions = []