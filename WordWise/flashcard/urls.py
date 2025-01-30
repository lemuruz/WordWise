from django.urls import path

from . import views

app_name = "flashcard"

urlpatterns = [
    path("", views.index, name="index"),
]