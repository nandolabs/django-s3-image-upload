from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Image
from .serializers import ImageSerializer, ImageUploadSerializer


@extend_schema(tags=['Images'])
class ImageListView(generics.ListAPIView):
    """
    List all images uploaded by the authenticated user.

    Returns a list of all images belonging to the current user,
    including image URLs and metadata.
    """
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List user's images",
        description="Retrieve all images uploaded by the authenticated user"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


@extend_schema(tags=['Images'])
class ImageUploadView(generics.CreateAPIView):
    """
    Upload a new image to S3 or local storage.

    Accepts multipart/form-data with an image file.
    Maximum file size: 10MB. Allowed formats: jpg, jpeg, png, gif, webp.
    """
    serializer_class = ImageUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary="Upload image",
        description="Upload a new image file with optional title and description. Max size: 10MB",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {'type': 'string', 'format': 'binary'},
                    'title': {'type': 'string'},
                    'description': {'type': 'string'},
                }
            }
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Images'])
class ImageDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific image.

    Returns image metadata and URL. Only accessible to the image owner.
    """
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get image detail",
        description="Retrieve details of a specific image (owner only)",
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Image ID'
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


@extend_schema(tags=['Images'])
class ImageDeleteView(generics.DestroyAPIView):
    """
    Delete an image.

    Permanently deletes an image from storage. Only accessible to the image owner.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Delete image",
        description="Delete an image permanently (owner only)",
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Image ID'
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

