from django.contrib import admin
from .models import flashCardDeck  # Import your models

class FlashcardDeckAdmin(admin.ModelAdmin):
    filter_horizontal = ('words',)  # Improves selection UI

admin.site.register(flashCardDeck, FlashcardDeckAdmin)