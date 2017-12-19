from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np
from numpy import array
from numpy import matrix

class WordEmbeddings:
    def __init__(self):
        self.nlp = spacy.load('en')

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
        A = self.np.matrix(A)
        B = self.np.matrix(B)
        A = A.transpose()
        dotProd = self.np.dot(B, A)
        dimMax = max(self.np.shape(dotProd))
        dimMin = min(self.np.shape(dotProd))
        detSum = 0
        for i in range(dimMax - dimMin + 1):
            sub = dotProd[i:i + dimMin, :]
            detSum += self.np.linalg.det(sub)
        detSum = detSum / (dimMax-dimMin+1)
        return detSum

    def __getSumVal(self, query, answer):
        terms1 = self.nlp(query)
        terms2 = self.nlp(answer)
        vector1 = []
        vector2 = []
        for index in range(384):
            vector1.append(0)
            vector2.append(0)
        for term in terms1:
            if term.has_vector:
                vector1 = [term.vector[i]+vector1[i] for i in range(len(term.vector))]
        for term in terms2:
            if term.has_vector:
                vector2 = [term.vector[i]+vector2[i] for i in range(len(term.vector))]
        vector1 = self.array(vector1).reshape(1, -1)
        vector2 = self.array(vector2).reshape(1, -1)
        return self.cosine(vector1, vector2)[0][0]

    
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
        for pair in data():
            det_vals.append(self.__getDetVal(pair[0], pair[1]))
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
        for pair in data():
            sum_vals.append(self.__getSumVal(pair[0], pair[1]))
        return np.asarray(sum_vals)

    

