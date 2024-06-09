from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Les champs supplémentaires, si nécessaire
    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:20]

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
    
    def __str__(self):
        return f"{self.follower} follows {self.followed}"

class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.text
