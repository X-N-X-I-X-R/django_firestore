# Connectify - Online Consulting Platform

## 🚀 Technical Overview
A Django-based platform connecting advisors with clients, featuring real-time communication and professional consulting tools.

## 🛠 Tech Stack
- **Backend**: Django 4.x
- **Authentication**: JWT with refresh tokens
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Real-time**: Django Channels with Redis
- **API Documentation**: Swagger/OpenAPI
- **Email Service**: Gmail SMTP
- **Security**: Custom Django Security Middleware

## 🔧 Development Setup

### Prerequisites
- Python 3.8+
- Redis (for Channels)
- Git

### Installation
1. **Clone Repository**
```bash
git clone [repository-url]
cd Django_server
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Variables**
Create `.env` file in project root:
```env
DJANGO_SERVER=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

4. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Run Development Server**
```bash
python manage.py runserver
```

## 🔐 Security Implementation

### JWT Configuration
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS512',
    'AUDIENCE': "Nir Fullstack Project",    
    'ISSUER': "None",
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

### Rate Limiting
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

## 📧 Email Configuration
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

## 🔄 Registration Flow

### Customer Registration
1. Basic registration with email verification
2. JWT token generation
3. Profile creation

### Advisor Registration
1. Extended registration with document verification
2. Expertise and rate setting
3. Admin approval process

## 📝 API Endpoints

### Authentication
```
POST /api/v1/auth/register/ - User registration
POST /api/v1/auth/login/ - User login
POST /api/v1/auth/verify-email/ - Email verification
POST /api/v1/auth/token/ - Get JWT token
POST /api/v1/auth/token/refresh/ - Refresh JWT token
```

## 🔍 Logging System
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'formatters': {
        'colored': {
            '()': StatusCodeFormatter,
            'format': "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(asctime)s%(reset)s %(log_color)s%(message)s%(reset)s",
        }
    }
}
```

## 🚀 Development Workflow

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Git Automation
```bash
./lazygithub.sh  # Automated git push script
```

### Testing
```bash
python manage.py test
```

## 📦 Project Structure
```
myapp/
├── services/      # Business logic
├── views/         # API endpoints
├── forms/         # Registration forms
├── models.py      # Database models
├── urls.py        # URL routing
└── middleware.py  # Custom middleware
```

## 🔒 Security Settings
```python
# CSRF Settings
CSRF_COOKIE_SECURE = False if DEBUG else True
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

# Cookie Settings
SESSION_COOKIE_SECURE = False if DEBUG else True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## 🌐 CORS Configuration
```python
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    # Add your frontend URLs here
]
```

## 📅 Time Settings
```python
TIME_ZONE = 'Asia/Jerusalem'
USE_TZ = True
```

## 🔄 Deployment Checklist
1. Update `DEBUG = False`
2. Set proper `ALLOWED_HOSTS`
3. Configure production database
4. Set up SSL certificates
5. Update email credentials
6. Configure proper CORS settings
7. Set up proper logging
8. Run migrations
9. Collect static files

## 🐛 Common Issues & Solutions

### JWT Token Issues
- Check token expiration settings
- Verify token blacklist is working
- Ensure proper token refresh flow

### Email Verification
- Verify SMTP settings
- Check spam folder
- Ensure proper email templates

### Database Migrations
- Backup database before migrations
- Check for conflicting migrations
- Verify model changes

## 📚 Additional Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Channels Documentation](https://channels.readthedocs.io/)
