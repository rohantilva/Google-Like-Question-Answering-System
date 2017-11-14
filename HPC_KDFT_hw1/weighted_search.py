#!/usr/bin/env python

import time
import logging
import gzip

from concrete import AnnotationMetadata, ServiceInfo
from concrete.search import SearchService
from concrete.search.ttypes import SearchResult, SearchResultItem
from concrete.services.ttypes import ServicesException
from concrete.util import AnalyticUUIDGeneratorFactory, SearchServiceWrapper
from collections import OrderedDict


class SearchHandler(SearchService.Iface):
    def alive(self):
        return True

    def about(self):
        return ServiceInfo(name='stub search', version='0.0')

    def getCapabilities(self):
        raise ServicesException()

    def getCorpora(self):
        raise ServicesException()

    def tfidfByDoc(self, query_terms, index):
        """
        Helper function that calculates tfidf for each matching term in query.
        Parameters:
            query_terms list of terms in the query
            index file (opened for reading in search function)
        Returns:
            dictionary of query_matches in which
                keys = document number
                value = list of tfidf scores
        """
        query_matches = {}
        for line in index:
            line = line.split()
            idf = float(line[1])
            if line[0] in query_terms and len(query_terms) != 0:
                temp_docs = [d for d in line[2:]]
                for item in temp_docs:
                    item = item.split(':')
                    if item[0] not in query_matches.keys():
                        query_matches[item[0]] = [float(item[1]) * idf]
                    else:
                        query_matches[item[0]].append(float(item[1]) * idf)
                query_terms.remove(line[0])
        return query_matches

    def returnDocList(self, query_matches, doc_list, k_returned):
        """
        Helper function that returns documents according to overlap score.
        Parameters:
            dictionary of query_matches from tfidfByDoc
            doc_list of documents
            k_returned number of documents to return
        Returns:
            List of objects of type SearchResultItem (where communicationId field
            is the communcation id of the document to return), in descending order
            of overlap score.
        """
        return_docs = []
        if len(query_matches.keys()) == 0:
            return return_docs
        for k in query_matches:
            s = sum(i for i in query_matches[k])
            query_matches[k] = s
        sorted_docs = OrderedDict(
            sorted(
                query_matches.items(),
                key=lambda x: x[1],
                reverse=True))
        count = 0
        for k in sorted_docs:
            if count == k_returned:
                return return_docs
            sri = SearchResultItem(communicationId=doc_list[int(k)])
            return_docs.append(sri)
            count += 1
        return return_docs

    def search(self, query):
        augf = AnalyticUUIDGeneratorFactory()
        aug = augf.create()
        terms = query.terms
        num_docs = query.k
        query_matches = {}
        documents = []
        results = []
        with gzip.open("/mnt/index/index.gz", 'rt', encoding='utf-8') as index:
            first_line = index.readline()
            documents = first_line.split()
            query_matches = self.tfidfByDoc(terms, index)
        results = self.returnDocList(query_matches, documents, num_docs)
        # begin weighted search here
        return SearchResult(uuid=aug.next(),
                            searchQuery=query,
                            searchResultItems=results,
                            metadata=AnnotationMetadata(
                                tool="stub search",
                                timestamp=int(time.time())),
                            lang="eng")


if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", type=int, default=9090)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--input-path",
                        default="/mnt/index/index.gz")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)-15s %(levelname)s: %(message)s',
                        level='DEBUG')

    handler = SearchHandler()

    server = SearchServiceWrapper(handler)

    logging.info('Starting the server...')
    server.serve(args.host, args.port)
