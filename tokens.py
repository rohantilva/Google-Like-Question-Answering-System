#tokenize terms
#find syns for verbs and for nouns
import nltk
from nltk.corpus import wordnet
from query_utils import stem
from utils import SearchKDFT

#sentence = "Do large dogs quickly move?"
#sentence = "What is the fastest land animal?"
#sentence = "who runs the world"
#sentence = "who is the point guard for the phoenix suns"
#sentence = "how are epithelial cells joined together?"
sentence = input("Enter a query: ")
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


#counter = 0
#print("verb modifications: ")
#for sentence in queries_verb:
#    print("sentence " + str(counter) + ": " + sentence)
#    counter += 1
#
#counter = 0
#print("adjective modifications: ")
#for sentence in queries_adj:
#    print("sentence " + str(counter) + ": " + sentence)
#    counter += 1
#
#counter = 0
#print("adverb modifications: ")
#for sentence in queries_adv:
#    print("sentence " + str(counter) + ": " + sentence)
#    counter += 1

queries = list(set(queries_verb) | set(queries_adj) | set(queries_adv))
print(queries)
s = SearchKDFT()
results = list()
for query in queries:
    result = s.search(query)
    results.append(result)

print(results)
