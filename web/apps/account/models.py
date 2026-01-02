import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Create your models here.
def profile_photo_path(instance, filename):
    ext = os.path.splitext(filename)[1]  # .jpg, .png
    filename = f"{uuid.uuid4().hex}{ext}"
    return f"photo/profile/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=55)
    nik = models.CharField(max_length=25)
    position = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=20)
    foto = models.ImageField(
        upload_to=profile_photo_path, 
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png"])
        ],
        blank=True, 
        null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# Create your models here.
def status_photo_path(instance, filename):
    ext = os.path.splitext(filename)[1]  # .jpg, .png
    filename = f"{uuid.uuid4().hex}{ext}"
    return f"photo/status/{filename}"

class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="status")
    message = models.TextField()
    foto = models.ImageField(
        upload_to=status_photo_path,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png"])
        ],
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.profile.name)