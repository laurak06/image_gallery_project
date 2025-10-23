from django.db import models

from django.db import models

class ImageItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_url = models.CharField(max_length=500)  # url, возвращаемый облаком
    cloudinary_public_id = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

