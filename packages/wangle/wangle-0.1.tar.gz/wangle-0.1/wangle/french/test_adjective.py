import unittest

from wangle.french.structure import Sentence
from wangle.french.pronoun import add_subject_pronoun
from wangle.french.verb import add_finite_verb
from wangle.french.adjective import add_adjective

class Tests(unittest.TestCase):

    def test_adjective_derives_declension(self):
        for gender in [None, "masc", "fem"]:
            for is_plural in [None, True, False]:
                with self.subTest(gender=gender, is_plural=is_plural):
                    s = Sentence()
                    p = add_subject_pronoun(s, "vous", gender=gender, is_plural=is_plural)
                    if gender is None:
                        self.assertFalse(p.has_tag("gender"))
                    else:
                        self.assertEqual(p.get_tag_value("gender"), gender)
                    if is_plural is None:
                        self.assertFalse(p.has_tag("is_plural"))
                    else:
                        self.assertEqual(p.get_tag_value("is_plural"), is_plural)
                    v = add_finite_verb(s, "être", p.id)
                    adj = add_adjective(s, "content", p.id)

                    s.inflect()
                    if gender is None:
                        self.assertFalse(adj.has_tag("gender"))
                    else:
                        self.assertEqual(adj.get_tag_value("gender"), gender)
                    if is_plural is None:
                        self.assertFalse(adj.has_tag("is_plural"))
                    else:
                        self.assertEqual(adj.get_tag_value("is_plural"), is_plural)

    def test_adjective_declension(self):
        declensions = [
            (None, False, "vous êtes content"),
            (None, True, "vous êtes contents"),
            ("masc", None, "vous êtes content"),
            ("fem", None, "vous êtes contente"),
            ("masc", False, "vous êtes content"),
            ("fem", False, "vous êtes contente"),
            ("masc", True, "vous êtes contents"),
            ("fem", True, "vous êtes contentes"),
        ]
        for gender, is_plural, declension in declensions:
            with self.subTest(gender=gender, is_plural=is_plural):
                s = Sentence()
                p = add_subject_pronoun(s, "vous", gender=gender, is_plural=is_plural)
                v = add_finite_verb(s, "être", p.id)
                adj = add_adjective(s, "content", p.id)
                s.inflect()
                self.assertEqual(str(s), declension)
