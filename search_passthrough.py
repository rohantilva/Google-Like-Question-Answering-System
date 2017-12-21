#!/usr/bin/env python

import time
import logging

from concrete import AnnotationMetadata, ServiceInfo, FetchRequest
from concrete.search import SearchService
from concrete.search.ttypes import SearchResult, SearchCapability, SearchType, SearchQuery
from concrete.services.ttypes import ServicesException
from concrete.util import AnalyticUUIDGeneratorFactory, SearchServiceWrapper, SearchClientWrapper, lun, get_tokens
from query_int import return_search_results
from concrete.util.access_wrapper import FetchCommunicationClientWrapper
import collections
import pickle
from sklearn.neural_network import MLPClassifier
from preprocess import Preprocess
from test_model import pre_ranking
from rerank import rerank

class SearchHandler(SearchService.Iface):
    def __init__(self, other, corpus_name, host, port, preprocess):
        self.other = other
        self.corpus_name = corpus_name
        self.port = port
        self.host = host

    def alive(self):
        return True

    def about(self):
        return ServiceInfo(name='search pass', version='0.0')

    def getCapabilities(self):
        return [SearchCapability(SearchType.SENTENCES)]
        # raise ServicesException()

    def getCorpora(self):
        raise [self.corpus_name]

    def search(self, query):
        augf = AnalyticUUIDGeneratorFactory()
        aug = augf.create()
        results = []
        for query1 in return_search_results(query.rawQuery):
            query1 = SearchQuery(type=SearchType.SENTENCES, terms = query1.split(" "), rawQuery = query1, k=500)
            result = self.other.search(query1)
            # logging.info(result.searchResultItems)
            results.extend(result.searchResultItems)
        # results = SearchResult(searchResultItems=results, searchQuery=query)
        # logging.info(len(results))
        resultsDict = {}
        for result in results:
            resultsDict[result.sentenceId.uuidString] = result
        results = []
        for key in resultsDict:
            results.append(resultsDict[key])
        # results = results[:10] # comment out on full run
        comm_ids_list, temp = get_comm_ids(results)
        dictUUID = fetch_dataset(comm_ids_list, temp)
        inv_map = {v: k for k, v in dictUUID.items()}
        toHannah = []
        for uuid in dictUUID:
            toHannah.append([query.rawQuery, dictUUID[uuid]])
        resultItemRet = SearchResult(uuid=aug.next(),
                                     searchQuery=query,
                                     searchResultItems=results,
                                     metadata=AnnotationMetadata(
                                        tool="search",
                                        timestamp=int(time.time())),
                                     lang="eng")
        model = pickle.load(open("./trained_model.p", "rb"))
        pre = Preprocess()
        feature_matrix = pre.process_run(toHannah)
        dictRanks = pre_ranking(feature_matrix, model, toHannah, inv_map)
        results = rerank(dictRanks, resultItemRet)
        resultArr = results.searchResultItems
        resultArr = sorted(resultArr, key=lambda result: result.score, reverse=True)
        for item in resultArr:
            logging.info(item.score)
        resultItemRet = SearchResult(uuid=aug.next(),
                                     searchQuery=query,
                                     searchResultItems=resultArr,
                                     metadata=AnnotationMetadata(
                                        tool="search",
                                        timestamp=int(time.time())),
                                     lang="eng")
        return resultItemRet
        # augf = AnalyticUUIDGeneratorFactory()
        # aug = augf.create()
        # with SearchClientWrapper(self.host, self.port) as sc:
            # return sc.search(query)

def get_comm_ids(results):
    comm_ids_list = list()
    temp = collections.OrderedDict()
    for search_result_item in results:
        temp[search_result_item.sentenceId.uuidString] = search_result_item.communicationId
        comm_ids_list.append(str(search_result_item.communicationId))
    return comm_ids_list, temp

def fetch_dataset(comm_ids, dict_uuid_commID):
    with FetchCommunicationClientWrapper("ec2-52-90-242-175.compute-1.amazonaws.com", 9093) as fc:
        num_comms = len(comm_ids)
        total = 0
        while (total < num_comms):
            if (num_comms - total >= 40):
                fetchObj = FetchRequest(communicationIds=comm_ids[total:total+40])
                total += 40
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
    return dict_uuid_commID

if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--port", type=int, default=9090)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--search_port", type=int, default=9090)
    parser.add_argument("--search_host", default="localhost")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)-15s %(levelname)s: %(message)s',
                        level='DEBUG')
    # time.sleep(10000)
    logging.info('Starting the server...')
    while True:
        try:
            logging.info('hi')
            time.sleep(1)
            with SearchClientWrapper("ec2-52-90-242-175.compute-1.amazonaws.com", "9091") as search_client:
                # Create preprocess and train it here, need to pass to handler
                handler = SearchHandler(search_client, "wikiQA", "", "", None)
                # handler = SearchHandler(None, "wikiQA", args.search_host, args.search_port)
                server = SearchServiceWrapper(handler)

                logging.info('Starting the server...')
                server.serve(args.host, args.port)
                break
        except:
            pass
