from concrete.util import lun, get_tokens
from concrete.util.access_wrapper import FetchCommunicationClientWrapper
from concrete import FetchRequest
import gzip

def get_tags(dataset, match):
    with gzip.open(dataset, "rb") as f:
        next(f)
        for line in f:
            line = line.decode('UTF-8')
            line = line.lower()
            arr = line.split("\t")
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
            if sid not in sent_match.keys():
                sent_match[sid] = [caw_info]
            else:
                sent_match[sid].append(caw_info)
    return sent_match


def main():
    matches = match_dict("./data/WikiQA-match/train-match.tsv")
    print(matches)


if __name__ == '__main__':
    main()
