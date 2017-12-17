# utility file and utility function for stemmer (morphy)

from nltk.corpus import wordnet as wn
import nltk

# stemming function constructs a new string with stemmed words (if possible).
# Returns string with modified words.
def stem(query):
    s = ""
    query = query.split(" ")
    for word in query:
        stem = wn.morphy(word)
        s += ' ' + stem if stem is not None else ' ' + word
    return s

def return_search_results(sentence):
    sentence = stem(sentence)
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    
    queries_verb = []
    queries_adj = []
    queries_adv = []
    
    queries_verb.append(sentence)
    queries_adj.append(sentence)
    queries_adv.append(sentence)
    
    print(tagged)
    
    for tups in tagged:
        if tups[1].startswith('V'):
            word = tups[0]
            syns = wordnet.synsets(word, pos=wordnet.VERB)
            for syn in syns:
                for l in syn.lemmas():
                    if l.name() != word:
                        new_sentence = sentence.replace(word, l.name())
                            #if new_sentence not in queries:
                        queries_verb.append(new_sentence)
                if len(queries_verb) >= 11:
                    break
    
    for tups in tagged:
        if tups[1] == 'JJ':
            word = tups[0]
            syns = wordnet.synsets(word, pos=wordnet.ADJ)
            for syn in syns:
                for l in syn.lemmas():
                    if l.name() != word:
                        new_sentence = sentence.replace(word, l.name())
                            #if new_sentence not in queries:
                        queries_adj.append(new_sentence)
                if len(queries_adj) >= 11:
                    break
    
    for tups in tagged:
        if tups[1] == 'RB':
            word = tups[0]
            syns = wordnet.synsets(word, pos=wordnet.ADV)
            for syn in syns:
                for l in syn.lemmas():
                    if l.name() != word:
                        new_sentence = sentence.replace(word, l.name())
                            #if new_sentence not in queries:
                        queries_adv.append(new_sentence)
                if len(queries_adv) >= 11:
                    break
    
    queries = list(set(queries_verb) | set(queries_adj) | set(queries_adv))
    print(queries)
    s = SearchKDFT()
    results = list()
    for query in queries:
        result = s.search(query)
        results.append(result)

    return results
