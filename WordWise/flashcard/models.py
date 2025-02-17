from django.db import models
from wordbank.models import wordBank

class flashCardDeck(models.Model):
    name = models.CharField(max_length=100, unique=True)
    words = models.ManyToManyField(wordBank)

    def __str__(self):
        return self.name
    
