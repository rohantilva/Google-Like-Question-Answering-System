import pickle
import gzip

wrong_indices = pickle.load(open("wrong_indices.p", "rb"))

with gzip.open('WikiQA-dev.tsv.gz', 'rb') as f:
    next(f)
    count = 1
    test = 0
    for line in f:
        if count in wrong_indices:
            line = line.decode("UTF-8")
            line = line.split("\t")
            print(line[1])
            print(line[5])
            print()
            test += 1
        count += 1
