from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    """
    Register a new user and receive JWT authentication tokens.

    Creates a new user account with email-based authentication.
    Returns the created user details along with JWT access and refresh tokens.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Registration",
        description="Register a new user account and receive JWT tokens for authentication",
        request=UserRegistrationSerializer,
        responses={
            201: UserSerializer,
        },
        examples=[
            OpenApiExample(
                'Registration Example',
                value={
                    'email': 'user@example.com',
                    'username': 'johndoe',
                    'password': 'SecurePassword123',
                    'password2': 'SecurePassword123'
                },
                request_only=True,
            ),
        ],
        tags=['Authentication']
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

