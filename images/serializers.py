from rest_framework import serializers
from .models import ImageItem


class ImageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageItem
        fields = ['id', 'title', 'description', 'image_url', 'cloudinary_public_id', 'uploaded_at']
        read_only_fields = ('image_url', 'cloudinary_public_id', 'uploaded_at')


class ImageItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageItem
        fields = ['id', 'title', 'description', 'image_url']