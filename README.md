# Expense Tracker with Templates & Views

A comprehensive Django-based expense tracking application with user authentication, budget management, dashboard analytics, and profile settings.

## Features

- **User Authentication**: Email-based registration, login, logout, and OTP verification
- **Expense Management**: Track, categorize, and manage daily expenses
- **Budget Planning**: Create and monitor budgets with spending alerts
- **Dashboard**: Visual analytics and expense summaries with charts
- **User Profiles**: Manage profile information and upload avatars
- **Password Reset**: Secure password recovery with OTP verification
- **User Settings**: Customize application preferences and account settings

## Project Structure

```
expense_track_main/
├── account/              # User authentication and profiles
├── expense_app/          # Expense management
├── budget_app/          # Budget tracking and management
├── dashboard/           # Analytics and reporting
├── usersettings/        # User preferences and settings
├── expense_track_main/  # Django project configuration
├── templates/           # HTML templates for all apps
├── static/              # CSS and JavaScript files
├── media/               # User-uploaded content (avatars, etc.)
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual Environment (recommended)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/codebyrishi3075/Expense-tracker-with-templates-views.git
   cd Expense-tracker-with-templates-views
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load Sample Data (Optional)**
   ```bash
   python manage.py seed_expenses
   ```

8. **Start Development Server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser

## Usage

### User Account
- **Register**: Visit `/register/` to create a new account
- **Login**: Access `/login/` with your credentials
- **Profile**: Manage your profile at `/profile/`
- **Settings**: Customize preferences at `/settings/`

### Expense Management
- View all expenses at `/expenses/`
- Add new expenses with categories and amounts
- Filter and sort expenses by date and category

### Budget Management
- Create budgets at `/budget/`
- Set spending limits per category
- Monitor budget usage and receive alerts

### Dashboard
- View financial overview at `/dashboard/summary/`
- Check spending trends and analytics
- Monitor budget status

## Technologies Used

- **Backend**: Django 6.0+
- **Database**: SQLite (default)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django Auth + Custom Email Backend
- **Email**: SMTP (Gmail)

## Configuration

Key settings in `expense_track_main/settings.py`:
- `DEBUG = True` (change to `False` in production)
- `ALLOWED_HOSTS = []` (update for production)
- `LOGIN_URL = 'login'` (custom login redirect URL)

## API & Views

### Account App
- `GET /` - Home page
- `POST /register/` - User registration
- `POST /verify-otp/` - Email verification
- `POST /login/` - User login
- `GET /logout/` - User logout
- `GET /profile/` - User profile
- `POST /update-profile/` - Update profile
- `POST /upload-avatar/` - Upload profile picture
- `POST /password-reset/` - Request password reset

### Expense App
- `GET /expenses/` - List all expenses
- `POST /expenses/` - Create new expense
- `GET /expenses/<id>/` - Expense detail
- `PUT /expenses/<id>/` - Update expense
- `DELETE /expenses/<id>/` - Delete expense

### Budget App
- `GET /budget/` - View budgets
- `POST /budget/` - Create budget
- `GET /budget/categories/` - Budget categories

### Dashboard
- `GET /dashboard/summary/` - Dashboard overview

### Settings
- `GET /settings/` - User settings page

## Testing

Run tests:
```bash
python manage.py test
```

Run specific app tests:
```bash
python manage.py test account
python manage.py test expense_app
python manage.py test budget_app
python manage.py test dashboard
python manage.py test usersettings
```

## Troubleshooting

### Common Issues

**404 Error for /accounts/login/**
- This is a Django default redirect URL that doesn't exist in this project
- The actual login URL is `/login/`
- Already configured via `LOGIN_URL = 'login'` in settings

**Email Not Sending**
- Verify Gmail credentials in `.env` file
- Use App Password for Gmail (not regular password)
- Enable "Less secure app access" if needed

**Database Errors**
- Delete `db.sqlite3` and run `python manage.py migrate` again
- Check migrations in each app's `migrations/` folder

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact & Support

- **GitHub**: [codebyrishi3075](https://github.com/codebyrishi3075)
- **Email**: For support, create an issue in the repository

## Acknowledgments

- Django Documentation
- Bootstrap for UI components
- Community contributors

---
**Last Updated**: March 9, 2026
