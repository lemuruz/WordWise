from django.db import models

# Create your models here.
class sentences(models.Model):
    sentence = models.TextField()

    def __str__(self):
        return self.sentence