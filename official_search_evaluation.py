#!/usr/bin/env python3

from gzip import GzipFile
from collections import defaultdict
import logging

from concrete.search.ttypes import SearchQuery, SearchType
from concrete.util import SearchClientWrapper


def mean(x):
    '''
    Return mean of x, an iterable of numbers (or things that are
    automatically cast to numbers).
    '''
    x = list(x)
    return sum(x) / float(len(x))


def escape_query(query):
    '''
    Given query text, return escaped version of text (with special
    characters escaped so Lucene doesn't freak out).

    Special characters determined from:
    https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
    Plus (determined empirically): /
    '''
    for c in list('\\/+-!(){}[]^"~*?:') + ['&&', '||']:
        query = query.replace(c, '\\' + c)
    return query


def search_questions(host, port, question_texts, k):
    '''
    Given a hostname (or IP) and port of a search service to connect to,
    a dictionary `question_texts` mapping question IDs to question texts
    (strings), and the maximum number of hits to retrieve, k, send each
    question text to the search service and retrieve the results as a
    SearchResult object.  Before passing a question text to the search
    client (in a query), escape it using `escape_query`.  Return a
    dictionary mapping question IDs to the respective SearchResult
    objects.

    Note: k is passed in the SearchQuery; it is also used to truncate
    SearchResult.searchResultItems afterward (noting that some services
    do not respect the k parameter).  So the length of searchResultItems
    in the returned SearchResult objects will always be at most k.
    '''
    results = dict()
    with SearchClientWrapper(host, port) as search_client:
        for (question_id, question_text) in question_texts.items():
            result = search_client.search(SearchQuery(
                type=SearchType.SENTENCES,
                rawQuery=escape_query(question_text),
                k=k))
            result.searchResultItems = result.searchResultItems[:k]
            results[question_id] = result
    return results


def search_result_contains_answer(answer_uuids, search_result):
    '''
    Given a set of gold-standard answer UUIDs, and a SearchResult
    representing the output of the system, return True if the sentence
    UUIDs of any of the result items are in the gold standard (and
    False otherwise).
    '''
    return not answer_uuids.isdisjoint(set(
        item.sentenceId.uuidString
        for item in search_result.searchResultItems))


def compute_success(question_search_results, question_answer_uuids):
    '''
    Given a dictionary mapping question IDs to search results (the
    outputs of a search system on those questions), and a dictionary
    mapping question IDs to sets of gold-standard answer sentence
    UUIDs, compute and return the success@k search performance metric.
    '''
    if set(question_search_results.keys()) != set(
            question_answer_uuids.keys()):
        raise Exception(
            'search results and gold-standard answers are not defined over '
            'the same set of questions')
    successes = [
        search_result_contains_answer(
            answer_uuids,
            question_search_results[question_id])
        for (question_id, answer_uuids)
        in question_answer_uuids.items()]
    return mean(successes)


def main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(
        description='Compute success@k of Search service over WikiQA.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('k', help='Number of hits to consider', type=int)
    parser.add_argument('--search-host',
                        help='IP/hostname on which search service is '
                             'listening',
                        default='localhost')
    parser.add_argument('--search-port',
                        help='Port on which search service is listening',
                        type=int, default=9091)
    parser.add_argument('--data-path',
                        help='path to WikiQA tsv.gz file of questions and '
                             'answers',
                        default='data/WikiQA/WikiQA-dev.tsv.gz')
    parser.add_argument('--match-data-path',
                        help='path to WikiQA tsv file matching WikiQA '
                             'question/answer IDs to Concrete',
                        default='data/WikiQA-match/dev-match.tsv')
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)-15s %(levelname)s: %(message)s',
                        level=logging.INFO)

    logging.info('parsing WikiQA question-answer pairs')

    # We only collect the positive answers to the questions; we do not
    # need the negative answers to compute success@k.

    # mapping: answer (sentence) ID -> set of question IDs
    answer_question_ids = defaultdict(set)
    # mapping: question ID -> question text
    question_texts = dict()

    all_question_ids = set()
    num_ans = 0
    num_pos_ans = 0
    fieldnames = None
    with GzipFile(args.data_path) as f:
        fieldnames = None
        for line_bytes in f:
            line = line_bytes.decode('utf-8')
            pieces = line.rstrip().split('\t')
            if fieldnames is None:
                fieldnames = pieces
            else:
                row = dict(zip(fieldnames, pieces))
                all_question_ids.add(row['QuestionID'])
                num_ans += 1
                if bool(int(row['Label'])):
                    answer_question_ids[row['SentenceID']].add(
                        row['QuestionID'])
                    question_texts[row['QuestionID']] = row['Question']
                    num_pos_ans += 1

    logging.info('parsed {} answers in total ({} positive answers)'.format(
        num_ans, num_pos_ans))
    logging.info('parsed {} questions in total ({} w/ pos. answers)'.format(
        len(all_question_ids), len(question_texts)))
    logging.info('average no. questions per positive answer: {:.2f}'.format(
        mean(len(qids) for qids in answer_question_ids.values())))

    logging.info('parsing WikiQA-Concrete match data')
    # mapping: question ID -> set of answer (sentence) UUIDs
    question_answer_uuids = defaultdict(set)

    num_ans = 0
    # No explicit fieldnames in this file, so specify it ourselves
    # (according to data/README.md).
    fieldnames = (
        'SentenceID', 'CommID', 'CommSentenceLoc', 'SentenceUUID', 'Label')
    with open(args.match_data_path, encoding='utf-8') as f:
        for line in f:
            pieces = line.rstrip().split('\t')
            row = dict(zip(fieldnames, pieces))
            num_ans += 1
            # Ignore Label this time; we already know which sentences
            # answer which questions, and just need to match WikiQA
            # sentence IDs to Concrete Sentence UUIDs.
            if row['SentenceID'] in answer_question_ids:
                for question_id in answer_question_ids[row['SentenceID']]:
                    question_answer_uuids[question_id].add(
                        row['SentenceUUID'])

    logging.info('parsed {} answers in total'.format(num_ans))
    logging.info('have {} questions with positive answers in Concrete'.format(
        len(question_answer_uuids)))
    logging.info('average no. positive answers per question: {:.2f}'.format(
        mean(len(auuids) for auuids in question_answer_uuids.values())))

    logging.info('performing search queries, truncating to {} hits'.format(
        args.k))

    question_texts_with_answers = dict(
        (question_id, question_text)
        for (question_id, question_text) in question_texts.items()
        if question_id in question_answer_uuids)
    question_search_results = search_questions(
        args.search_host,
        args.search_port,
        question_texts_with_answers,
        args.k)

    logging.info('average no. hits per query: {:.2f}'.format(mean(
        len(sr.searchResultItems) for sr in question_search_results.values())))

    logging.info('computing success(@{}) over search results'.format(
        args.k))

    success_at_k = compute_success(
        question_search_results, question_answer_uuids)
    print('{:.2f}'.format(success_at_k))


if __name__ == '__main__':
    main()

