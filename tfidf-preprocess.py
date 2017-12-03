import numpy as np
import sklearn.metrics.pairwise
import math
import gzip

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


def cosine_sim(dataset, q_scores, a_scores):
    sim_vec = []
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
            qscore_vec = []
            for w in q:
                qscore_vec.append(q_scores[w])
            ascore_vec = []
            for w in a:
                ascore_vec.append(a_scores[w])
            qscore_vec = np.asarray(qscore_vec)
            #qscore_vec = qscore_vec.reshape(-1, 1)
            print(qscore_vec)
            ascore_vec = np.asarray(ascore_vec)
            ascore_vec = np.transpose(ascore_vec)

            #ascore_vec = ascore_vec.reshape(-1, 1)
            print(ascore_vec)
            #cos_sim = sklearn.metrics.pairwise.cosine_similarity(qscore_vec, ascore_vec)
            sim_vec.append(cos_sim)
    print(sim_vec)
    return(sim_vec)

def test():
    vec1 = [1, 0, -1]
    vec2 = [-1, -1, 0]
    #vec2 = np.transpose(vec2)
    d = np.dot(vec1, vec2)
    #denom = vec1.size * vec2.size
    #cos = d/denom
    csim = sklearn.metrics.pairwise.cosine_similarity(vec1, vec2)
    print(csim)

def main():
    dpath = "data/WikiQA/WikiQA-train.tsv.gz"
    tfidf = calc_tfidf(dpath, {}, {})
    q_scores = tfidf[0]
    a_scores = tfidf[1]
    #cosine_sim(dpath, q_scores, a_scores)
    test()

if __name__ == '__main__':
    main()