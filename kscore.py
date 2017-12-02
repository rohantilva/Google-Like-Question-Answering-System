#!/usr/bin/env python3

import logging
import csv, gzip, time
from concrete.search.ttypes import SearchQuery, SearchType
from concrete.util import SearchClientWrapper


def calc_kscore(search_client):
    truth = []
    time.sleep(10)
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
                    results = execute_search_query(search_client, terms, k_val)
                    for result in results:
                        print(result)
            else:
                continue
    # kmatches = qmatches[:k]
    correct = 0
    #for m in kmatches:
        #if m in truth:
            #correct += 1
    return(correct)

def execute_search_query(search_client, terms, k):
    logging.debug("executing query '{}'".format(' '.join(terms)))
    query = SearchQuery(type=SearchType.COMMUNICATIONS, terms=terms, k=k)
    result = search_client.search(query)
    return [
        (item.communicationId, item.score)
        for item in result.searchResultItems
    ]


def main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    import sys

    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description='Concrete Search client (allows specifying query on '
                    'command line, interactively on the terminal, or '
                    'in batch from standard input).'
    )
    parser.add_argument("--host", default="localhost",
                        help='Hostname of Search service')
    parser.add_argument("--port", type=int, default=8081,
                        help='Port of Search service')
    parser.add_argument("--search_port", type=int, default=9090,
                        help='Port of Search service')
    parser.add_argument("--search_host", default="kdft",
                        help='Port of Search service')
    parser.add_argument("--fetch_port", type=int, default=9090,
                        help='Port of Search service')
    parser.add_argument("--fetch_host", default="fetch",
                        help='Port of Search service')
    args = parser.parse_args()





    logging.info('starting single-query non-interactive search client...')
    with SearchClientWrapper(args.search_host, args.search_port) as search_client:
        calc_kscore(search_client)


if __name__ == "__main__":
    main()
