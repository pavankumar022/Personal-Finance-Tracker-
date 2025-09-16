"""
User management system for the finance tracker.
"""

import json
import os
import hashlib
from typing import Dict, Optional
from datetime import datetime


class UserManager:
    """Handles user authentication and management."""
    
    def __init__(self, users_file: str = "users.json"):
        """Initialize user manager."""
        self.users_file = os.path.join("data", users_file)
        self.users: Dict[str, Dict] = {}
        self.load_users()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, email: str) -> bool:
        """
        Create a new user account.
        
        Args:
            username: Unique username
            password: User password
            email: User email
            
        Returns:
            True if user created successfully, False if username exists
        """
        if username in self.users:
            return False
        
        self.users[username] = {
            'password_hash': self.hash_password(password),
            'email': email,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        self.save_users()
        return True
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate user credentials.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            True if credentials are valid
        """
        if username not in self.users:
            return False
        
        password_hash = self.hash_password(password)
        if self.users[username]['password_hash'] == password_hash:
            # Update last login
            self.users[username]['last_login'] = datetime.now().isoformat()
            self.save_users()
            return True
        
        return False
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists."""
        return username in self.users
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information (without password hash)."""
        if username not in self.users:
            return None
        
        user_info = self.users[username].copy()
        del user_info['password_hash']  # Don't return password hash
        return user_info
    
    def save_users(self) -> None:
        """Save users to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def load_users(self) -> None:
        """Load users from JSON file."""
        if not os.path.exists(self.users_file):
            return
        
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
            self.users = {}