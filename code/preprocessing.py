'''

Preprocessing methods used by build_index.py
Sources: 
    https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
    https://www.nltk.org/api/nltk.tag.pos_tag.html
    https://www.cs.upc.edu/~nlp/SVMTool/PennTreebank.html
    https://stackoverflow.com/questions/33157847/lemmatizing-words-after-pos-tagging-produces-unexpected-results

'''

import nltk

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from nltk.tag import pos_tag
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

import string

def get_wordnet_pos(treebank_tag):
    '''
    Return a wordnet compliant Part Of Speech (POS) tag using treebank tags. Valid options are: 
        "n" for nouns,
        "v" for verbs, 
        "a" for adjectives,
        "r" for adverbs,
        "s" for satellite adjectives (not available with treebank tags, so mapped to nouns instead)
    Sources: 
        https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
        https://www.cs.upc.edu/~nlp/SVMTool/PennTreebank.html
    '''
    if treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        # Default type in is Noun
        return wordnet.NOUN

def tokenize(text):
    '''
    Tokenizes text in a document or query. 
    Removes punctuation and returns a list of tokens.
    '''
    assert type(text) == str

    # remove punctuation
    new_text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(new_text)

    return tokens

def normalize(tokens, method):
    '''
    Normalize a list of tokens by lowercasing and applying 
    stemming or lemmatization.
    Sources:
        https://www.nltk.org/api/nltk.tag.pos_tag.html
        https://stackoverflow.com/questions/33157847/lemmatizing-words-after-pos-tagging-produces-unexpected-results
    '''
    assert type(tokens) == list

    l_cased = [token.lower() for token in tokens]

    if method == 'stemming':
        normalized = [stemmer.stem(token) for token in l_cased]
    else:
        # Find pos tags of words in a sentence, ie (token, tag)
        pos_tagged_tokens = pos_tag(l_cased)
        
        # Lemmatize tokens using their pos_tags converted into a usable format
        normalized = [lemmatizer.lemmatize(token, pos=get_wordnet_pos(pos_tag)) for token, pos_tag in pos_tagged_tokens]

    return normalized
