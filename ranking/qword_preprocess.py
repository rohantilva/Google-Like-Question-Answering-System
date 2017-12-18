class QwordPreprocess:
    def __init__(self):
        import numpy as np
        import sklearn.metrics.pairwise
        import sklearn
        import math
        import gzip
        from scipy import sparse
        import logging
        import pickle
        import re

    def get_question_word(self, dataset):
        q_words = ["", "who", "what", "when", "where", "why", "how", "is", "whom"]
        final_list = []
        with gzip.open(dataset, 'rb') as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                q = alpha.sub(' ', str(arr[1]))
                q = q.split()
                index = 0
                if q[0] in q_words:
                    index = q_words.index(q[0])
                final_list.append(index)
        return final_list