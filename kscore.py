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
        return self.other.search(query)
        # augf = AnalyticUUIDGeneratorFactory()
        # aug = augf.create()
        # with SearchClientWrapper(self.host, self.port) as sc:
            # return sc.search(query)

def kscore(s):
    truth = []
    answer_labels = {}
    with open("dev-match.tsv") as match:
        reader = csv.reader(match, delimiter="\t", quotechar="'")
        for row in reader:
            answer_labels[row[3]] = row[4]
        
    with gzip.open("WikiQA-dev.tsv.gz", 'rt') as wiki:
        reader = csv.reader(wiki, delimiter="\t", quotechar="'")
        next(reader)
        used = {}
        k_val_dict = {
            1:[0,0],
            10:[0,0],
            100:[0,0],
            1000:[0,0]
        }
        k_vals = [1, 10, 100, 1000]
        for row in reader:
            print(row)
            query = row[1]
            sentenceID = row[4]
            # query = query.replace(","," ")
            # query = query.replace("'"," ")
            query = query.replace('"',"")
            query = query.replace("/"," ")
            query = query.replace("?","")
            if query not in used:
                used[query] = 0
                terms = query.split(" ")
                for k_val in k_vals:
                    query1 = SearchQuery(type=SearchType.SENTENCES, terms=terms, k=k_val, rawQuery=query)
                    results = s.search(query1)
                    atK = 0
                    totCorrect = 0
                    hasAnswerInMatch = False
                    for result in results.searchResultItems:
                        if atK == k_val:
                            break
                        else:
                            atK += 1
                            try:
                                totCorrect += int(answer_labels[result.sentenceId.uuidString])
                                hasAnswerInMatch = True
                            except (KeyError):
                                atK -= 1
                         
                    if totCorrect >= 1:
                        k_val_dict[k_val][0] += 1
                    if hasAnswerInMatch:
                        k_val_dict[k_val][1] += 1

            else:
                continue
    print("Baseline success @k")
    print("1: {}".format(k_val_dict[1][0]/k_val_dict[1][1]))
    print("10: {}".format(k_val_dict[10][0]/k_val_dict[10][1]))
    print("100: {}".format(k_val_dict[100][0]/k_val_dict[100][1]))
    print("1000: {}".format(k_val_dict[1000][0]/k_val_dict[1000][1]))


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
