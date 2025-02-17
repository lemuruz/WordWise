from django.urls import path

from . import views

app_name = "ordergame"

urlpatterns = [
    path("game/", views.game, name="game"),
    path("test/", views.test, name="test"),
    path("addsentence/", views.add_sentence, name="addSentence"),
    path("addscore/", views.add_score, name="addscore")
]