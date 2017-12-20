import numpy as np
import sklearn.metrics.pairwise
import sklearn
import math
import gzip
from scipy import sparse
import logging
import pickle
import re
import numpy as np

class UnionIntersect:
    def __get_percentage(self, question, answer):
        question = question.split(" ")
        answer = answer.split(" ")
        intersection = list(set(question).intersection(answer))
        num_intersect = len(intersection)

        union = list(set(question).union(answer))
        num_union = len(union)

        feat = num_intersect/num_union
        return feat

    def get_percentage_dataset(self, dataset):
        vals = []
        with gzip.open(dataset, 'rb') as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                q = alpha.sub(' ', str(arr[1]))
                a = alpha.sub(' ', str(arr[5]))
                vals.append(self.__get_percentage(q, a))
        return np.asarray(vals)

    def get_percentage_run(self, data):
        vals = []
        for pair in data():
            vals.append(self.__get_percentage(pair[0], pair[1]))
        return np.asarray(vals)
