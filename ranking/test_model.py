from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.utils import resample
import pickle
import numpy as np
from random import shuffle
import logging

def pre_ranking(x_features, model, query_cands, uuidDict):
    retDict = {}
    probs = model.predict_proba(x_features)
    for i in range(len(probs)):
        prob_yes = probs[i][1]
        logging.info(prob_yes)
        logging.info("\n\n\n\n\n\n\n")
        sentence = query_cands[i][1]
        uuid = uuidDict[sentence]
        retDict[uuid] = prob_yes
    return retDict

def f1_test_set(data, model_path):
    model = pickle.load(open(model_path, "rb"))
    test_data = pickle.load(open(data, "rb"))
    x_test = test_data['x']
    y_test = test_data['y']
    y_test_pred = model.predict(x_test)
    f1 = f1_score(y_test, y_test_pred)
    p = precision_score(y_test, y_test_pred)
    r = recall_score(y_test, y_test_pred)
    print((f1, p, r))
