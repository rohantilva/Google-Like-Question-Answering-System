#!/usr/bin/env python

import time
import logging

from concrete import AnnotationMetadata, ServiceInfo
from concrete.search import SearchService
from concrete.search.ttypes import SearchResult, SearchCapability, SearchType, SearchQuery
from concrete.services.ttypes import ServicesException
from concrete.util import AnalyticUUIDGeneratorFactory, SearchServiceWrapper, SearchClientWrapper
from query_int import return_search_results

class SearchHandler(SearchService.Iface):
    def __init__(self, other, corpus_name, host, port):
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
        return SearchResult(uuid=aug.next(),
                            searchQuery=query,
                            searchResultItems=results,
                            metadata=AnnotationMetadata(
                                tool="search",
                                timestamp=int(time.time())),
                            lang="eng")
        # augf = AnalyticUUIDGeneratorFactory()
        # aug = augf.create()
        # with SearchClientWrapper(self.host, self.port) as sc:
            # return sc.search(query)


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
    while True:
        try:
            with SearchClientWrapper("search", "9090") as search_client:
                handler = SearchHandler(search_client, "wikiQA", "", "")
                # handler = SearchHandler(None, "wikiQA", args.search_host, args.search_port)
                server = SearchServiceWrapper(handler)

                logging.info('Starting the server...')
                server.serve(args.host, args.port)
                break
        except:
            pass
