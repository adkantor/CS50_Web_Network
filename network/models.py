from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followed_by = models.ManyToManyField('self', blank=True, related_name='following', symmetrical=False)


class Post(models.Model):
    """ Class to represent a post. """
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    content = models.TextField()
    liked_by = models.ManyToManyField(User, blank=True, related_name='liked_posts')

    