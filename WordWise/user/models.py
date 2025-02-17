from django.db import models
from flashcard.models import flashCardDeck
from wordbank.models import wordBank
class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    flashcard = models.ManyToManyField(flashCardDeck)  # Adjust based on needs

    def __str__(self):
        return self.username
    
class flashcardUserScore(models.Model):
    words = models.ManyToManyField(wordBank)
    account = models.ManyToManyField(Account)
    score = models.FloatField()
    answerCount = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['words', 'account'], name='unique')
        ]