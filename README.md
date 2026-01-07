# Employee Authentication System

A production-ready centralized authentication system for managing employee information and authentication across multiple company applications.

## Features

- 🔐 JWT-based authentication
- 👥 Comprehensive employee management
- 🛡️ Role-based access control (Admin/Employee)
- 🔑 Secure password change functionality
- 📊 Production-ready with security best practices
- 🚀 RESTful API architecture

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 5. Run Server

```bash
python manage.py runserver
```

Server will start at: http://127.0.0.1:8000/

## API Endpoints

### Authentication

- `POST /api/auth/login/` - Employee login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/change-password/` - Change password (requires authentication)

### Employee Management (Admin only)

- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee
- `PATCH /api/employees/{id}/` - Partial update employee
- `DELETE /api/employees/{id}/` - Delete employee

### Employee Self-Service

- `GET /api/employees/me/` - Get own profile
- `PUT /api/employees/me/` - Update own profile (limited fields)

## API Usage Examples

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john.doe", "password": "password123"}'
```

### Create Employee (Admin)
```bash
curl -X POST http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane.smith",
    "email": "jane@company.com",
    "password": "secure_password",
    "first_name": "Jane",
    "last_name": "Smith",
    "employee_id": "EMP002",
    "position": "Software Engineer",
    "department": "Engineering",
    "phone_number": "+1234567890",
    "salary": "75000.00",
    "joining_date": "2024-01-15"
  }'
```

### Change Password
```bash
curl -X POST http://127.0.0.1:8000/api/auth/change-password/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "current_password",
    "new_password": "new_secure_password"
  }'
```

## Production Deployment

1. Set `DEBUG=False` in .env
2. Generate secure SECRET_KEY
3. Configure proper database (PostgreSQL recommended)
4. Set up proper ALLOWED_HOSTS
5. Use gunicorn: `gunicorn employee_auth.wsgi:application`
6. Configure nginx as reverse proxy
7. Enable HTTPS

## Security Features

- Password hashing with Django's PBKDF2
- JWT token authentication
- CSRF protection
- CORS configuration
- Password validation rules
- Role-based permissions
- Secure headers with WhiteNoise

## Project Structure

```
employee_auth_system/
├── employee_auth/          # Project settings
├── authentication/         # Auth app
│   ├── models.py          # Employee model
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   └── permissions.py     # Custom permissions
├── manage.py
└── requirements.txt
```