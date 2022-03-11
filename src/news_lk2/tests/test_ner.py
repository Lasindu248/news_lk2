
import unittest

from news_lk2.analysis import ner
from news_lk2.analysis.ner import POS


class TestNER(unittest.TestCase):
    def test_get_combined_nlp(self):
        for [text, expected_combined_nlp] in [
            [
                '''
                    Sri Lanka is an island in the Indian Ocean.
                    Its capital city is Colombo.
                    Sri Lanka has 9 provinces.

                ''',
                [
                    {'pos': POS.NE, 'text': 'Sri Lanka'},
                    {'pos': POS.OTHER, 'text': 'is an island in the'},
                    {'pos': POS.NE, 'text': 'Indian Ocean'},
                    {'pos': POS.PUNCT, 'text': '.'},
                    {'pos': POS.OTHER, 'text': 'Its capital city is'},
                    {'pos': POS.NE, 'text': 'Colombo'},
                    {'pos': POS.PUNCT, 'text': '.'},
                    {'pos': POS.NE, 'text': 'Sri Lanka'},
                    {'pos': POS.OTHER, 'text': 'has'},
                    {'pos': POS.NUM, 'text': '9'},
                    {'pos': POS.OTHER, 'text': 'provinces'},
                    {'pos': POS.PUNCT, 'text': '.'},
                ],
            ]
        ]:
            self.assertEqual(expected_combined_nlp, ner.get_combined_nlp(text))


if __name__ == '__main__':
    unittest.main()
