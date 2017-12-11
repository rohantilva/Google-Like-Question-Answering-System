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
            if caw_info not in sent_match.keys():
                sent_match[caw_info] = [sid]
            else:
                sent_match[caw_info].append(sid)
                #print(sent_match[caw_info])
    return sent_match


def match_tags(match_dict):
    (caw_info, sid) = zip(*match_dict.items())
    caw_info = list(caw_info)
    sid = list(sid)
    print(len(caw_info))
    print(len(sid))
    with FetchCommunicationClientWrapper("ec2-35-153-184-225.compute-1.amazonaws.com", 9090) as fc:
        print("opened connection")
        comm_count = len(caw_info) #fc.getCommunicationCount()
        start_count = 0
        while start_count != comm_count:
            end_count = min(50, comm_count - start_count)
            curr_caws = caw_info[start_count:end_count]
            print(curr_caws)
            comm_ids = [i.split(':')[0] for i in curr_caws]
            print(comm_ids)
            fetchObj = FetchRequest(communicationIds=comm_ids)
            print(fetchObj)
            fr = fc.fetch(fetchObj)
            print("butts")
            print(fr.communications)
            for comm in fr.communications:
                print(comm.id)
                for section in lun(comm.sectionList):
                    print(section)
                    for sentence in lun(section.sentenceList):
                        for token_tag in get_tagged_tokens(sentence.tokenization, 'POS'):
                            #print(token_tag)
                            continue
            start_count += 50
            start_count = min(start_count, comm_count)

def main():
    matches = match_dict("./data/WikiQA-match/train-match.tsv")
    #print(matches)
    print(len(matches.keys()))
    match_tags(matches)


if __name__ == '__main__':
    main()
