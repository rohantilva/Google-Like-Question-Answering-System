from keras.models import Sequential
from keras.layers import Dense, Activation
import pickle
from random import shuffle
import numpy as np


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


def build_model():
    model = Sequential()
    model.add(Dense(20360, input_shape=(2,), activation="sigmoid"))
    #model.add(Dense(1000, activation="linear"))
    #model.add(Dense(500, activation="linear"))
    #model.add(Dense(2, activation="sigmoid"))
    return(model)


def train_model(model, td, dd):
    model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
    x_train = td['x']
    y_train = td['y']
    #(x_train, y_train) = subtractive_balance(x_train, y_train)
    # x_dev = dd['x']
    # y_dev = dd['y']

    model.fit(x_train, y_train, epochs=10, batch_size=32)



def main():
    m = build_model()
    train_data = pickle.load(open("./processed_train.p", "rb"))
    dev_data = pickle.load(open("./processed_dev.p", "rb"))
    train_model(m, train_data, dev_data)
    return

if __name__ == '__main__':
    main()
