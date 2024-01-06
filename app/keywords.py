import operator
from keybert import KeyBERT

keybert_model = KeyBERT()


def extract_keywords_(text):
    return list(map(operator.itemgetter(0), list(keybert_model.extract_keywords(text))))
