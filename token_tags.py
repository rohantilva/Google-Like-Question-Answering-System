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
            sid = str(arr[0])
            caw_info = arr[2].encode('UTF-8')
            if caw_info not in sent_match.keys():
                sent_match[caw_info] = [sid]
            else:
                sent_match[caw_info].append(sid)
                #print(sent_match[caw_info])
    s_match = OrderedDict(sorted(sent_match.items(), key=lambda i: i[0]))
    print(s_match)
    return s_match


def match_tags(match_dict):
    sid_to_tokens = {}
    (caw_info, sid) = zip(*match_dict.items())
    caw_info = list(caw_info)
    sid = list(sid)
    print(sid)
    with FetchCommunicationClientWrapper("ec2-35-153-184-225.compute-1.amazonaws.com", 9090) as fc:
        print("opened connection")
        comm_count = len(caw_info)
        start_count = 0
        end_count = 5
        sid_count = 0
        while end_count < comm_count:
            curr_caws = caw_info[start_count:end_count]
            comm_ids = [i.split(':')[0] for i in curr_caws]
            print(comm_ids)
            fetchObj = FetchRequest(communicationIds=comm_ids)
            fr = fc.fetch(fetchObj)
            comm_num = 0 
            for comm in fr.communications:
                info = curr_caws[comm_num].split(':')
                section_num = int(info[1])
                sent_num = int(info[2])
                section = lun(comm.sectionList)[section_num]
                sentence = lun(section.sentenceList)[sent_num]
                tokens = get_tokens(sentence.tokenization)
                tags = get_tagged_tokens(sentence.tokenization, 'POS')
                sid_to_tokens[sid[sid_count][0]] = tags
                comm_num += 1
                sid_count += 1
            start_count += 5
            start_count = min(start_count, comm_count)
            end_count = min(start_count + 5, comm_count -1)
            print(sid_to_tokens)
    return(sid_to_tokens)


def main():
    matches = match_dict("./data/WikiQA-match/train-match.tsv")
    #print(matches)
    print(len(matches.keys()))
    match_tags(matches)


if __name__ == '__main__':
    main()
