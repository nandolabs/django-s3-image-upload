from rest_framework import serializers
from .models import Image
from users.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for listing and retrieving images.
    """
    user = UserSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'user', 'image', 'image_url', 'title', 'description',
                  'uploaded_at', 'updated_at')
        read_only_fields = ('id', 'user', 'uploaded_at', 'updated_at')

    def get_image_url(self, obj):
        return obj.image_url


class ImageUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading images.
    """
    class Meta:
        model = Image
        fields = ('id', 'image', 'title', 'description', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at')

    def validate_image(self, value):
        # Validate image file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "Image file too large. Size should not exceed 10 MB."
            )

        # Validate image file type
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"Unsupported file extension. Allowed types: {', '.join(allowed_extensions)}"
            )

        return value
