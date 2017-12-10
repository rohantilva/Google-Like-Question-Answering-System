# utility file and utility function for stemmer (morphy)

from nltk.corpus import wordnet as wn

# stemming function constructs a new string with stemmed words (if possible).
# Returns string with modified words.
def stem(query):
    s = ""
    query = query.split(" ")
    for word in query:
        stem = wn.morphy(word)
        s += ' ' + stem if stem is not None else ' ' + word
    return s
