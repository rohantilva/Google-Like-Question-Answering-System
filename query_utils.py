from concrete.util import lun, get_tokens
from concrete.util.access_wrapper import FetchCommunicationClientWrapper
from concrete import FetchRequest
from utils import SearchKDFT
import collections

def return_search_results(sentence):
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
        num_comms = len(comm_ids)
        total = 0
        while (total < num_comms):
            if (num_comms - total >= 10):
                fetchObj = FetchRequest(communicationIds=comm_ids[total:total+10])
                total += 10
            else:
                fetchObj = FetchRequest(communicationIds=comm_ids[total:num_comms-total])
                total += num_comms - total
#        print("check1")
            print(fetchObj)
            fr = fc.fetch(fetchObj)
            for comm in fr.communications:
                for section in lun(comm.sectionList):
                    for sentence in lun(section.sentenceList):
                        if sentence.uuid.uuidString in dict_uuid_commID.keys():
                            dict_uuid_commID[sentence.uuid.uuidString] = comm.text[sentence.textSpan.start:sentence.textSpan.ending]

    print(dict_uuid_commID)
    inv_map = {v: k for k, v in dict_uuid_commID.items()}

results = return_search_results("Who is the point guard for the Cleveland Cavaliers?")
comm_ids, dict_uuid_commID = get_comm_ids(results)
fetch_dataset(comm_ids, dict_uuid_commID)
