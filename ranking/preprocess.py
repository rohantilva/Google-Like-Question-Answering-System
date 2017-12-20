from tfidf_preprocess import TfidfPreprocess
from qword_preprocess import QwordPreprocess
from word_embeddings import WordEmbeddings
import numpy as np
import sklearn.metrics.pairwise
import sklearn
import math
import gzip
from scipy import sparse
import logging
import pickle
import re

class Preprocess:
    def __init__(self, query_candidates, sritem, str_to_uuid):
        self.query_cands = 

    def process_dataset(self, dataset):
        tfidf = TfidfPreprocess()
        pack = tfidf.preprocess_tfidf_dataset(dataset)
        sim_vector = pack[0]
        labels = pack[1]
        sim_vector.flatten()
        qwords = QwordPreprocess()
        question_vector = qwords.get_question_word_data(dataset)
        we = WordEmbeddings()
        det_val_vector = we.get_det_val_dataset(dataset)
        sum_val_vector = we.get_sum_vals_dataset(dataset)
        matrix = np.vstack((sim_vector, question_vector, det_val_vector, sum_val_vector))
        matrix = matrix.transpose()
        processed_data = dict(x=matrix, y=labelsn)
        with open("./processed_" + str(dataset) + ".p", "wb") as p:
            pickle.dump(processed_data, p)


    def process_run(self, query_candidates):
        tfidf = TfidfPreprocess()
        sim_vector = tfidf.preprocess_tfidf_runtime(query_candidates)
        sim_vector.flatten()
        qwords = QwordPreprocess()
        question_vector = qwords.get_question_word_run(query_candidates)
        we = WordEmbeddings()
        det_val_vector = we.get_det_vals_run(query_candidates)
        sum_val_vector = we.get_sum_vals_run(query_candidates)
        feature_matrix = np.vstack((sim_vector, question_vector, det_val_vector, sum_val_vector))
        feature_matrix = matrix.transpose()
        return(feature_matrix)

