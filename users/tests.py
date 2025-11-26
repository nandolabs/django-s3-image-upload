import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserAuthentication:
    """Tests for user authentication endpoints."""

    def test_signup_success(self, api_client, user_data):
        """Test successful user registration."""
        response = api_client.post('/api/auth/signup/', user_data)

        assert response.status_code == 201
        assert 'user' in response.data
        assert 'tokens' in response.data
        assert response.data['user']['email'] == user_data['email']
        assert 'access' in response.data['tokens']
        assert 'refresh' in response.data['tokens']

    def test_signup_password_mismatch(self, api_client, user_data):
        """Test signup with password mismatch."""
        user_data['password2'] = 'DifferentPassword'
        response = api_client.post('/api/auth/signup/', user_data)

        assert response.status_code == 400
        assert 'password' in response.data

    def test_signup_duplicate_email(self, api_client, user_data, create_user):
        """Test signup with duplicate email."""
        response = api_client.post('/api/auth/signup/', user_data)

        assert response.status_code == 400

    def test_signup_missing_fields(self, api_client):
        """Test signup with missing required fields."""
        response = api_client.post('/api/auth/signup/', {
            'email': 'test@example.com'
        })

        assert response.status_code == 400

    def test_login_success(self, api_client, create_user, user_data):
        """Test successful user login."""
        response = api_client.post('/api/auth/login/', {
            'email': user_data['email'],
            'password': user_data['password']
        })

        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_invalid_credentials(self, api_client, create_user):
        """Test login with invalid credentials."""
        response = api_client.post('/api/auth/login/', {
            'email': 'testuser@example.com',
            'password': 'WrongPassword'
        })

        assert response.status_code == 401

    def test_login_missing_fields(self, api_client):
        """Test login with missing fields."""
        response = api_client.post('/api/auth/login/', {
            'email': 'test@example.com'
        })

        assert response.status_code == 400
