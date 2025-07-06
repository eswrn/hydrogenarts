from django.db import models
from django.db import models
from django.db import models

from django.conf import settings

class ImageRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='image_requests', null=True, blank=True)
    prompt = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    process = models.CharField(max_length=32, blank=True, null=True, help_text="Process status or worker identifier")
    created_at = models.DateTimeField(auto_now_add=True)
    lastupdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prompt
