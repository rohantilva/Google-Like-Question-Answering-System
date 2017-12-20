from sklearn.metrics.pairwise import cosine_similarity as cosine
import spacy
import numpy as np
from numpy import array
from numpy import matrix
import math
import gzip
import re

class WordEmbeddings:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')

    def __getDetVal(self, query, answer):
        terms1 = self.nlp(query)
        terms2 = self.nlp(answer)
        A = []
        for term in terms1:
            if term.has_vector:
                A.append(term.vector)
        B = []
        for term in terms2:
            if term.has_vector:
                B.append(term.vector)
        A = np.matrix(A)
        B = np.matrix(B)
        A = A.transpose()
        try:
            dotProd = np.dot(B, A)
            dimMax = max(np.shape(dotProd))
            dimMin = min(np.shape(dotProd))
            detSum = 0
            for i in range(dimMax - dimMin + 1):
                if dimMax == np.shape(dotProd)[0]:
                    sub = dotProd[i:i + dimMin, :]
                else:
                    sub = dotProd[:, i:i + dimMin]
                detSum += np.linalg.det(sub)
            detSum = detSum / (dimMax-dimMin+1)
            if math.isnan(detSum):
                detSum = 0
        except:
            return 0
        return detSum

    def __getSumVal(self, query, answer):
        terms1 = self.nlp(query)
        terms2 = self.nlp(answer)
        vector1 = []
        vector2 = []
        for index in range(300):
            vector1.append(0)
            vector2.append(0)
        for term in terms1:
            if term.has_vector:
                vector1 = [term.vector[i]+vector1[i] for i in range(len(term.vector))]
        for term in terms2:
            if term.has_vector:
                vector2 = [term.vector[i]+vector2[i] for i in range(len(term.vector))]
        vector1 = array(vector1).reshape(1, -1)
        vector2 = array(vector2).reshape(1, -1)
        return cosine(vector1, vector2)[0][0]

    def __getSpacySim(self, query, answer):
        terms1 = self.nlp(query)
        terms2 = self.nlp(answer)
        return terms1.similarity(terms2)

    def get_det_val_dataset(self, dataset):
        det_vals = []
        with gzip.open(dataset, 'rb') as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                q = alpha.sub(' ', str(arr[1]))
                a = alpha.sub(' ', str(arr[5]))
                det_vals.append(self.__getDetVal(q, a))
        return np.asarray(det_vals)


    def get_det_vals_run(self, data):
        det_vals = []
        for pair in data:
            alpha = re.compile('[^0-9a-zA-Z]')
            question = str(pair[0])
            question = question.lower()
            answer = str(pair[1])
            answer = answer.lower()
            q = alpha.sub(' ', question)
            a = alpha.sub(' ', answer)
            det_vals.append(self.__getDetVal(q, a))
        return np.asarray(det_vals)


    def get_sum_vals_dataset(self, dataset):
        sum_vals = []
        with gzip.open(dataset, 'rb') as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                q = alpha.sub(' ', str(arr[1]))
                a = alpha.sub(' ', str(arr[5]))
                sum_vals.append(self.__getSumVal(q, a))
        return np.asarray(sum_vals)


    def get_sum_vals_run(self, data):
        sum_vals = []
        for pair in data:
            alpha = re.compile('[^0-9a-zA-Z]')
            question = str(pair[0])
            question = question.lower()
            answer = str(pair[1])
            answer = answer.lower()
            q = alpha.sub(' ', question)
            a = alpha.sub(' ', answer)
            sum_vals.append(self.__getSumVal(q, a))
        return np.asarray(sum_vals)

    def get_spacy_sim_dataset(self, dataset):
        sim_vals = []
        with gzip.open(dataset, 'rb') as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                q = alpha.sub(' ', str(arr[1]))
                a = alpha.sub(' ', str(arr[5]))
                sim_vals.append(self.__getSpacySim(q, a))
        return np.asarray(sim_vals)


    def get_spacy_sim_run(self, data):
        sim_vals = []
        for pair in data:
            alpha = re.compile('[^0-9a-zA-Z]')
            question = str(pair[0])
            question = question.lower()
            answer = str(pair[1])
            answer = answer.lower()
            q = alpha.sub(' ', question)
            a = alpha.sub(' ', answer)
            sim_vals.append(self.__getSpacySim(q, a))
        return np.asarray(sim_vals)
