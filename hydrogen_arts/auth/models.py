from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # You can extend with more fields if needed
    pass

class PromptLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.prompt[:30]}..."
