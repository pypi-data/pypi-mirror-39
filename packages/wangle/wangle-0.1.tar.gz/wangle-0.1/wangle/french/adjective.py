def add_adjective(sentence, lemma, nominal_word_id, position=None):
    word = sentence.register_word(lemma)

    word.set_tag("adjective")
    word.set_tag("modifies", nominal_word_id)
    word.set_tag("agrees_with", nominal_word_id)

    if position is not None:
        sentence.tokens.insert(position, word)
    else:
        sentence.tokens.append(word)

    return word

def decline(sentence, adjective):
    gender, is_plural = "masc", False
    if adjective.has_tag("agrees_with"):
        word = sentence.words[adjective.get_tag_value("agrees_with")]

        if not adjective.has_tag("gender") and word.has_tag("gender"):
            gender = word.get_tag_value("gender")
            adjective.set_tag("gender", value=gender)

        if not adjective.has_tag("is_plural") and word.has_tag("is_plural"):
            is_plural = word.get_tag_value("is_plural")
            adjective.set_tag("is_plural", value=is_plural)

    adjective.inflection = sentence.decliner.decline(adjective.lemma, gender == "masc", is_plural)
