from concrete.util import lun, get_tokens
from concrete.util.access_wrapper import FetchCommunicationClientWrapper
from concrete import FetchRequest
from nltk.corpus import wordnet
import nltk
from utils import SearchKDFT
import collections

# stemming function constructs a new string with stemmed words (if possible).
# Returns string with modified words.
'''def stem(query):
    s = ""
    query = query.split(" ")
    for word in query:
        stem = wordnet.morphy(word)
        s += ' ' + stem if stem is not None else ' ' + word
    return s'''

def return_search_results(sentence):
'''    # common linking verbs
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
    queries.append(sentence)'''
    queries = []
    queries.append(sentence)
    print('queries are' + str(queries))
    s = SearchKDFT()
    results = list()
    for query in queries:
        result = s.search(query)
        results.append(result)
        
    return results

def get_comm_ids(results):
    comm_ids_list = list()
    temp = collections.OrderedDict()
    for search_result in results:
        for search_result_item in search_result.searchResultItems:
            temp[search_result_item.sentenceId.uuidString] = search_result_item.communicationId
            comm_ids_list.append(str(search_result_item.communicationId))
    return comm_ids_list, temp

def fetch_dataset(comm_ids, dict_uuid_commID):
    with FetchCommunicationClientWrapper("172.18.0.2", 9090) as fc:
#        print(comm_ids)
        fetchObj = FetchRequest(communicationIds=comm_ids)
        print("check1")
        print(fetchObj)
        fr = fc.fetch(fetchObj)
        print("pleaseeeeee")
        for comm in fr.communications:
            for section in lun(comm.sectionList):
                for sentence in lun(section.sentenceList):
                    if sentence.uuid.uuidString in dict_uuid_commID.keys():
                        print(sentence.uuid.uuidString)
                        print(comm.text[sentence.textSpan.start:sentence.textSpan.ending])
                        dict_uuid_commID[sentence.uuid.uuidString] = comm.text[sentence.textSpan.start:sentence.textSpan.ending]

    print(dict_uuid_commID)
    inv_map = {v: k for k, v in dict_uuid_commID.items()}

results = return_search_results("Who is the point guard for the Cleveland Cavaliers?")
comm_ids, dict_uuid_commID = get_comm_ids(results)
fetch_dataset(comm_ids, dict_uuid_commID)
