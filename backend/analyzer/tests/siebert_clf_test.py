import unittest
from siebert_clf import analyzer

test_10_strings = (
    "I absolutely love this new phone; it's amazing in every way!",
    "This is the worst movie I have ever seen. Totally disappointing.",
    "I'm not sure how I feel about the new policy changes.",
    "The weather today is just okay, nothing special.",
    "This restaurant is fantastic - the best meal I've had in years!",
    "I'm so frustrated with the delayed flight schedules.",
    "The book was decent, but I've read better ones.",
    "I'm feeling very happy and excited about the upcoming concert!",
    "The service at the bank today was absolutely terrible.",
    "It's a regular day, nothing much happening."
)

test_10_expected = [1, -1, -1, -1, 1, -1, -1, 1, -1, -1]


class TestSentimentFunction(unittest.TestCase):

    def setUp(self):
        analyzer.init()

    def test_sentiment_positive(self):
        self.assertEqual([1], analyzer.get_siebert_clf_score(("this is great!",)))

    def test_sentiment_negative(self):
        self.assertEqual([-1], analyzer.get_siebert_clf_score(("this sucks.",)))

    def test_sentiment_empty_list(self):
        self.assertEqual([0], analyzer.get_siebert_clf_score(("",)))

    def test_sentiment_non_string_input(self):
        with self.assertRaises(TypeError):
            analyzer.get_siebert_clf_score((123, None))

    def test_10_strings(self):
        self.assertEqual(test_10_expected, analyzer.get_siebert_clf_score(test_10_strings))


if __name__ == '__main__':
    unittest.main()
