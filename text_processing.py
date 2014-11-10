"""
Set of functions that process texts.
They are meant as parameters of GraphBuilder objects
"""
import string

import nltk


def clean_stopwords(tokens):
    """
    Removes stopwords from a list of words
    """
    stopwords = nltk.corpus.stopwords.words('english')
    not_stop_words = []
    for token in tokens:

        if not token in stopwords:
            not_stop_words.append(token)

    return not_stop_words

def remove_punctuation(tokens):
    """
    Removes punctuation from a list of tokens
    It uses string.punctuation list of punctuation
    """
    REMOVE_PUNCTUATION_MAPPING = dict.fromkeys(map(ord, string.punctuation))

    not_punct_words = []
    for token in tokens:

        # Careful: not enough for unicode punctuation, ie. spanish or other languages
        # punctuation symbols. Not important in this context though.
        not_punct_token = token.translate(REMOVE_PUNCTUATION_MAPPING)
        if not not_punct_token == '':
            not_punct_words.append(not_punct_token)

    return not_punct_words

def clean_punctuation_and_stopwords(tokens):
    tokens = remove_punctuation(tokens)
    tokens = clean_stopwords(tokens)
    return tokens