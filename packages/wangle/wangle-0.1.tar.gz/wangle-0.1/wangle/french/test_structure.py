import unittest

from .structure import Sentence
from .pronoun import add_subject_pronoun
from .verb import add_finite_verb

class Tests(unittest.TestCase):

    def test_simple_contraction(self):
        s = Sentence()
        p = add_subject_pronoun(s, 'je')
        v = add_finite_verb(s, 'aimer', p.id)
        s.inflect()
        s.contract()
        self.assertEqual(str(s), "j'aime")
