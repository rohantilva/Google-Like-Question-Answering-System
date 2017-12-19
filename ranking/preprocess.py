from tfidf_preprocess import TfidfPreprocess
from qword_preprocess import QwordPreprocess
from word_embeddings import WordEmbeddings
from union_intersect_preprocess import UnionIntersect
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
    def process_dataset(self, dataset, pickle_name):
        tfidf = TfidfPreprocess()
        pack = tfidf.preprocess_tfidf_dataset(dataset)
        sim_vector = pack[0]
        labels = pack[1]
        # sim_vector = sim_vector.flatten()
        # print(sim_vector)
        # qwords = QwordPreprocess()
        # question_vector = qwords.get_question_word_data(dataset)
        # print(question_vector)
        we = WordEmbeddings()
        # det_val_vector = we.get_det_val_dataset(dataset)
        # print(det_val_vector)
        # sum_val_vector = we.get_sum_vals_dataset(dataset)
        # print(sum_val_vector)
        spacy_sim_vector = we.get_spacy_sim_dataset(dataset)
        print(spacy_sim_vector)
        ui = UnionIntersect()
        ui_vector = ui.get_percentage_dataset(dataset)
        print(ui_vector)
        matrix = np.vstack((spacy_sim_vector, ui_vector))
        # matrix = np.vstack((sim_vector, question_vector, sum_val_vector, spacy_sim_vector, ui_vector))
        matrix = matrix.transpose()
        print(matrix)
        processed_data = dict(x=matrix, y=labels)
        with open(str(pickle_name) + ".p", "wb") as p:
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
        spacy_sim_vector = we.get_spacy_sim_dataset(query_candidates)
        ui_vector = ui.get_percentage_dataset(query_candidates)
        feature_matrix = np.vstack((sim_vector, question_vector, sum_val_vector, spacy_sim_vector, ui_vector))
        feature_matrix = matrix.transpose()
        return(feature_matrix)
