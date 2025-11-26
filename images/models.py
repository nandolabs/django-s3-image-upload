import uuid
from django.db import models
from django.conf import settings


def upload_to(instance, filename):
    """
    Generate unique filename for uploaded images.
    Format: images/{user_id}/{uuid}_{original_filename}
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}_{filename}"
    return f'images/{instance.user.id}/{filename}'


class Image(models.Model):
    """
    Model for storing uploaded images with S3 or local storage.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to=upload_to)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.user.email} - {self.title or 'Untitled'}"

    @property
    def image_url(self):
        """
        Return the full URL of the image.
        """
        if self.image:
            return self.image.url
        return None

