from django.urls import path

from . import views

app_name = "ordergame"

urlpatterns = [
    path("", views.index, name="index"),
]