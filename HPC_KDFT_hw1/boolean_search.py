#!/usr/bin/env python

import time
import logging
import gzip

from concrete import AnnotationMetadata, ServiceInfo
from concrete.search import SearchService
from concrete.search.ttypes import SearchResult, SearchResultItem
from concrete.services.ttypes import ServicesException
from concrete.util import AnalyticUUIDGeneratorFactory, SearchServiceWrapper


class SearchHandler(SearchService.Iface):
    def alive(self):
        return True

    def about(self):
        return ServiceInfo(name='stub search', version='0.0')

    def getCapabilities(self):
        raise ServicesException()

    def getCorpora(self):
        raise ServicesException()

    def docsByTerm(self, query_terms, index):
        """
        A helper function that finds query matches from an index.
        Parameters:
            list of query terms
            index file (opened for reading in the search function)
        Returns:
            dictionary of query matches where
                keys = query terms
                value = list of documents term appears in
        """
        query_matches = {}
        for line in index:
            line = line.split()
            if line[0] in query_terms and len(query_terms) != 0:
                temp_docs = [d for d in line[2:]]
                doc_matches = []
                for item in temp_docs:
                    item = item.split(':')
                    doc_matches.append(item[0])
                query_matches[line[0]] = doc_matches
                query_terms.remove(line[0])
        return query_matches

    def returnDocList(self, query_matches, doc_list, k_returned):
        """
        A helper function that returns documents that all query terms appear in.
        Parameters:
            dictionary of query_matches
            doc_list of document names (in order of storage in the index)
            k_returned integer number of documents to return from the search
        Returns:
            A list of objects of type SearchResultItem, where the communcationId
            field is the string communcation id
        """
        r = []
        results = []
        if len(query_matches.keys()) == 0:
            return(results)
        dl = [d for d in query_matches.values()]
        intersection = set(dl[0]).intersection(*dl)
        r = list(intersection)
        r = r[:k_returned]
        for i in r:
            sri = SearchResultItem(communicationId=doc_list[int(i)])
            results.append(sri)
        return results

    def search(self, query):
        augf = AnalyticUUIDGeneratorFactory()
        aug = augf.create()
        k_returned = query.k
        terms = query.terms
        # implement boolean search here
        query_matches = {}
        documents = []
        with gzip.open("/mnt/index/index.gz", 'rt', encoding='utf-8') as index:
            first_line = index.readline()
            documents = first_line.split()
            query_matches = self.docsByTerm(terms, index)
        results = self.returnDocList(query_matches, documents, k_returned)
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
