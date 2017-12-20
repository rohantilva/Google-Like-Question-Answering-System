import numpy as np
import sklearn.metrics.pairwise
import sklearn
import math
import gzip
from scipy import sparse
import logging
import pickle
import re

class TfidfPreprocess:

    def __get_distinct_words_labels_dataset(self, dataset):
        distinct_words = {}
        labels = []
        count = 0
        with gzip.open(dataset, 'rb') as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                q = alpha.sub(' ', str(arr[1]))
                q = q.split()
                a = alpha.sub(' ', str(arr[5]))
                a = a.split()
                label = int(arr[6])
                labels.append(label)
                for word in q:
                    if word not in distinct_words.keys():
                        distinct_words[word] = count
                        count += 1
                for word in a:
                    if word not in distinct_words.keys():
                        distinct_words[word] = count
                        count += 1
        return(distinct_words, np.asarray(labels))

    
    def __get_distinct_words_run(self, data):
        distinct_words = {}
        count = 0
        for pair in data:
            q = str(pair[0]).split()
            q = q.lower()
            a = str(pair[1]).split()
            a = a.lower()
            alpha = re.compile('[^0-9a-zA-Z]')
            question = alpha.sub(' ', q)
            answer = alpha.sub(' ', a)
            for word in question:
                if word not in distinct_words.keys():
                    distinct_words[word] = count
                    count += 1
            for word in answer:
                if word not in distinct_words.keys():
                    count += 1
        return(distinct_words)


    def __calc_tfidf_dataset(self, dataset, q_list, a_list):
        qids = {}
        aids = {}
        with gzip.open(dataset, 'rb') as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                qid = arr[0]
                qids[qid] = True
                aid = arr[4]
                aids[aid] = True
                q = alpha.sub(' ', str(arr[1]))
                q = q.split()
                a = alpha.sub(' ', str(arr[5]))
                a = a.split()
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
        question_count = len(qids.keys())
        answer_count = len(aids.keys())
        mf_qs = sorted(q_list.items(), key=lambda x: x[1][0], reverse=True)
        mf_as = sorted(a_list.items(), key=lambda x: x[1][0], reverse=True)
        mf_qs = mf_qs[:200]
        mf_as = mf_as[:200]
        q_list = {word: counts for word, counts in q_list.items() if word not in mf_qs}
        a_list = {word: counts for word, counts in a_list.items() if word not in mf_as}
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


    def __calc_tfidf_run(self, data):
        q_list = {}
        a_list = {}
        answer_count = 0
        for pair in data:
            q = str(pair[0]).split()
            q = q.lower()
            a = str(pair[1]).split()
            a = a.lower()
            alpha = re.compile('[^0-9a-zA-Z]')
            question = alpha.sub(' ', q)
            answer = alpha.sub(' ', a)
            unique_qw = dict((el, True) for el in question)
            unique_aw = dict((el, True) for el in answer)
            for word in question:
                if word not in q_list.keys():
                    q_list[word] = [0, 0]
                q_list[word][0] += 1
            for key in unique_qw.keys():
                q_list[key][1] += 1
            for word in answer:
                if word not in a_list.keys():
                    a_list[word] = [0, 0]
                a_list[word][0] += 1
            for key in unique_aw.keys():
                a_list[key][1] += 1
        answer_count = len(data)
        q_scores = {}
        for k in q_list.keys():
            val = q_list[k]
            tf = val[0]
            score = tf * math.log((float(1)) / float(val[1]))
            q_scores[k] = score
        a_scores = {}
        for k in a_list.keys():
            val = a_list[k]
            tf = val[0]
            score = tf * math.log((float(answer_count) / float(val[1])))
            a_scores[k] = score
        return(q_scores, a_scores)


    def __cosine_sim_dataset(self, dataset, q_scores, a_scores, temp):
        sim_vec = []
        with gzip.open(dataset, 'rb') as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                q = alpha.sub(' ', str(arr[1]))
                q = q.split()
                a = alpha.sub(' ', str(arr[5]))
                a = a.split()
                qscore_vec = np.zeros(len(temp))
                for w in q:
                    if w in temp.keys():
                        qscore_vec[temp[w]] = q_scores[w]
                ascore_vec = np.zeros(len(temp))
                for w in a:
                    if w in temp.keys():
                        ascore_vec[temp[w]] = a_scores[w]
                qscore_sparse = sparse.csr_matrix(qscore_vec)
                ascore_sparse = sparse.csr_matrix(ascore_vec)
                cos_sim = sklearn.metrics.pairwise.cosine_similarity(qscore_sparse, ascore_sparse)
                sim_vec.append(cos_sim)
        return(sim_vec)
    

    def __cosine_sim_run(self, data, q_scores, a_scores, unique):
        sim_vec = []
        for pair in data:
            q_score_vec = np.zeros(len(unique))
            a_score_vec = np.zeros(len(unique))
            question = pair[0].split()
            answer = pair[1].split()
            for word in question:
                if word in unique.keys():
                    q_score_vec[unique[word]] = q_scores[word]
            for word in answer:
                if word in unique.keys():
                    a_score_vec[unique[word]] = a_scores[word]
            q_score_sparse = sparse.csr_matrix(q_score_vec)
            a_score_sparse = sparse.csr_matrix(a_score_vec)
            cos_sim = sklearn.metrics.pairwise.cosine_similarity(q_score_sparse, a_score_sparse)
            sim_vec.append(cos_sim)
        return(sim_vec)
                

    def preprocess_tfidf_dataset(self, dataset):
        first_pass = self.__get_distinct_words_labels_dataset(dataset)
        distinct_word = first_pass[0]
        labels = first_pass[1]
        tfidf = self.__calc_tfidf_dataset(dataset, {}, {})
        q_scores = tfidf[0]
        a_scores = tfidf[1]
        sims = np.asarray(self.__cosine_sim_dataset(dataset, q_scores, a_scores, distinct_word))
        return (sims, labels)
    

    def preprocess_tfidf_runtime(self, data):
        first_pass = self.__get_distinct_words_run(data)
        distinct_word = first_pass
        tfidf = self.__calc_tfidf_run(data)
        q_scores = tfidf[0]
        a_scores = tfidf[1]
        sims = np.asarray(self.__cosine_sim_run(data, q_scores, a_scores, distinct_word))
        return sims