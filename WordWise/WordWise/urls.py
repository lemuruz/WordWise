from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('',include("menu.urls")),
    path("flashcard/", include("flashcard.urls")),
    path("crossword/",include("crossword.urls")),
    path("ordergame/",include("ordergame.urls")),
]
