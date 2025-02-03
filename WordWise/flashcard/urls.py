from django.urls import path, include
from . import views

app_name = "flashcard"

urlpatterns = [
    path("", views.index, name="index"),
    path('end/', views.flashcardend, name='flashcardend'),
    path('flashcard/play/<int:deck_id>/', views.flashcardplay, name="flashcardplay"),
]