def add_subject_pronoun(sentence, lemma, gender=None, is_plural=None, position=None):
    word = sentence.register_word(lemma)

    word.set_tag("pronoun")

    if lemma in ["il", "ils"]:
        word.set_tag("gender", value="masc")
    elif lemma in ["elle", "elles"]:
        word.set_tag("gender", value="fem")
    elif gender is not None:
        word.set_tag("gender", value=gender)

    if lemma in ["je", "tu", "il", "elle", "on", "ça", "cela", "ceci"]:
        word.set_tag("is_plural", value=False)
    elif lemma in ["nous", "ils", "elles"]:
        word.set_tag("is_plural", value=True)
    elif is_plural is not None:
        word.set_tag("is_plural", value=is_plural)

    if position is not None:
        sentence.tokens.insert(position, word)
    else:
        sentence.tokens.append(word)

    return word
