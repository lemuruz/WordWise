from django.test import TestCase
from .views import get_random_sentence

# Create your tests here.
class WordBankTests(TestCase):

    def test_get_random_sentence(self):
        print(get_random_sentence())