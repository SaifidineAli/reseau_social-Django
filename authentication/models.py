from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Photo de profil', blank=True, null=True)
    
    IMAGE_MAX_SIZE = (800, 800)
    
    def resize_image(self):
        if self.avatar:
            image = Image.open(self.avatar)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.avatar.path)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
        
    def __str__(self):
        return self.username