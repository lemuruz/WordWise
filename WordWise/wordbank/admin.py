from django.contrib import admin

from .models import wordBank

class SearchWord(admin.ModelAdmin):
    search_fields = ['word',]
admin.site.register(wordBank,SearchWord)