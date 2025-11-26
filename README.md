# Django S3 Image Upload Service

A professional Django REST API for uploading and managing images with AWS S3 storage support and JWT authentication.

## Features

- **JWT Authentication**: Secure user signup/login with JSON Web Tokens
- **Image Upload**: Upload images to AWS S3 or local storage
- **User-Based Access**: Each user can only access their own images
- **RESTful API**: Clean REST API endpoints for all operations
- **Image Management**: List, view, and delete uploaded images
- **File Validation**: Automatic validation of file size and type
- **Test Coverage**: Comprehensive pytest test suite
- **Admin Interface**: Django admin for user and image management

## Tech Stack

- **Python**: 3.12.3
- **Django**: 5.2.8
- **Django REST Framework**: 3.16.1
- **JWT Authentication**: djangorestframework-simplejwt 5.5.1
- **AWS S3 Integration**: boto3 1.41.4, django-storages 1.14.6
- **Database**: PostgreSQL 16+ (psycopg2-binary 2.9.11)
- **Image Processing**: Pillow 12.0.0
- **Testing**: pytest 9.0.1, pytest-django 4.11.1

## Prerequisites

- Python 3.12 or higher
- PostgreSQL 16 or higher
- AWS Account with S3 bucket (optional, can use local storage)
- Virtual environment tool (venv or virtualenv)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd django-s3-image-upload
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set your variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=django_s3_images
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# AWS S3 Configuration (optional for local development)
USE_S3=False
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

**Note**: For local development, set `USE_S3=False` to store images locally in the `media/` directory.

### 5. Create PostgreSQL database

```bash
sudo -u postgres psql
CREATE DATABASE django_s3_images;
\q
```

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser (optional)

```bash
python manage.py createsuperuser
```

## Running the Application

### Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

### Admin Interface

Access the Django admin at `http://localhost:8000/admin/`

## API Documentation

### Base URL

```
http://localhost:8000/api/
```

### Authentication Endpoints

#### 1. User Signup

Register a new user and receive JWT tokens.

**Endpoint**: `POST /api/auth/signup/`

**Request Body**:
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123",
  "password2": "SecurePassword123"
}
```

**Response** (201 Created):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "date_joined": "2024-01-15T10:30:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePassword123",
    "password2": "SecurePassword123"
  }'
```

#### 2. User Login

Authenticate and receive JWT tokens.

**Endpoint**: `POST /api/auth/login/`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response** (200 OK):
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123"
  }'
```

#### 3. Refresh Token

Get a new access token using the refresh token.

**Endpoint**: `POST /api/auth/token/refresh/`

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Image Endpoints

All image endpoints require authentication. Include the JWT access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

#### 1. Upload Image

Upload a new image (requires authentication).

**Endpoint**: `POST /api/images/upload/`

**Request**: multipart/form-data
- `image`: Image file (required, max 10MB)
- `title`: Image title (optional)
- `description`: Image description (optional)

**Response** (201 Created):
```json
{
  "id": 1,
  "image": "/media/images/1/uuid-filename.jpg",
  "title": "My Image",
  "description": "A beautiful landscape",
  "uploaded_at": "2024-01-15T10:35:00Z"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/images/upload/ \
  -H "Authorization: Bearer <access_token>" \
  -F "image=@/path/to/image.jpg" \
  -F "title=My Image" \
  -F "description=A beautiful landscape"
```

#### 2. List User's Images

Get all images uploaded by the authenticated user.

**Endpoint**: `GET /api/images/`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "johndoe",
      "date_joined": "2024-01-15T10:30:00Z"
    },
    "image": "/media/images/1/uuid-filename.jpg",
    "image_url": "http://localhost:8000/media/images/1/uuid-filename.jpg",
    "title": "My Image",
    "description": "A beautiful landscape",
    "uploaded_at": "2024-01-15T10:35:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
  }
]
```

**cURL Example**:
```bash
curl -X GET http://localhost:8000/api/images/ \
  -H "Authorization: Bearer <access_token>"
```

#### 3. Get Image Detail

Retrieve details of a specific image (owner only).

**Endpoint**: `GET /api/images/<id>/`

**Response** (200 OK):
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "date_joined": "2024-01-15T10:30:00Z"
  },
  "image": "/media/images/1/uuid-filename.jpg",
  "image_url": "http://localhost:8000/media/images/1/uuid-filename.jpg",
  "title": "My Image",
  "description": "A beautiful landscape",
  "uploaded_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

**cURL Example**:
```bash
curl -X GET http://localhost:8000/api/images/1/ \
  -H "Authorization: Bearer <access_token>"
```

