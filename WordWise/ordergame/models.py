from django.db import models
from user.models import Account

# Create your models here.
class sentences(models.Model):
    sentence = models.TextField()

    def __str__(self):
        return self.sentence
    
class orderUserScore(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)  # Link to a single user
    sentence = models.ForeignKey(sentences, on_delete=models.CASCADE)  # Link to a single sentence
    score = models.FloatField()
    times = models.IntegerField()

    class Meta:
        unique_together = ('user', 'sentence')  # Enforce unique combination of user and sentence

    def __str__(self):
        return f"{self.user.username} - {self.sentence.sentence}"
