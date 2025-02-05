from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    flashcard = models.JSONField(default=dict)  # Adjust based on needs

    def __str__(self):
        return self.username
