#!/usr/bin/env python

import time, csv, gzip
import logging

from concrete import AnnotationMetadata, ServiceInfo
from concrete.search import SearchService
from concrete.search.ttypes import SearchResult, SearchCapability, SearchType, SearchQuery
from concrete.services.ttypes import ServicesException
from concrete.util import AnalyticUUIDGeneratorFactory, SearchServiceWrapper, SearchClientWrapper


class SearchHandler(SearchService.Iface):
    def __init__(self, other, corpus_name, host, port):
        self.other = other
        self.corpus_name = corpus_name
        self.port = port
        self.host = host
    def alive(self):
        return True

    def about(self):
        return ServiceInfo(name='search kscore', version='0.0')

    def getCapabilities(self):
        return [SearchCapability(SearchType.SENTENCES)]
        # raise ServicesException()

    def getCorpora(self):
        raise [self.corpus_name]

    def search(self, query):
        print(query)
        return self.other.search(query)
        # augf = AnalyticUUIDGeneratorFactory()
        # aug = augf.create()
        # with SearchClientWrapper(self.host, self.port) as sc:
            # return sc.search(query)

def kscore(s):
    truth = []
    with gzip.open("WikiQA-dev.tsv.gz", 'rt') as wiki:
        reader = csv.reader(wiki)
        next(reader)
        used = {}
        k_vals = [1, 10, 100, 1000]
        for row in reader:
            print(row)
            row = row[0].split("\t")
            query = row[1]
            if query not in used:
                used[query] = 0
                terms = query.split(" ")
                for k_val in k_vals:
                    query1 = SearchQuery(type=SearchType.SENTENCES, terms=terms, k=k_val, rawQuery=query)
                    results = s.search(query1)
                    for result in results.searchResultItems:
                        print(k_val)
            else:
                continue
    # kmatches = qmatches[:k]
    correct = 0
    #for m in kmatches:
        #if m in truth:
            #correct += 1
    return(correct)


if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--port", type=int, default=9090)
    parser.add_argument("--host", default="kdft")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)-15s %(levelname)s: %(message)s',
                        level='DEBUG')
    print(args.host)
    print(args.port)   
    time.sleep(10)
    with SearchClientWrapper(args.host, args.port) as search_client:
        handler = SearchHandler(search_client, "wikiQA", "", "")
        kscore(handler)
