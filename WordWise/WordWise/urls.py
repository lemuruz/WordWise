from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('',include("menu.urls")),
    path("flashcard/", include("flashcard.urls")),
    path("hangman/",include("hangman.urls")),
    path("ordergame/",include("ordergame.urls")),
    path("user/",include("user.urls")),
    path("admin/", admin.site.urls)
]
