import gzip
import csv

def calc_kscore(query, qmatches, k):
    truth = []
    with gzip.open("WikiQA-train.tsv.gz", "r") as wiki:
        reader = csv.reader(wiki)
        next(reader)
        for row in reader:
            if row[1] == query and row[6] ==  1:
                truth.append(row[5])
            else:
                continue
    kmatches = qmatches[:k]
    correct = 0
    for m in kmatches:
        if m in truth:
            correct += 1
    return(correct / k)



