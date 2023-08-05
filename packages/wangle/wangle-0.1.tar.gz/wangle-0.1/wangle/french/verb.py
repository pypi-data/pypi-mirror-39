verbs_that_conjugate_with_etre = [
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

def add_finite_verb(sentence, lemma, subject_id, mood="indicatif", tense="présent", informal=False, position=None, aux_lemma=None):
    verb = sentence.register_word(lemma)

    verb.set_tag("verb")
    verb.set_tag("main_verb")
    verb.set_tag("mood", value=mood)
    verb.set_tag("tense", value=tense)

    if informal:
        verb.set_tag("informal")

    aux, finite_verb, pp = None, None, None

    if mood == "indicatif":
        if tense in ["présent", "imparfait", "passé simple", "futur"]:
            verb.set_tag("conj_mood", value=mood)
            verb.set_tag("conj_tense", value=tense)
            finite_verb = verb
        if tense in ["passé composé", "plus-que-parfait", "passé anterieur", "futur anterieur"]:
            if aux_lemma is None:
                if verb.lemma in verbs_that_conjugate_with_etre:
                    aux_lemma = "être"
                else:
                    aux_lemma = "avoir"
            aux = sentence.register_word(aux_lemma)
            aux.set_tag("verb")
            aux.set_tag("conj_mood", value=mood)
            aux_tense = None
            if tense == "passé composé":
                aux_tense = "présent"
            elif tense == "plus-que-parfait":
                aux_tense = "imparfait"
            elif tense == "passé anterieur":
                aux_tense = "passé simple"
            elif tense == "futur anterieur":
                aux_tense = "futur"
            aux.set_tag("conj_tense", value=aux_tense)
            aux.set_tag("aux_for", value=verb.id)
            finite_verb = aux 
            verb.set_tag("past_participle")
            pp = verb
    elif mood == "conditionnel":
        if tense in ["présent"]:
            verb.set_tag("conj_mood", value=mood)
            verb.set_tag("conj_tense", value=tense)
            finite_verb = verb
        if tense == "passé":
            if aux_lemma is None:
                if verb.lemma in verbs_that_conjugate_with_etre:
                    aux_lemma = "être"
                else:
                    aux_lemma = "avoir"
            aux = sentence.register_word(aux_lemma)
            aux.set_tag("verb")
            aux.set_tag("conj_mood", value=mood)
            aux.set_tag("conj_tense", value="présent")
            aux.set_tag("aux_for", value=verb.id)
            finite_verb = aux 
            verb.set_tag("past_participle")
            pp = verb
    elif mood == "subjonctif":
        if tense in ["présent", "imparfait"]:
            verb.set_tag("conj_mood", value=mood)
            verb.set_tag("conj_tense", value=tense)
            finite_verb = verb
        if tense in ["passé", "plus-que-parfait"]:
            if aux_lemma is None:
                if verb.lemma in verbs_that_conjugate_with_etre:
                    aux_lemma = "être"
                else:
                    aux_lemma = "avoir"
            aux = sentence.register_word(aux_lemma)
            aux.set_tag("verb")
            aux.set_tag("conj_mood", value=mood)
            aux_tense = None
            if tense == "passé":
                aux_tense = "présent"
            elif tense == "plus-que-parfait":
                aux_tense = "passé simple"
            aux.set_tag("conj_tense", value=aux_tense)
            aux.set_tag("aux_for", value=verb.id)
            finite_verb = aux 
            verb.set_tag("past_participle")
            pp = verb

    if aux is not None:
        if position is not None:
            sentence.tokens.insert(position, aux)
            position += 1
        else:
            sentence.tokens.append(aux)

    if position is not None:
        sentence.tokens.insert(position, verb)
    else:
        sentence.tokens.append(verb)

    if finite_verb is not None:
        subj = sentence.words[subject_id]
        subj.set_tag("subject_for", verb.id)
        finite_verb.set_tag("finite_verb")
        finite_verb.set_tag("agrees_with", subj.id)

    if pp is not None and aux.lemma == "être":
        pp.set_tag("agrees_with", subj.id)

    return verb

def conjugate(sentence, verb):
    if verb.has_tag("finite_verb"):
        subject = None
        if verb.has_tag("agrees_with"):
            subject = sentence.words[verb.get_tag_value("agrees_with")]
            conj_group = None
            if subject.lemma == "je":
                conj_group = "S1"
            elif subject.lemma == "tu":
                conj_group = "S2"
            elif subject.lemma == "nous":
                conj_group = "P1"
            elif subject.lemma == "vous":
                conj_group = "P2"
            elif subject.has_tag("is_plural"):
                if subject.get_tag_value("is_plural"):
                    conj_group = "P3"
                else:
                    conj_group = "S3"

            if conj_group is not None:
                verb.set_tag("conj_group", value=conj_group)
                conj_mood = verb.get_tag_value("conj_mood")
                conj_tense = verb.get_tag_value("conj_tense")
                if conj_mood == "indicatif":
                    if conj_tense == "présent":
                        verb.inflection = sentence.conjugator.calculate_présent(verb.lemma, conj_group)
                    elif conj_tense == "imparfait":
                        verb.inflection = sentence.conjugator.calculate_imparfait(verb.lemma, conj_group)
                    elif conj_tense == "futur":
                        verb.inflection = sentence.conjugator.calculate_futur(verb.lemma, conj_group)
                    elif conj_tense == "passé simple":
                        verb.inflection = sentence.conjugator.calculate_passé_simple(verb.lemma, conj_group)
                elif conj_mood == "conditionnel":
                    if conj_tense == "présent":
                        verb.inflection = sentence.conjugator.calculate_conditionnel(verb.lemma, conj_group)
                elif conj_mood == "subjonctif":
                    if conj_tense == "présent":
                        verb.inflection = sentence.conjugator.calculate_subjonctif_présent(verb.lemma, conj_group)
    elif verb.has_tag("past_participle"):
        gender, is_plural = "masc", False
        if verb.has_tag("agrees_with"):
            word = sentence.words[verb.get_tag_value("agrees_with")]

            if not verb.has_tag("gender") and word.has_tag("gender"):
                gender = word.get_tag_value("gender")
                verb.set_tag("gender", value=gender)

            if not verb.has_tag("is_plural") and word.has_tag("is_plural"):
                is_plural = word.get_tag_value("is_plural")
                verb.set_tag("is_plural", value=is_plural)
        verb.inflection = sentence.conjugator.calculate_past_participle(verb.lemma, gender == "masc", is_plural)
