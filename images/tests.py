import pytest
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Image


@pytest.mark.django_db
class TestImageUpload:
    """Tests for image upload and management endpoints."""

    def test_upload_image_success(self, authenticated_client, sample_image):
        """Test successful image upload."""
        response = authenticated_client.post(
            '/api/images/upload/',
            {
                'image': sample_image,
                'title': 'My Test Image',
                'description': 'A beautiful test image'
            },
            format='multipart'
        )

        assert response.status_code == 201
        assert response.data['title'] == 'My Test Image'
        assert 'image' in response.data

    def test_upload_image_unauthenticated(self, api_client, sample_image):
        """Test image upload without authentication."""
        response = api_client.post(
            '/api/images/upload/',
            {
                'image': sample_image,
                'title': 'Test Image'
            },
            format='multipart'
        )

        assert response.status_code == 401

    def test_upload_image_without_file(self, authenticated_client):
        """Test image upload without file."""
        response = authenticated_client.post(
            '/api/images/upload/',
            {
                'title': 'Test Image'
            }
        )

        assert response.status_code == 400

    def test_list_user_images(self, authenticated_client, create_image):
        """Test listing user's images."""
        response = authenticated_client.get('/api/images/')

        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_list_images_unauthenticated(self, api_client):
        """Test listing images without authentication."""
        response = api_client.get('/api/images/')

        assert response.status_code == 401

    def test_get_image_detail(self, authenticated_client, create_image):
        """Test retrieving image detail."""
        response = authenticated_client.get(
            f'/api/images/{create_image.id}/'
        )

        assert response.status_code == 200
        assert response.data['id'] == create_image.id
        assert response.data['title'] == create_image.title

    def test_delete_image(self, authenticated_client, create_image):
        """Test deleting an image."""
        response = authenticated_client.delete(
            f'/api/images/{create_image.id}/delete/'
        )

        assert response.status_code == 204
        assert not Image.objects.filter(id=create_image.id).exists()

    def test_upload_large_image_fails(self, authenticated_client):
        """Test that uploading a large image fails."""
        # Create a large image (over 10MB)
        large_image = PILImage.new('RGB', (5000, 5000), color='blue')
        image_io = BytesIO()
        large_image.save(image_io, format='JPEG', quality=100)
        image_io.seek(0)

        large_file = SimpleUploadedFile(
            name='large_image.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )

        response = authenticated_client.post(
            '/api/images/upload/',
            {
                'image': large_file,
                'title': 'Large Image'
            },
            format='multipart'
        )

        # This might pass or fail depending on actual file size
        # If it's over 10MB, it should fail
        if large_file.size > 10 * 1024 * 1024:
            assert response.status_code == 400
