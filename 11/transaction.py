"""
Transaction class for representing financial transactions.
"""

from datetime import datetime
from typing import Dict, Any


class Transaction:
    """Represents a single financial transaction."""
    
    def __init__(self, amount: float, description: str, category: str, 
                 is_income: bool = False, date: str = None, currency: str = "USD", room: str = "Personal"):
        """
        Initialize a transaction.
        
        Args:
            amount: Transaction amount (positive number)
            description: Description of the transaction
            category: Category (e.g., 'Food', 'Transport', 'Salary')
            is_income: True if income, False if expense
            date: Transaction date (ISO format), defaults to current date
            currency: Currency code (USD or INR)
            room: Room/space name for organizing transactions
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        self.amount = amount
        self.description = description.strip()
        self.category = category.strip().title()
        self.is_income = is_income
        self.date = date or datetime.now().isoformat()
        self.currency = currency.upper()
        self.room = room.strip().title()
        
        if not self.description:
            raise ValueError("Description cannot be empty")
        if not self.category:
            raise ValueError("Category cannot be empty")
        if self.currency not in ["USD", "INR"]:
            raise ValueError("Currency must be USD or INR")
        if not self.room:
            raise ValueError("Room cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary for JSON serialization."""
        return {
            'id': getattr(self, 'id', None),
            'amount': self.amount,
            'description': self.description,
            'category': self.category,
            'is_income': self.is_income,
            'date': self.date,
            'currency': self.currency,
            'room': self.room
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Create transaction from dictionary."""
        transaction = cls(
            amount=data['amount'],
            description=data['description'],
            category=data['category'],
            is_income=data['is_income'],
            date=data['date'],
            currency=data.get('currency', 'USD'),  # Default for backward compatibility
            room=data.get('room', 'Personal')      # Default for backward compatibility
        )
        # Set ID if it exists
        if 'id' in data and data['id']:
            transaction.id = data['id']
        return transaction
    
    def __str__(self) -> str:
        """String representation of transaction."""
        transaction_type = "Income" if self.is_income else "Expense"
        date_str = datetime.fromisoformat(self.date).strftime("%Y-%m-%d")
        currency_symbol = "₹" if self.currency == "INR" else "$"
        return f"{date_str} | {transaction_type} | {currency_symbol}{self.amount:.2f} | {self.category} | {self.description} | [{self.room}]"
    
    def __repr__(self) -> str:
        return f"Transaction(amount={self.amount}, description='{self.description}', category='{self.category}', is_income={self.is_income})"