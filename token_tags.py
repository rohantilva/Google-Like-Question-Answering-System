from concrete.util import lun, get_tokens
from concrete.util.access_wrapper import FetchCommunicationClientWrapper
from concrete import FetchRequest
from concrete.util import get_tagged_tokens
import gzip

def qid_sid(dataset):
    with open(dataset, "rb") as f:
        next(f)
        for line in f:
            line = line.decode('UTF-8')
            qid = arr[0]
            sid = arr[4]
    return


def match_dict(match):
    sent_match = {}
    with open(match, "rb") as f:
        next(f)
        for line in f:
            line = line.decode('UTF-8')
            arr = line.split("\t")
            print(arr)
            sid = arr[0]
            caw_info = arr[2]
            if sid not in sent_match.keys():
                sent_match[sid] = [caw_info]
            else:
                sent_match[sid].append(caw_info)
    return sent_match


def match_tags(match_dict):
    mt = {}
    with FetchCommunicationClientWrapper("ec2-35-153-184-225.compute-1.amazonaws.com", 9090) as fc:
        print("opened connection")
        comm_count = fc.getCommunicationCount()
        start_count = 0
        while start_count != comm_count:
            conn_comIDs = fc.getCommunicationIDs(
                start_count, min(50, comm_count - start_count)
            )
            print(conn_comIDs)
            fetchObj = FetchRequest(communicationIds=conn_comIDs)
            fr = fc.fetch(fetchObj)
            for comm in fr.communications:
                print(comm.id)
                section = 0
                for section in lun(comm.sectionList):
                    for sentence in lun(section.sentenceList):
                        for token_tag in get_tagged_tokens(sentence.tokenization, 'POS'):
                            print(token_tag)
            start_count += 50
            start_count = min(start_count, comm_count)

def main():
    matches = match_dict("./data/WikiQA-match/train-match.tsv")
    #print(matches)
    match_tags(matches)


if __name__ == '__main__':
    main()
