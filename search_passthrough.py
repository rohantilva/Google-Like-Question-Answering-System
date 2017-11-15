#!/usr/bin/env python

import time
import logging

from concrete import AnnotationMetadata, ServiceInfo
from concrete.search import SearchService
from concrete.search.ttypes import SearchResult
from concrete.services.ttypes import ServicesException
from concrete.util import AnalyticUUIDGeneratorFactory, SearchServiceWrapper


class SearchHandler(SearchService.Iface):
    def alive(self):
        return True

    def about(self):
        return ServiceInfo(name='search pass', version='0.0')

    def getCapabilities(self):
        raise ServicesException()

    def getCorpora(self):
        raise ServicesException()

    def search(self, query):
        augf = AnalyticUUIDGeneratorFactory()
        aug = augf.create()
        return SearchResult(uuid=aug.next(),
                            searchQuery=query,
                            searchResultItems=[],
                            metadata=AnnotationMetadata(
                                tool="stub search",
                                timestamp=int(time.time())),
                            lang="eng")


if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", type=int, default=9090)
    parser.add_argument("--host", default="localhost")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)-15s %(levelname)s: %(message)s',
                        level='DEBUG')

    handler = SearchHandler()

    server = SearchServiceWrapper(handler)

    logging.info('Starting the server...')
    server.serve(args.host, args.port)
