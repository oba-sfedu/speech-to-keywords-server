import yake
import operator
from keybert import KeyBERT
from settings import language

yake_max_ngram_size = 3
yake_deduplication_threshold = 0.9
yake_num_of_keywords = 5
yake_extractor = yake.KeywordExtractor(lan=language, n=yake_max_ngram_size, dedupLim=yake_deduplication_threshold,
                                       top=yake_num_of_keywords, features=None)

keybert_model = KeyBERT()


def extract_keywords_yake(text):
    return list(map(operator.itemgetter(0), yake_extractor.extract_keywords(text)))


def extract_keywords_keybert(text):
    return list(map(operator.itemgetter(0), list(keybert_model.extract_keywords(text))))
