from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score, accuracy_score
import pickle
import numpy as np
from random import shuffle


def subtractive_balance(x, y):
    '''
    Given feature matrix x and label vector y, return subset of x and y
    (subset of the rows) such that there are as many positive labels
    as negative labels.
    Data that we have has more negative than positive. But any ML algos
    prefer a balance between pos and negative. Subtractive balancing
    removes negative examples until a balance is reached between pos
    and negative exemplars.
    '''

    # Compute the row indices of positive, negative samples
    id_pos = [i for i in range(y.shape[0]) if y[i] == 1]
    id_neg = [i for i in range(y.shape[0]) if y[i] == 0]

    # Create an array of the row indices of all positive samples and
    # a random subset of the negative samples (equal in size to the set
    # of all positive samples).
    num_pos = len(id_pos)
    shuffle(id_neg)
    id_bal = np.array(id_pos + id_neg[:num_pos])

    # Return features (x) and labels (y) for our new, balanced subset of
    # the data.
    print('balancing {} samples down to {}'.format(
        y.shape[0], id_bal.shape[0]))
    return (x[id_bal], y[id_bal])



def train_model(train_data, dev_data):
    model = LinearSVC()
    x_train = train_data['x']
    x_train = x_train.reshape(-1, 1)
    y_train = train_data['y']
    (x_train, y_train) = subtractive_balance(x_train, y_train)
    model.fit(x_train, y_train)

    x_dev = dev_data['x']
    x_dev = x_dev.reshape(-1, 1)
    y_dev = dev_data['y']
    y_hat = model.predict(x_dev)

    acc = accuracy_score(y_dev, y_hat) 
    f1 = f1_score(y_dev, y_hat)

    for i in range(len(y_dev)):
        print((y_dev[i], y_hat[i]))

    print("Accuracy: " + str(acc))
    print("F1: " + str(f1))


def main():
    train_data = pickle.load(open("./processed_train.p", "rb"))
    dev_data = pickle.load(open("./processed_dev.p", "rb"))
    train_model(train_data, dev_data)

    


if __name__ == '__main__':
    main()