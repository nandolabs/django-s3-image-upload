

# Django S3 Image Upload Service

## Problem this solves

Many applications need to store and serve user-uploaded images (profile pictures, content uploads, media assets, etc.). Handling image uploads, storage, access control, and secure retrieval — especially at scale — can be a complex, error-prone task. This service provides a robust, ready-to-use backend that simplifies image storage by offloading file storage to Amazon S3 (or fallback to local storage), while ensuring secure access and clean management out-of-the-box.

## Core Features

* Secure user authentication with JSON Web Tokens (JWT) — each user can manage only their own images. ([GitHub][1])
* Upload images (to S3 or local storage) with automatic validation (file type and size). ([GitHub][1])
* RESTful API endpoints to upload, list, retrieve, and delete images. ([GitHub][1])
* File metadata stored in a relational database (PostgreSQL), while actual image binaries are stored on S3 (or filesystem). ([GitHub][1])
* Admin interface for image/user management (via Django Admin). ([GitHub][1])
* Optional S3 support — works with local storage out-of-the-box for development or low-scale projects. ([GitHub][1])
* API documentation via Swagger / OpenAPI at `/api/docs/` for easy integration. ([GitHub][1])
* Full test coverage (pytest + pytest-django) to ensure reliability. ([GitHub][1])

## Why this matters for clients on Upwork

* **Time-to-market:** You get a production-ready, secure image upload backend without needing to design or build storage logic from scratch.
* **Scalability:** With S3 integration and database-backed metadata, the system is ready to handle growth — from small prototypes to large user bases.
* **Security and compliance:** JWT authentication and per-user access control reduce risk of unauthorized access to user media.
* **Flexibility:** Since the service supports local storage for development and S3 for production, you can deploy it in any environment (dev, staging, production) easily.
* **Easy integration:** Clean RESTful API + OpenAPI docs means frontend teams (React, Vue, mobile) or external clients can consume the service without friction.

## Installation & Setup

```bash
git clone https://github.com/nandolabs/django-s3-image-upload.git  
cd django-s3-image-upload  
python3 -m venv venv  
source venv/bin/activate         # On Windows: venv\Scripts\activate  
pip install -r requirements.txt  
cp .env.example .env  
```

Then open `.env` and configure variables:

```ini
# Django settings  
SECRET_KEY=your-secret-key  
DEBUG=True  
ALLOWED_HOSTS=localhost,127.0.0.1  

# Database (PostgreSQL)  
DB_NAME=your_db_name  
DB_USER=your_db_user  
DB_PASSWORD=your_db_password  
DB_HOST=localhost  
DB_PORT=5432  

# AWS S3 (optional)  
USE_S3=False                         # Set to True to enable S3  
AWS_ACCESS_KEY_ID=your_aws_key  
AWS_SECRET_ACCESS_KEY=your_aws_secret  
AWS_STORAGE_BUCKET_NAME=your_bucket_name  
AWS_S3_REGION_NAME=your_region  
```

If you use local storage, set `USE_S3=False`; for S3 storage, provide valid AWS credentials and a bucket name. ([GitHub][1])

Next, in your PostgreSQL instance create the database and run migrations:

```bash
createdb your_db_name  
python manage.py migrate  
python manage.py createsuperuser   # optional, for admin interface  
```

Start the development server:

```bash
python manage.py runserver
```

Access the API at `http://localhost:8000/`, and the admin interface at `http://localhost:8000/admin/`.

## Example API Requests

**Upload an image**

```
POST /api/images/  
Authorization: Bearer <JWT_TOKEN>  
Content-Type: multipart/form-data  

Form-Data:
  file: <binary image file>
```

*Response (JSON):*

```json
{
  "id": 123,
  "user": "user_id",
  "file_name": "my_photo.jpg",
  "file_url": "https://your-bucket.s3.amazonaws.com/uploads/2025/12/07/uuid-my_photo.jpg",
  "uploaded_at": "2025-12-07T12:34:56Z"
}
```

**List user images**

```
GET /api/images/  
Authorization: Bearer <JWT_TOKEN>
```

*Response:*

```json
[
  { "id": 123, "file_url": "...", "uploaded_at": "..." },
  { "id": 124, "file_url": "...", "uploaded_at": "..." }
]
```

**Delete an image**

```
DELETE /api/images/123/  
Authorization: Bearer <JWT_TOKEN>
```

*Response:* HTTP 204 No Content

## Screenshot

* Screenshot of the Swagger / OpenAPI API docs page (e.g. at `/api/docs/`)
![alt text](../support_files_for_django/swagger_documentation.png)


---

Thank you for considering —
**NandoLabs** 🚀
