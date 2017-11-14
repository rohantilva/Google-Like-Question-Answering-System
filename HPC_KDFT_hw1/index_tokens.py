from concrete.util import lun, get_tokens
from concrete.util.access_wrapper import FetchCommunicationClientWrapper
from concrete import FetchRequest
from collections import OrderedDict
import math
import gzip
import os
import io
import stat


def read_communications():
    """
    Function to read in communications via the network on port 9090 (as
    per project specifications).
    Appends individual tokens to a dictionary with:
        token : {term_frequency: x, docy: z}
            where x is the total number of occurences of the term
            where docy represents a document the term appears in
            where z is the frequency within the document

    Note: this nested dictionary implementation may be the reason why
    my ./run.bash wikipedia.zip doesn't work. It could be that I'm
    using too much memory? I'm not sure at all.
    """
    comm_ids = []
    tokens = {}
    with FetchCommunicationClientWrapper("localhost", 9090) as connection:
        comm_count = connection.getCommunicationCount()
        start_count = 0
        while start_count != comm_count:
            conn_comIDs = connection.getCommunicationIDs(
                start_count, min(50, comm_count - start_count))
            fetchObj = FetchRequest(communicationIds=conn_comIDs)
            fr = connection.fetch(fetchObj)
            for comm in fr.communications:
                cid = comm.id
                comm_ids.append(cid)
                for section in lun(comm.sectionList):
                    for sentence in lun(section.sentenceList):
                        for token in get_tokens(sentence.tokenization):
                            token = str(token.text).lower()
                            if token not in tokens:
                                tokens[token] = {
                                    'tf': 1, (len(comm_ids) - 1): 1}
                            elif (len(comm_ids) - 1) not in tokens[token]:
                                tokens[token]['tf'] += 1
                                tokens[token][len(comm_ids) - 1] = 1
                            else:
                                tokens[token]['tf'] += 1
                                tokens[token][len(comm_ids) - 1] += 1
            start_count = start_count + 50
            start_count = min(start_count + 50, comm_count)
    sorted_tokens = OrderedDict(
        sorted(
            tokens.items(),
            key=lambda x: x[1]['tf'],
            reverse=True))
    return (comm_ids, sorted_tokens)


def write_to_file(cid, index):
    """
    Function that writes the index to the file.
    Parameters:
        list of communication ids
        dictionary of tokens from read_communcations
    Writes to the top-terms file as well as the index file as per project
    specifications.
    Returns:
        dictionary of tokens (in case we needed it later for any reason)
    """
    top = list(index.items())[:50]
    final_len = len(index) - 250
    while len(index) > final_len:
        index.popitem(last=False)
    top_terms = "/mnt/index/top-terms.txt"
    os.chmod("/mnt", stat.S_IWOTH)
    os.makedirs(os.path.dirname(top_terms), exist_ok=True)
    with io.open(top_terms, mode='w', encoding='utf-8') as f:
        for term in top:
            f.write(term[0] + '\n')
    index_file = "/mnt/index/index.gz"
    os.makedirs(os.path.dirname(index_file), exist_ok=True)
    with gzip.open(index_file, 'wt', encoding='utf-8') as f:
        for i in range(len(cid)):
            f.write(cid[i])
            if i < len(cid) - 1:
                f.write('\t')
        f.write('\n')
        position = 0
        for term in index:
            values = index[term]
            values.pop('tf')
            tidf = idf(len(cid), len(values.items()))
            f.write(term + '\t' + str(tidf))
            for k in sorted(values.keys()):
                f.write('\t' + str(k) + ':' + str(values[k]))
            if(position < len(index) - 1):
                f.write('\n')
            position += 1
    return index


def idf(N, df):
    return math.log(float(N) / float(df))


def main():
    t = read_communications()
    write_to_file(t[0], t[1])


if __name__ == "__main__":
    main()
