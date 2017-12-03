import numpy as np
import sklearn.metrics.pairwise
import math
import gzip
from scipy import sparse
import logging

def get_distinct_words(dataset):
    distinct_words = {}
    count = 0
    with gzip.open(dataset, 'rb') as f:
        next(f)
        for line in f:
            line = line.decode('UTF-8')
            for ch in ["\n", "\r", "?"]:
                if ch in line:
                    line = line.replace(ch, "")
            line = line.lower()
            arr = line.split("\t")
            q = arr[1].split(" ")
            a = arr[5].split(" ")
            for word in q:
                if word not in distinct_words.keys():
                    distinct_words[word] = count
                    count += 1
            for word in a:
                if word not in distinct_words.keys():
                    distinct_words[word] = count
                    count += 1
    return distinct_words


def calc_tfidf(dataset, q_list, a_list):
    question_count = 0
    with gzip.open(dataset, 'rb') as f:
        next(f)
        for line in f:
            question_count += 1
            line = line.decode('UTF-8')
            for ch in ["\n", "\r", "?"]:
                if ch in line:
                    line = line.replace(ch, "")
            line = line.lower()
            arr = line.split("\t")
            q = arr[1].split(" ")
            a = arr[5].split(" ")
            unique_qw = dict((el, True) for el in q)
            unique_aw = dict((el, True) for el in a)
            for word in q:
                if word not in q_list.keys():
                    q_list[word] = [0, 0]
                q_list[word][0] += 1
            for k in unique_qw.keys():
                q_list[k][1] += 1
            for word in a:
                if word not in a_list.keys():
                    a_list[word] = [0, 0]
                a_list[word][0] += 1
            for k in unique_aw.keys():
                a_list[k][1] += 1           
    answer_count = question_count
    q_scores = {}
    for k in q_list.keys():
        val = q_list[k]
        tf = val[0]
        score = tf * math.log((float(question_count))/ float(val[1]))
        q_scores[k] = score
    a_scores = {}
    for k in a_list.keys():
        val = a_list[k]
        tf = val[0]
        score = tf * math.log((float(answer_count))/ float(val[1]))
        a_scores[k] = score
    f.close()
    return (q_scores, a_scores)


def new_cosine_sim(dataset, q_scores, a_scores, temp):
    sim_vec = []
    line_count = 0
    with gzip.open(dataset, 'rb') as f:
        next(f)
        for line in f:
            line_count += 1
            line = line.decode('UTF-8')
            for ch in ["\n", "\r", "?"]:
                if ch in line:
                    line = line.replace(ch, "")
            line = line.lower()
            arr = line.split("\t")
            q = arr[1].split(" ")
            a = arr[5].split(" ")
            qscore_vec = np.zeros(len(temp))
            for w in q:
                qscore_vec[temp[w]] = q_scores[w]
            ascore_vec = np.zeros(len(temp))
            for w in a:
                ascore_vec[temp[w]] = a_scores[w]
            qscore_sparse = sparse.csr_matrix(qscore_vec)
            ascore_sparse = sparse.csr_matrix(ascore_vec)
            cos_sim = sklearn.metrics.pairwise.cosine_similarity(qscore_sparse, ascore_sparse)
            sim_vec.append(cos_sim)
    return(sim_vec)


def main():
    dpath = "data/WikiQA/WikiQA-train.tsv.gz"
    temp = get_distinct_words(dpath)
    tfidf = calc_tfidf(dpath, {}, {})
    q_scores = tfidf[0]
    a_scores = tfidf[1]
    sims = new_cosine_sim(dpath, q_scores, a_scores, temp)

if __name__ == '__main__':
    main()
