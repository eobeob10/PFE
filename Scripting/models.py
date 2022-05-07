from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)


class scan_list (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.description


class Documents (models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
