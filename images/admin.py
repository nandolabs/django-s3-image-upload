from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'uploaded_at')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('title', 'description', 'user__email')
    readonly_fields = ('uploaded_at', 'updated_at')
    ordering = ('-uploaded_at',)
