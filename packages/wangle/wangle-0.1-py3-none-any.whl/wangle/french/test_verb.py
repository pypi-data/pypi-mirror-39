import unittest

from .structure import Sentence
from .pronoun import add_subject_pronoun
from .verb import add_finite_verb

class Tests(unittest.TestCase):
    def test_single_tense_labelling(self):
        test_case = [
            ("indicatif", "présent"),
            ("indicatif", "imparfait"),
            ("indicatif", "passé simple"),
            ("indicatif", "futur"),
            ("conditionnel", "présent"),
            ("subjonctif", "présent"),
            ("subjonctif", "imparfait"),
        ]
        for mood, tense in test_case:
            with self.subTest(mood=mood, tense=tense):
                s = Sentence()
                p = add_subject_pronoun(s, "je")
                lemma = "aimer"
                v = add_finite_verb(s, lemma, p.id, mood=mood, tense=tense)
                s.inflect()

                self.assertEqual(v.lemma, lemma)
                self.assertTrue(v.has_tag("verb"))
                self.assertTrue(v.has_tag("finite_verb"))
                self.assertTrue(v.has_tag("main_verb"))
                self.assertEqual(v.get_tag_value("mood"), mood)
                self.assertEqual(v.get_tag_value("tense"), tense)
                self.assertEqual(v.get_tag_value("conj_mood"), mood)
                self.assertEqual(v.get_tag_value("conj_tense"), tense)

    def test_single_aux_compound_tense_labelling(self):
        test_case = [
            ("indicatif", "passé composé", "présent"),
            ("indicatif", "plus-que-parfait", "imparfait"),
            ("indicatif", "passé anterieur", "passé simple"),
            ("indicatif", "futur anterieur", "futur"),
            ("conditionnel", "passé", "présent"),
            ("subjonctif", "passé", "présent"),
            ("subjonctif", "plus-que-parfait", "passé simple"),
        ]
        for mood, tense, aux_tense in test_case:
            with self.subTest(mood=mood, tense=tense):
                s = Sentence()
                p = add_subject_pronoun(s, "je")
                lemma = "aimer"
                v = add_finite_verb(s, lemma, p.id, mood=mood, tense=tense)
                s.inflect()

                aux = s.tokens[1]
                pp = s.tokens[2]

                self.assertEqual(aux.lemma, "avoir")
                self.assertTrue(aux.has_tag("verb"))
                self.assertTrue(aux.has_tag("finite_verb"))
                self.assertEqual(aux.get_tag_value("conj_mood"), mood)
                self.assertEqual(aux.get_tag_value("conj_tense"), aux_tense)
                self.assertEqual(aux.get_tag_value("aux_for"), pp.id)
                self.assertFalse(aux.has_tag("main_verb"))

                self.assertEqual(pp.lemma, lemma)
                self.assertTrue(pp.has_tag("verb"))
                self.assertTrue(pp.has_tag("main_verb"))
                self.assertEqual(pp.get_tag_value("mood"), mood)
                self.assertEqual(pp.get_tag_value("tense"), tense)
                self.assertTrue(pp.has_tag("past_participle"))
                self.assertFalse(pp.has_tag("finite_verb"))

    def test_vandertramp_verbs_use_être_aux(self):
        test_cases = [
            ("indicatif", "passé composé", "présent"),
            ("indicatif", "plus-que-parfait", "imparfait"),
            ("indicatif", "passé anterieur", "passé simple"),
            ("indicatif", "futur anterieur", "futur"),
            ("conditionnel", "passé", "présent"),
            ("subjonctif", "passé", "présent"),
            ("subjonctif", "plus-que-parfait", "passé simple"),
        ]
        vandertramp_lemmas = [
            "devenir", 
            "revenir,",
            "monter",
            "rester",
            "sortir",
            "venir",
            "aller",
            "naître",
            "descendre",
            "entrer",
            "retourner",
            "tomber",
            "rentrer",
            "arriver",
            "mourir",
            "partir"
        ]
        for lemma in vandertramp_lemmas:
            for mood, tense, aux_tense in test_cases:
                with self.subTest(mood=mood, tense=tense):
                    s = Sentence()
                    p = add_subject_pronoun(s, "je")
                    v = add_finite_verb(s, lemma, p.id, mood=mood, tense=tense)
                    s.inflect()

                    aux = s.tokens[1]

                    self.assertEqual(aux.lemma, "être")

    def test_être_aux_override(self):
        test_cases = [
            ("indicatif", "passé composé", "présent"),
            ("indicatif", "plus-que-parfait", "imparfait"),
            ("indicatif", "passé anterieur", "passé simple"),
            ("indicatif", "futur anterieur", "futur"),
            ("conditionnel", "passé", "présent"),
            ("subjonctif", "passé", "présent"),
            ("subjonctif", "plus-que-parfait", "passé simple"),
        ]
        for mood, tense, aux_tense in test_cases:
            with self.subTest(mood=mood, tense=tense):
                s = Sentence()
                p = add_subject_pronoun(s, "je")
                v = add_finite_verb(s, "demeurer", p.id, mood=mood, tense=tense)
                s.inflect()

                aux = s.tokens[1]

                self.assertEqual(aux.lemma, "avoir")
        for mood, tense, aux_tense in test_cases:
            with self.subTest(mood=mood, tense=tense):
                s = Sentence()
                p = add_subject_pronoun(s, "je")
                v = add_finite_verb(s, "demeurer", p.id, mood=mood, tense=tense, aux_lemma="être")
                s.inflect()

                aux = s.tokens[1]

                self.assertEqual(aux.lemma, "être")

    def test_présent_inflection(self):
        conjugations = [
            ("je", "je suis"),
            ("tu", "tu es"),
            ("il", "il est"),
            ("nous", "nous sommes"),
            ("vous", "vous êtes"),
            ("ils", "ils sont"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'être', p.id)
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)
                
    def test_imparfait_inflection(self):
        conjugations = [
            ("je", "j'étais"),
            ("tu", "tu étais"),
            ("il", "il était"),
            ("nous", "nous étions"),
            ("vous", "vous étiez"),
            ("ils", "ils étaient"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'être', p.id, tense="imparfait")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_futur_inflection(self):
        conjugations = [
            ("je", "je serai"),
            ("tu", "tu seras"),
            ("il", "il sera"),
            ("nous", "nous serons"),
            ("vous", "vous serez"),
            ("ils", "ils seront"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'être', p.id, tense="futur")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_passé_simple_inflection(self):
        conjugations = [
            ("je", "je fus"),
            ("tu", "tu fus"),
            ("il", "il fut"),
            ("nous", "nous fûmes"),
            ("vous", "vous fûtes"),
            ("ils", "ils furent"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'être', p.id, tense="passé simple")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_passé_composé_inflection(self):
        conjugations = [
            ("je", "j'ai aimé"),
            ("tu", "tu as aimé"),
            ("il", "il a aimé"),
            ("nous", "nous avons aimé"),
            ("vous", "vous avez aimé"),
            ("ils", "ils ont aimé"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'aimer', p.id, tense="passé composé")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_plus_que_parfait_inflection(self):
        conjugations = [
            ("je", "j'avais aimé"),
            ("tu", "tu avais aimé"),
            ("il", "il avait aimé"),
            ("nous", "nous avions aimé"),
            ("vous", "vous aviez aimé"),
            ("ils", "ils avaient aimé"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'aimer', p.id, tense="plus-que-parfait")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_futur_anterieur_inflection(self):
        conjugations = [
            ("je", "j'aurai aimé"),
            ("tu", "tu auras aimé"),
            ("il", "il aura aimé"),
            ("nous", "nous aurons aimé"),
            ("vous", "vous aurez aimé"),
            ("ils", "ils auront aimé"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'aimer', p.id, tense="futur anterieur")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_passé_anterieur_inflection(self):
        conjugations = [
            ("je", "j'eus aimé"),
            ("tu", "tu eus aimé"),
            ("il", "il eut aimé"),
            ("nous", "nous eûmes aimé"),
            ("vous", "vous eûtes aimé"),
            ("ils", "ils eurent aimé"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'aimer', p.id, tense="passé anterieur")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_conditionnel_présent_inflection(self):
        conjugations = [
            ("je", "je serais"),
            ("tu", "tu serais"),
            ("il", "il serait"),
            ("nous", "nous serions"),
            ("vous", "vous seriez"),
            ("ils", "ils seraient"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'être', p.id, mood="conditionnel", tense="présent")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_conditionnel_passé_inflection(self):
        conjugations = [
            ("je", "j'aurais aimé"),
            ("tu", "tu aurais aimé"),
            ("il", "il aurait aimé"),
            ("nous", "nous aurions aimé"),
            ("vous", "vous auriez aimé"),
            ("ils", "ils auraient aimé"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'aimer', p.id, mood="conditionnel", tense="passé")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_subjonctif_présent_inflection(self):
        conjugations = [
            ("je", "je sois"),
            ("tu", "tu sois"),
            ("il", "il soit"),
            ("nous", "nous soyons"),
            ("vous", "vous soyez"),
            ("ils", "ils soient"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'être', p.id, mood="subjonctif", tense="présent")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_conditionnel_passé_inflection(self):
        conjugations = [
            ("je", "j'aie aimé"),
            ("tu", "tu aies aimé"),
            ("il", "il ait aimé"),
            ("nous", "nous ayons aimé"),
            ("vous", "vous ayez aimé"),
            ("ils", "ils aient aimé"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'aimer', p.id, mood="subjonctif", tense="passé")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_past_participle_agrees_with_subject_for_transitive_conjugation_with_etre_aux(self):
        declensions = [
            (None, False, "vous êtes allé"),
            (None, True, "vous êtes allés"),
            ("masc", None, "vous êtes allé"),
            ("fem", None, "vous êtes allée"),
            ("masc", False, "vous êtes allé"),
            ("fem", False, "vous êtes allée"),
            ("masc", True, "vous êtes allés"),
            ("fem", True, "vous êtes allées"),
        ]
        for gender, is_plural, result in declensions:
            with self.subTest(gender=gender, is_plural=is_plural):
                s = Sentence()
                p = add_subject_pronoun(s, "vous", gender=gender, is_plural=is_plural)
                v = add_finite_verb(s, "aller", p.id, tense="passé composé")
                s.inflect()
                self.assertEqual(str(s), result)
