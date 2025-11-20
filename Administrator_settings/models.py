from django.db import models
from django.contrib.auth.models import User


class User(models.Model):   
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=100) 
    password = models.CharField(max_length=255)  # New password field

    def __str__(self):
        return self.name


