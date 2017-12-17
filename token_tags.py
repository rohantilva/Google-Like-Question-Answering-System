from concrete.util import lun, get_tokens
from concrete.util.access_wrapper import FetchCommunicationClientWrapper
from concrete import FetchRequest
from concrete.util import get_tagged_tokens
import gzip
import pickle
from collections import OrderedDict


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
        end_count = 25
        sid_count = 0
        while end_count < comm_count:
            curr_caws = caw_info[10:11]
            print(curr_caws)
            comm_ids = {}
            for c in curr_caws:
                c = c.split(':')
                comm_id = c[0]
                section_num = int(c[1])
                sent_num = int(c[2])
                if comm_id not in comm_ids.keys():
                    comm_ids[comm_id] = [[section_num, sent_num]]
                else:
                    comm_ids[comm_id].append([section_num, sent_num])
            print(comm_ids.keys())
            fetchObj = FetchRequest(communicationIds=list(comm_ids.keys()))
            fr = fc.fetch(fetchObj)
            print(fr)
            with open("testing.p", "wb") as p:
                pickle.dump(fr.communications, p)
            return
            for comm in fr.communications:
                for i in range(len(comm_ids[comm])):
                    section_num = comm_ids[comm][i][0]
                    sent_num = comm_ids[com][i][1]
                    if section_num < len(lun(comm.sectionList)):
                        section = lun(comm.sectionList)[section_num]
                    else:
                        continue
                    if sent_num < len(lun(section.sentenceList)):
                        sentence = lun(section.sentenceList)[sent_num]
                    else:
                        continue
                    tokens = get_tokens(sentence.tokenization)
                    tags = get_tagged_tokens(sentence.tokenization, 'POS')
                    t = [i.tag.encode('UTF-8') for i in tags]
                    sid_to_tokens[sid[sid_count][0]] = t
                    sid_count += 1
            start_count += 25
            start_count = min(start_count, comm_count)
            end_count = min(start_count + 25, comm_count -1)
            print(sid_to_tokens)
    return(sid_to_tokens)


def main():
    matches = match_dict("./data/WikiQA-match/train-match.tsv")
    #print(matches)
    print(len(matches.keys()))
    tags = match_tags(matches)
    with open("./train_matches.p", "wb") as p:
        pickle.dump(tags, p)

if __name__ == '__main__':
    main()
