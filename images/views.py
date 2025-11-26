from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Image
from .serializers import ImageSerializer, ImageUploadSerializer


class ImageListView(generics.ListAPIView):
    """
    View to list all images for the authenticated user.
    """
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


class ImageUploadView(generics.CreateAPIView):
    """
    View to upload a new image.
    """
    serializer_class = ImageUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a specific image.
    """
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


class ImageDeleteView(generics.DestroyAPIView):
    """
    View to delete a specific image.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)
