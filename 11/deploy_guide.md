# Deployment Guide - Personal Finance Tracker

## 🚀 Deploy to Web (Free Options)

### Option 1: Heroku (Recommended)

1. **Create Heroku Account**: Sign up at [heroku.com](https://heroku.com)

2. **Install Heroku CLI**: Download from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

3. **Deploy Steps**:
   ```bash
   # Login to Heroku
   heroku login
   
   # Create new app
   heroku create your-finance-tracker-name
   
   # Set environment variables
   heroku config:set SECRET_KEY=your-super-secret-key-here
   heroku config:set FLASK_ENV=production
   
   # Deploy
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

4. **Your app will be live at**: `https://your-finance-tracker-name.herokuapp.com`

### Option 2: Railway

1. **Create Railway Account**: Sign up at [railway.app](https://railway.app)

2. **Deploy Steps**:
   - Connect your GitHub repository
   - Railway will auto-detect Flask app
   - Set environment variables in Railway dashboard:
     - `SECRET_KEY`: your-super-secret-key-here
     - `FLASK_ENV`: production

### Option 3: Render

1. **Create Render Account**: Sign up at [render.com](https://render.com)

2. **Deploy Steps**:
   - Create new Web Service
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`
   - Add environment variables

### Option 4: PythonAnywhere

1. **Create PythonAnywhere Account**: Sign up at [pythonanywhere.com](https://pythonanywhere.com)

2. **Deploy Steps**:
   - Upload files to your account
   - Create new web app
   - Configure WSGI file to point to your app
   - Set environment variables

## 🔒 Security Features

- ✅ **User Authentication**: Secure login/signup system
- ✅ **Password Hashing**: SHA-256 password encryption
- ✅ **Session Management**: Secure user sessions
- ✅ **Data Isolation**: Each user has separate data files
- ✅ **Login Required**: All financial data protected by authentication

## 🌐 Production Configuration

### Environment Variables to Set:
- `SECRET_KEY`: Strong secret key for session security
- `FLASK_ENV`: Set to "production"
- `PORT`: Port number (usually set by hosting provider)

### Security Recommendations:
1. Use strong SECRET_KEY (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
2. Enable HTTPS on your hosting platform
3. Regularly backup user data
4. Monitor for suspicious activity

## 📱 Features Available Online:

- ✅ **Multi-User Support**: Each user has private account
- ✅ **Secure Authentication**: Login/logout system
- ✅ **Multi-Currency**: USD ($) and INR (₹) support
- ✅ **Room Organization**: 10+ customizable rooms
- ✅ **Real-time Charts**: Interactive expense visualization
- ✅ **Mobile Responsive**: Works on all devices
- ✅ **Data Persistence**: Automatic saving to user-specific files

## 🔧 Local Development:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

Visit: `http://localhost:5000`

## 📊 User Data Storage:

- User accounts: `data/users.json`
- User transactions: `data/{username}_transactions.json`
- Each user's data is completely isolated and secure