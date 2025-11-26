import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from images.models import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
from io import BytesIO

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client instance."""
    return APIClient()


@pytest.fixture
def user_data():
    """Return sample user data."""
    return {
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'TestPassword123',
        'password2': 'TestPassword123'
    }


@pytest.fixture
def create_user(db, user_data):
    """Create and return a test user."""
    user = User.objects.create_user(
        email=user_data['email'],
        username=user_data['username'],
        password=user_data['password']
    )
    return user


@pytest.fixture
def authenticated_client(api_client, create_user, user_data):
    """Return an authenticated API client."""
    response = api_client.post('/api/auth/login/', {
        'email': user_data['email'],
        'password': user_data['password']
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def sample_image():
    """Generate a sample image file for testing."""
    # Create a simple image using PIL
    image = PILImage.new('RGB', (100, 100), color='red')
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)

    return SimpleUploadedFile(
        name='test_image.jpg',
        content=image_io.read(),
        content_type='image/jpeg'
    )


@pytest.fixture
def create_image(db, create_user, sample_image):
    """Create and return a test image."""
    image = Image.objects.create(
        user=create_user,
        image=sample_image,
        title='Test Image',
        description='A test image'
    )
    return image
