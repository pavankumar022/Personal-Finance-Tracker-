"""
Utility functions for the finance tracker.
"""

import os
from typing import Optional


def get_float_input(prompt: str, min_value: float = 0.01) -> float:
    """
    Get a valid float input from user.
    
    Args:
        prompt: Input prompt message
        min_value: Minimum allowed value
        
    Returns:
        Valid float value
    """
    while True:
        try:
            value = float(input(prompt))
            if value < min_value:
                print(f"Please enter a value >= {min_value}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_yes_no_input(prompt: str) -> bool:
    """
    Get yes/no input from user.
    
    Args:
        prompt: Input prompt message
        
    Returns:
        True for yes, False for no
    """
    while True:
        response = input(prompt).lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def get_string_input(prompt: str, min_length: int = 1) -> str:
    """
    Get a non-empty string input from user.
    
    Args:
        prompt: Input prompt message
        min_length: Minimum string length
        
    Returns:
        Valid string input
    """
    while True:
        value = input(prompt).strip()
        if len(value) >= min_length:
            return value
        print(f"Please enter at least {min_length} character(s).")


def ensure_data_directory() -> str:
    """
    Ensure data directory exists and return its path.
    
    Returns:
        Path to data directory
    """
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir


def format_currency(amount: float) -> str:
    """Format amount as currency string."""
    return f"${amount:.2f}"


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pause execution until user presses Enter."""
    input("\nPress Enter to continue...")