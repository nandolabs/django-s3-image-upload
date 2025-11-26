from django.urls import path
from .views import (
    ImageListView,
    ImageUploadView,
    ImageDetailView,
    ImageDeleteView,
)

urlpatterns = [
    path('', ImageListView.as_view(), name='image-list'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
    path('<int:pk>/delete/', ImageDeleteView.as_view(), name='image-delete'),
]
