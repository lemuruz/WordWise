from django.test import TestCase
from .views import test_get_random_sentence
from .models import sentences,orderUserScore
from user.models import Account

# Create your tests here.
class test_get_object(TestCase):
    def setUp(self):
        self.user = Account.objects.create(username="James",password="1234")
        self.done_sentence = sentences.objects.create(sentence="I played this sentence.")
        self.user_played = orderUserScore.objects.create(user=self.user, sentence=self.done_sentence, score=1, times=1)
        self.new_sentence = sentences.objects.create(sentence="I haven't play this sentence.")

    def test_get_user_from_done(self):
        username = self.user.username
        retsen = test_get_random_sentence(master=username, number=0.1) #get from done sentence
        self.assertEqual(retsen, "I played this sentence.")

    def test_get_new_sentence_dont_have_user(self):
        retsen = test_get_random_sentence(master="No user", number=0.1)
        self.assertEqual(retsen, "I haven't play this sentence.")

    def test_get_new_sentence_high_random(self):
        username = self.user.username
        retsen = test_get_random_sentence(master=username, number=0.7)
        self.assertEqual(retsen, "I haven't play this sentence.")