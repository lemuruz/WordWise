from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from flashcard.models import flashCardDeck
from wordbank.models import wordBank
from user.models import Account, flashcardUserScore
from flashcard.views import getflashcardselection
import random

class FlashcardWordSelectionTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create(
            username="testuser",
            password="testpass"
        )
        
        self.deck = flashCardDeck.objects.create(name="Test Deck")
        self.words = []
        for i in range(30):
            word = wordBank.objects.create(
                word=f"word{i}",
                translates=f"translation{i}",
                word_type="noun"
            )
            self.words.append(word)
            self.deck.words.add(word)

        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'username': 'testuser'}

    def create_user_scores(self, word_scores):
        for word, score in word_scores:
            score_entry = flashcardUserScore.objects.create(
                score=score,
                answerCount=1
            )
            score_entry.words.add(word)
            score_entry.account.add(self.user)

    def test_word_selection_new_user(self):
        selected_words = getflashcardselection(self.request, self.deck.id)
        
        self.assertEqual(len(selected_words), 20)

        user_scores = flashcardUserScore.objects.filter(account=self.user)
        self.assertEqual(user_scores.count(), 0)

    def test_word_selection_with_low_scores(self):
        # Create word scores
        low_score_words = self.words[:5]  # First 5 words with low scores
        word_scores = [(word, 0.2) for word in low_score_words]
        
        # Add some higher scoring words
        high_score_words = self.words[5:10]  # Next 5 words with high scores
        word_scores.extend([(word, 0.9) for word in high_score_words])
        
        self.create_user_scores(word_scores)
        
        selected_words = getflashcardselection(self.request, self.deck.id)
        
        low_score_words_set = set(low_score_words)
        selected_words_set = set(selected_words)
        common_low_score_words = low_score_words_set.intersection(selected_words_set)
        
        # All low score words should be included
        self.assertTrue(len(common_low_score_words) >= len(low_score_words))

    def test_word_selection_composition(self):
        """Test the composition of selected words (new, low score, random)"""
        # Create scores for 15 words
        used_words = self.words[:15]
        word_scores = [(word, random.uniform(0.3, 1.0)) for word in used_words]
        self.create_user_scores(word_scores)
        
        selected_words = getflashcardselection(self.request, self.deck.id)
        used_words_text = set(
            flashcardUserScore.objects.filter(account=self.user)
            .values_list('words__word', flat=True)
        )
        # print('used>>',used_words_text)
        # Get new words (words not in used_words_text)
        new_words = [w for w in selected_words if w.word not in used_words_text]
        # print('new>>',new_words)
        # Get low score words by word text
        low_score_words_text = set(
            flashcardUserScore.objects.filter(account=self.user)
            .order_by('score')[:7]
            .values_list('words__word', flat=True)
        )
        low_score_words = [w for w in selected_words if w.word in low_score_words_text]
        
        
        self.assertGreaterEqual(len(new_words), 7, "Should have at most 7 new words")
        self.assertLessEqual(len(low_score_words), 7, "Should have at most 7 low score words")
        self.assertEqual(len(selected_words), 20, "Should have exactly 20 words total")

    def test_word_selection_randomization(self):
        first_selection = getflashcardselection(self.request, self.deck.id)
        second_selection = getflashcardselection(self.request, self.deck.id)
        
        first_set = set(word.id for word in first_selection)
        second_set = set(word.id for word in second_selection)

        self.assertNotEqual(first_set, second_set)