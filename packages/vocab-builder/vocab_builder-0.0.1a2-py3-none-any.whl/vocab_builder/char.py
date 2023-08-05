from .vocab import Vocab


# Building Vocab with text files
class CharVocab(Vocab):
    def tokenizer(self, sentence: str):
        return list(sentence.strip())

    def joiner(self, tokens: list):
        return "".join(tokens)
