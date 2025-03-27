# Django Server Project

A modern Django REST API server with JWT authentication and user management.

## Project Structure

```
myapp/
├── api/                    # API endpoints
│   ├── v1/                # API version 1
│   │   ├── views/         # API views
│   │   ├── serializers/   # API serializers
│   │   └── urls.py        # API URL routing
├── core/                   # Core application
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── signals.py         # Django signals
├── utils/                  # Utility functions
├── middlewares/           # Custom middlewares
└── tests/                # Unit tests
```

## Setup

1. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Features

- JWT Authentication
- Custom User Model
- API Versioning
- Swagger Documentation
- Email Notifications
- User Management
- Profile Management

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
```bash
black .
flake8
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