#### 4. Delete Image

Delete an image (owner only).

**Endpoint**: `DELETE /api/images/<id>/delete/`

**Response** (204 No Content)

**cURL Example**:
```bash
curl -X DELETE http://localhost:8000/api/images/1/delete/ \
  -H "Authorization: Bearer <access_token>"
```

## Testing

The project includes a comprehensive test suite using pytest.

### Run all tests

```bash
pytest
```

### Run with verbose output

```bash
pytest -v
```

### Run specific test file

```bash
pytest users/tests.py
pytest images/tests.py
```

### Test Coverage

- **Authentication Tests**: Signup, login, JWT tokens, validation
- **Image Upload Tests**: Upload, list, detail, delete, file validation
- **Authorization Tests**: Unauthenticated access, owner-only operations

## AWS S3 Configuration

### Setting up AWS S3

1. **Create an S3 bucket** in your AWS Console
2. **Create an IAM user** with programmatic access
3. **Attach the following policy** to the IAM user:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::your-bucket-name/*",
        "arn:aws:s3:::your-bucket-name"
      ]
    }
  ]
}
```

4. **Configure bucket CORS** (if accessing from web):

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": []
  }
]
```

5. **Update `.env`** with your AWS credentials:

```env
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### Using LocalStack for Local S3 Testing

For local development without AWS costs, use LocalStack:

```bash
# Install LocalStack
pip install localstack

# Start LocalStack with S3
localstack start -d

# Create a bucket
aws --endpoint-url=http://localhost:4566 s3 mb s3://test-bucket

# Update .env
USE_S3=True
AWS_S3_ENDPOINT_URL=http://localhost:4566
AWS_STORAGE_BUCKET_NAME=test-bucket
```

## Project Structure

```
django-s3-image-upload/
├── config/              # Django project settings
│   ├── settings.py      # Main settings with S3, JWT, REST Framework
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py
├── users/               # User authentication app
│   ├── models.py        # Custom User model with email auth
│   ├── serializers.py   # User serializers for signup/login
│   ├── views.py         # Authentication views
│   ├── urls.py          # Auth endpoints
│   ├── admin.py         # User admin configuration
│   └── tests.py         # Authentication tests
├── images/              # Image management app
│   ├── models.py        # Image model with S3 support
│   ├── serializers.py   # Image serializers with validation
│   ├── views.py         # Image CRUD views
│   ├── urls.py          # Image endpoints
│   ├── admin.py         # Image admin configuration
│   └── tests.py         # Image upload tests
├── media/               # Local media files (if USE_S3=False)
├── venv/                # Virtual environment
├── .env                 # Environment variables (not in git)
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
├── pytest.ini           # Pytest configuration
├── conftest.py          # Pytest fixtures
├── manage.py            # Django management script
└── README.md            # This file
```

## Image Storage

### Local Storage (Development)

When `USE_S3=False` in `.env`:
- Images stored in `media/images/{user_id}/` directory
- Accessed via `/media/` URL path
- Files persist on local filesystem

### S3 Storage (Production)

When `USE_S3=True` in `.env`:
- Images uploaded to AWS S3 bucket
- Path: `images/{user_id}/{uuid}_{filename}`
- Accessed via S3 URL or CloudFront CDN
- Files stored in cloud with high availability

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Validation**: Django's built-in password validators
- **File Validation**: Size limit (10MB) and type checking
- **User Isolation**: Users can only access their own images
- **Environment Variables**: Sensitive data not hardcoded
- **CORS Ready**: Can be configured for cross-origin requests

## Deployment Considerations

### Environment Variables for Production

```env
DEBUG=False
SECRET_KEY=strong-random-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
USE_S3=True
# ... AWS credentials
```

### Database

- Use managed PostgreSQL service (AWS RDS, DigitalOcean)
- Enable SSL connections
- Regular backups

### Static Files

```bash
python manage.py collectstatic
```

### WSGI Server

Use Gunicorn or uWSGI:

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Reverse Proxy

Configure Nginx or Apache as reverse proxy with SSL.

## API Response Formats

### Success Response

```json
{
  "id": 1,
  "field": "value",
  ...
}
```

### Error Response

```json
{
  "field": [
    "Error message"
  ]
}
```

### Validation Error

```json
{
  "detail": "Authentication credentials were not provided."
}
```

## JWT Token Lifetime

- **Access Token**: 24 hours
- **Refresh Token**: 7 days

Configure in `config/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is open source and available under the MIT License.

## Author

Portfolio Project - Full Stack Developer

## Support

For issues, questions, or contributions, please open an issue on GitHub.
