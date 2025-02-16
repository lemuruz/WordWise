from django.urls import path
from . import views


app_name = "menu"

urlpatterns = [
    path("", views.index, name="index"),  # Menu page
    path("add-word/", views.add_word, name="add_word"),
    
]