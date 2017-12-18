# utility file and utility function for stemmer (morphy)
from concrete.util import lun, get_tokens
from concrete.util.access_wrapper import FetchCommunicationClientWrapper
from concrete import FetchRequest
from nltk.corpus import wordnet
import nltk
# from utils import SearchKDFT

# stemming function constructs a new string with stemmed words (if possible).
# Returns string with modified words.
def stem(query):
    s = ""
    query = query.split(" ")
    for word in query:
        stem = wordnet.morphy(word)
        s += ' ' + stem if stem is not None else ' ' + word
    return s

def return_search_results(sentence):
    # common linking verbs
    linking_verbs = ['am', 'be', 'are', 'wa', 'being']
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
            if word not in linking_verbs:
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
    queries.append(sentence)
    # print('queries are' + str(queries))
    # s = SearchKDFT()
    # results = list()
    # for query in queries:
        # result = s.search(query)
        # print(result)
        # print()
        # print()
#        results.append(result)

    return queries  
    # return results

def get_comm_ids(results):
    comm_ids_list = list()
    #for result in results:
        

def fetch_large_dataset():
    with FetchCommunicationClientWrapper("ec2-35-153-184-225.compute-1.amazonaws.com", 9090) as fc:
        comm_count = fc.getCommunicationCount()
        start_count = 0
        conn_comIDs = fc.getCommunicationIDs(start_count, 1)
        fetchObj = FetchRequest(communicationIds=conn_comIDs)
        fr = fc.fetch(fetchObj)
        for comm in fr.communications:
            for section in lun(comm.sectionList):
                for sentence in lun(section.sentenceList):
                    print(sentence.uuid.uuidString)
                    print(comm.text[sentence.textSpan.start:sentence.textSpan.ending])
                    # if sentence.uuid.uuidString == sentence_uuid_string:

#            for section in lun(comm.sectionList):
#                for sentence in lun(section.sentenceList):
#                    print(sentence)
#                    print()
        #while start_count != comm_count:
        #    conn_comIDs = fc.getCommunicationIDs(
        #        start_count, min(50, comm_count - start_count)
        #    )
        #    fetchObj = FetchRequest(communicationIds=conn_comIDs)
        #    fr = fc.fetch(fetchObj)
        #    for comm in fr.communications:
        #        print(comm.id)
        #        for section in lun(comm.sectionList):
        #            for sentence in lun(section.sentenceList):
        #                for token in get_tokens(sentence.tokenization):
        #                    print(token)
        #    start_count += 50
        #    start_count = min(start)


results = return_search_results("Who is the point guard for the Cleveland Cavaliers?")
get_comm_ids(results)
fetch_large_dataset()
