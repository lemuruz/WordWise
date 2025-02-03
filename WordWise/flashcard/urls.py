from django.urls import path, include
from . import views

app_name = "flashcard"

urlpatterns = [
    path("", views.index, name="index"),
    # path('next_word/', views.next_word, name='next_word'),
    path('flashcard/play/<int:deck_id>/', views.flashcardplay, name="flashcardplay"),
]