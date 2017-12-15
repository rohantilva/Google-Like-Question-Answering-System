from concrete.util import lun, get_tokens
from concrete.util.access_wrapper import FetchCommunicationClientWrapper
from concrete import FetchRequest
from concrete.util import get_tagged_tokens
import gzip
from collections import OrderedDict

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
            sid = arr[0]
            caw_info = arr[2]
            if caw_info not in sent_match.keys():
                sent_match[caw_info] = [sid]
            else:
                sent_match[caw_info].append(sid)
                #print(sent_match[caw_info])
    s_match = OrderedDict(sorted(sent_match.items(), key=lambda i: i[0]))
    return s_match


def match_tags(match_dict):
    mt = {}
    (caw_info, sid) = zip(*match_dict.items())
    caw_info = list(caw_info)
    sid = list(sid)
    with FetchCommunicationClientWrapper("ec2-35-153-184-225.compute-1.amazonaws.com", 9090) as fc:
        print("opened connection")
        comm_count = len(caw_info)
        start_count = 0
        curr_caws = caw_info[start_count:1]
        end_count = min(5 + end_count, comm_count - start_count)
        print(curr_caws)
        comm_ids = [i.split(':')[0] for i in curr_caws]
        print(comm_ids)
        fetchObj = FetchRequest(communicationIds=comm_ids)
        print(fetchObj)
        fr = fc.fetch(fetchObj)
        print(fr)
        comm_num = 0
        for comm in fr.communications:
            print("butts")
            info = curr_caws[comm_num].split(':')
            section_num = info[1]
            sent_num = info[2]
            section = lun(comm.sectionList)[section_num]
            sentence = lun(section.sentenceList)[sent_num]
            print(sentence)
            for token_tag in get_tagged_tokens(sentence.tokenization, 'POS'):
                print(token_tag)
            comm_num += 1
        start_count += 5
        start_count = min(start_count, comm_count)


def match_tags2(match_dict):
    with FetchCommunicationClientWrapper("ec2-35-153-184-225.compute-1.amazonaws.com", 9090) as fc:
        print("opened connection")
        comm_count = fc.getCommunicationCount()
        start_count = 0
        while start_count != comm_count:
            conn_comIDs = fc.getCommunicationIDs(
                start_count, min(1, comm_count - start_count)
            )
            print(conn_comIDs)
            fetchObj = FetchRequest(communicationIds=conn_comIDs)
            fr = fc.fetch(fetchObj)
        end_count = min(5, comm_count - start_count)
        while end_count < comm_count:
            curr_caws = caw_info[start_count:1]
            end_count = min(5 + end_count, comm_count - start_count)
            print(curr_caws)
            comm_ids = [i.split(':')[0] for i in curr_caws]
            print(comm_ids)
            fetchObj = FetchRequest(communicationIds=comm_ids)
            print(fetchObj)
            fr = fc.fetch(fetchObj)
            print(fr)
            print(fr.communications)
            comm_num = 0
            for comm in fr.communications:
                print(comm.id)
                for section in lun(comm.sectionList):
                    for sentence in lun(section.sentenceList):
                        for token_tag in get_tagged_tokens(sentence.tokenization, 'POS'):
                            print(token_tag)
            start_count += 50
            start_count = min(start_count, comm_count)
            break


<<<<<<< HEAD
=======
def match_tags2(match_dict):
    with FetchCommunicationClientWrapper("ec2-35-153-184-225.compute-1.amazonaws.com", 9090) as fc:
        print("opened connection")
        comm_count = fc.getCommunicationCount()
        start_count = 0
        while start_count != comm_count:
            conn_comIDs = fc.getCommunicationIDs(
                start_count, min(1, comm_count - start_count)
            )
            print(conn_comIDs)
            fetchObj = FetchRequest(communicationIds=conn_comIDs)
            fr = fc.fetch(fetchObj)
            for comm in fr.communications:
                print(comm.id)
                for section in lun(comm.sectionList):
                    for sentence in lun(section.sentenceList):
                        for token_tag in get_tagged_tokens(sentence.tokenization, 'POS'):
                            print(token_tag)
            start_count += 50
            start_count = min(start_count, comm_count)
>>>>>>> a6bdc33b8c5e65fdec5bab0e2f093a69a8e5ef23
def main():
    matches = match_dict("./data/WikiQA-match/train-match.tsv")
    #print(matches)
    print(len(matches.keys()))
    match_tags(matches)


if __name__ == '__main__':
    main()
