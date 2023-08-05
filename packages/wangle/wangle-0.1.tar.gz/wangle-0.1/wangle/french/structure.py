from wangle import structure

from . import conjugator
from . import decliner 
from . import adjective
from . import verb

class Sentence(structure.Sentence):
    conjugator = conjugator
    decliner = decliner

    def inflect(self):
        for token in self.tokens:
            if isinstance(token, structure.Word):
                word = token
                if word.has_tag("adjective"):
                    adjective.decline(self, word)
                if word.has_tag("verb"):
                    verb.conjugate(self, word)

    def contract(self):
        i = 0
        while i < len(self.tokens) - 1:
            token = self.tokens[i]
            next_token = self.tokens[i + 1]
            if isinstance(token, structure.Word) and isinstance(next_token, structure.Word) and str(token) in ["je", "me", "te", "se", "le", "la"] and str(next_token)[0] in "aâeéèêhiîïoôuy":
                token.inflection = token.inflection[0]
                self.tokens.insert(i + 1, "'")
            i += 1
