#!/usr/bin/env python

import time
import logging

from concrete import AnnotationMetadata, ServiceInfo
from concrete.search import SearchService
from concrete.search.ttypes import SearchResult, SearchCapability, SearchType
from concrete.services.ttypes import ServicesException
from concrete.util import AnalyticUUIDGeneratorFactory, SearchServiceWrapper, SearchClientWrapper


class SearchHandler(SearchService.Iface):
    def __init__(self, other, corpus_name):
        self.other = other
        self.corpus_name = corpus_name
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
        # return self.other.search(query)
        # augf = AnalyticUUIDGeneratorFactory()
        # aug = augf.create()
        with SearchClientWrapper("search", "9090") as sc:
            return sc.search(query)


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
    
    # time.sleep(3000)
    # with SearchClientWrapper("search", "9090") as search_client:
    # handler = SearchHandler(search_client, "wikiQA")
    handler = SearchHandler(None, "wikiQA")

    server = SearchServiceWrapper(handler)

    logging.info('Starting the server...')
    server.serve(args.host, args.port)
