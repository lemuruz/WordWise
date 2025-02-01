from django.db import models

# Create your models here.
class wordBank(models.Model):
    word = models.CharField(max_length=100, null=False)
    word_type = models.CharField(max_length=50, null=False)
    meaning = models.TextField()
    translates = models.CharField(max_length=100, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['word', 'word_type'], name='unique_word')
        ]

    def __str__(self):
        return self.word