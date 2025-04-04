from django.db import models
import re

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def sanitizar_username(self):
        self.username = self.username.lower()
        self.username = " ".join(self.username.split())
        self.username.strip()
        self.username = re.sub(r'[^a-zA-ZÀ-ÿ0-9\s]', '', self.username)


    def save(self, *args, **kwargs):
        self.sanitizar_username()
        super().save(*args, **kwargs)