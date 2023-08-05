import unittest
import os

from . import conjugator
from . import decliner

class Tests(unittest.TestCase):
    def test_adjectives(self):
        full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data', 'adjective_declensions.txt')
        with open(full_path) as fin:
            for line in fin:
                if len(line) > 0:
                    declensions = line.strip().split(',')
                    lemma = declensions[0]
                    with self.subTest(lemma=lemma):
                        i = 0
                        for plural in [False, True]:
                            for masculine in [True, False]:
                                expected = declensions[i]
                                calculated = decliner.decline(lemma, masculine, plural)
                                self.assertEqual(calculated, expected, msg=('the masculine=%s, plural=%s declension should be %s, not %s' % (masculine, plural, expected, calculated)))
                                i += 1
