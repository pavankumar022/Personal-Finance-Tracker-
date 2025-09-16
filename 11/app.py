"""
Personal Finance Tracker - Web Application with Authentication, Rooms and Multi-Currency
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
from functools import wraps
import os
from finance_tracker import FinanceTracker
from transaction import Transaction
from user_manager import UserManager

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Initialize managers
user_manager = UserManager()
trackers = {}  # Store trackers per user

# Default rooms
DEFAULT_ROOMS = [
    "Personal", "Business", "Travel", "Family", "Investment", 
    "Education", "Health", "Entertainment", "Emergency", "Savings"
]


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_user_tracker(username: str) -> FinanceTracker:
    """Get or create tracker for user."""
    if username not in trackers:
        # Create user-specific data file
        user_data_file = f"{username}_transactions.json"
        trackers[username] = FinanceTracker(user_data_file)
    return trackers[username]


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if user_manager.authenticate_user(username, password):
            session['username'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup page."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email'].strip()
        
        # Validation
        if len(username) < 3:
            flash('Username must be at least 3 characters long.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match.', 'error')
        elif '@' not in email:
            flash('Please enter a valid email address.', 'error')
        elif user_manager.user_exists(username):
            flash('Username already exists. Please choose another.', 'error')
        else:
            # Create user
            if user_manager.create_user(username, password, email):
                session['username'] = username
                flash(f'Account created successfully! Welcome, {username}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Error creating account. Please try again.', 'error')
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    """User logout."""
    username = session.get('username')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/')
@app.route('/room/<room_name>')
@login_required
def index(room_name=None):
    """Home page with dashboard, optionally filtered by room."""
    username = session['username']
    tracker = get_user_tracker(username)
    
    current_room = room_name or session.get('current_room', 'All')
    session['current_room'] = current_room
    
    transactions = tracker.get_transactions(room_name if room_name != 'All' else None)
    recent_transactions = sorted(transactions, key=lambda t: t.date, reverse=True)[:5]
    
    total_income = tracker.get_total_income(room_name if room_name != 'All' else None)
    total_expenses = tracker.get_total_expenses(room_name if room_name != 'All' else None)
    balance = tracker.get_balance(room_name if room_name != 'All' else None)
    
    rooms = tracker.get_rooms()
    if not rooms:
        rooms = DEFAULT_ROOMS[:3]  # Show first 3 default rooms if no transactions
    
    return render_template('index.html', 
                         recent_transactions=recent_transactions,
                         total_income=total_income,
                         total_expenses=total_expenses,
                         balance=balance,
                         rooms=rooms,
                         current_room=current_room,
                         username=username)


@app.route('/add_transaction', methods=['GET', 'POST'])
@app.route('/add_transaction/<room_name>', methods=['GET', 'POST'])
@login_required
def add_transaction(room_name=None):
    """Add new transaction page."""
    username = session['username']
    tracker = get_user_tracker(username)
    current_room = room_name or session.get('current_room', 'Personal')
    
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            description = request.form['description'].strip()
            category = request.form['category'].strip()
            currency = request.form['currency']
            room = request.form['room'].strip()
            is_income = request.form.get('is_income') == 'on'
            
            if amount <= 0:
                flash('Amount must be positive', 'error')
                return render_template('add_transaction.html', rooms=DEFAULT_ROOMS, current_room=current_room)
            
            if not description or not category or not room:
                flash('All fields are required', 'error')
                return render_template('add_transaction.html', rooms=DEFAULT_ROOMS, current_room=current_room)
            
            transaction = Transaction(amount, description, category, is_income, currency=currency, room=room)
            tracker.add_transaction(transaction)
            
            transaction_type = "Income" if is_income else "Expense"
            currency_symbol = "₹" if currency == "INR" else "$"
            flash(f'{transaction_type} of {currency_symbol}{amount:.2f} added to {room}!', 'success')
            
            # Redirect to the room where transaction was added
            return redirect(url_for('index', room_name=room if room != 'All' else None))
            
        except ValueError as e:
            flash(f'Error: {str(e)}', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    rooms = tracker.get_rooms() + [r for r in DEFAULT_ROOMS if r not in tracker.get_rooms()]
    return render_template('add_transaction.html', rooms=rooms, current_room=current_room)


@app.route('/transactions')
@app.route('/transactions/<room_name>')
@login_required
def transactions(room_name=None):
    """View all transactions, optionally filtered by room."""
    username = session['username']
    tracker = get_user_tracker(username)
    current_room = room_name or session.get('current_room', 'All')
    
    all_transactions = tracker.get_transactions(room_name if room_name != 'All' else None)
    sorted_transactions = sorted(all_transactions, key=lambda t: t.date, reverse=True)
    
    rooms = tracker.get_rooms()
    
    return render_template('transactions.html', 
                         transactions=sorted_transactions,
                         rooms=rooms,
                         current_room=current_room)


@app.route('/summary')
@app.route('/summary/<room_name>')
@login_required
def summary(room_name=None):
    """Financial summary page, optionally filtered by room."""
    username = session['username']
    tracker = get_user_tracker(username)
    current_room = room_name or session.get('current_room', 'All')
    
    total_income = tracker.get_total_income(room_name if room_name != 'All' else None)
    total_expenses = tracker.get_total_expenses(room_name if room_name != 'All' else None)
    balance = tracker.get_balance(room_name if room_name != 'All' else None)
    category_summary = tracker.get_category_summary()
    
    rooms = tracker.get_rooms()
    
    return render_template('summary.html',
                         total_income=total_income,
                         total_expenses=total_expenses,
                         balance=balance,
                         category_summary=category_summary,
                         rooms=rooms,
                         current_room=current_room)


@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    """Edit an existing transaction."""
    username = session['username']
    tracker = get_user_tracker(username)
    
    transaction = tracker.get_transaction_by_id(transaction_id)
    if not transaction:
        flash('Transaction not found.', 'error')
        return redirect(url_for('transactions'))
    
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            description = request.form['description'].strip()
            category = request.form['category'].strip()
            currency = request.form['currency']
            room = request.form['room'].strip()
            is_income = request.form.get('is_income') == 'on'
            
            if amount <= 0:
                flash('Amount must be positive', 'error')
                return render_template('edit_transaction.html', transaction=transaction, rooms=DEFAULT_ROOMS)
            
            if not description or not category or not room:
                flash('All fields are required', 'error')
                return render_template('edit_transaction.html', transaction=transaction, rooms=DEFAULT_ROOMS)
            
            updated_transaction = Transaction(amount, description, category, is_income, 
                                            date=transaction.date, currency=currency, room=room)
            
            if tracker.update_transaction(transaction_id, updated_transaction):
                transaction_type = "Income" if is_income else "Expense"
                currency_symbol = "₹" if currency == "INR" else "$"
                flash(f'{transaction_type} updated successfully!', 'success')
                return redirect(url_for('transactions'))
            else:
                flash('Error updating transaction.', 'error')
                
        except ValueError as e:
            flash(f'Error: {str(e)}', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    rooms = tracker.get_rooms() + [r for r in DEFAULT_ROOMS if r not in tracker.get_rooms()]
    return render_template('edit_transaction.html', transaction=transaction, rooms=rooms)


@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    """Delete a transaction."""
    username = session['username']
    tracker = get_user_tracker(username)
    
    if tracker.delete_transaction(transaction_id):
        flash('Transaction deleted successfully!', 'success')
    else:
        flash('Transaction not found.', 'error')
    
    return redirect(url_for('transactions'))


@app.route('/reset_data', methods=['GET', 'POST'])
@login_required
def reset_data():
    """Reset all user data."""
    username = session['username']
    
    if request.method == 'POST':
        confirm = request.form.get('confirm')
        if confirm == 'DELETE_ALL_DATA':
            tracker = get_user_tracker(username)
            tracker.reset_all_transactions()
            flash('All transaction data has been reset!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Confirmation text did not match. Data not deleted.', 'error')
    
    return render_template('reset_data.html')


@app.route('/api/chart_data')
@app.route('/api/chart_data/<room_name>')
@login_required
def chart_data(room_name=None):
    """API endpoint for chart data."""
    username = session['username']
    tracker = get_user_tracker(username)
    transactions = tracker.get_transactions(room_name if room_name != 'All' else None)
    
    # Separate data by currency
    usd_expenses = {}
    inr_expenses = {}
    
    for transaction in transactions:
        if not transaction.is_income:
            if transaction.currency == 'USD':
                usd_expenses[transaction.category] = usd_expenses.get(transaction.category, 0) + transaction.amount
            else:
                inr_expenses[transaction.category] = inr_expenses.get(transaction.category, 0) + transaction.amount
    
    return jsonify({
        'usd': [{'category': cat, 'amount': amt} for cat, amt in usd_expenses.items()],
        'inr': [{'category': cat, 'amount': amt} for cat, amt in inr_expenses.items()]
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)