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

class SearchKDFT:
    def search(self, string):
        string = string.replace('"',"")
        string = string.replace("/"," ")
        string = string.replace("?","")
        terms = string.split(" ")
        with SearchClientWrapper("172.19.0.4", 9090) as search_client:
            handler = SearchHandler(search_client, "wikiQA", "", "")
            query1 = SearchQuery(type=SearchType.SENTENCES, terms=terms, k=500, rawQuery=string)
            return handler.search(query1)
