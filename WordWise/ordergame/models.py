from django.db import models
from user.models import Account

# Create your models here.
class sentences(models.Model):
    sentence = models.TextField()

    def __str__(self):
        return self.sentence
    
class userScore(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    score = models.FloatField()
    times = models.IntegerField()

    def __str__(self):
        return self.user.username