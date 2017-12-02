import numpy as np
import gzip
from scipy.sparse import csr_matrix
np.set_printoptions(threshold=np.nan)

def preprocess(word_dict, q_list, a_list):
    count = 0
    count1 = 0
    with gzip.open('data/WikiQA/WikiQA-train.tsv.gz', 'rb') as f:
        for line in f:
            line = line.decode('UTF-8')
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            line = line.replace("?", "")
            arr = line.split("\t")
            q = arr[1].split(" ")
            a = arr[5].split(" ")
            for word in q:
                if word not in q_list:
                    q_list[word] = count
                    count += 1
            for word in a:
                if word not in a_list:
                    a_list[word] = count1
                    count1 += 1
                    
        f.seek(0)
        #matrix = csr_matrix((len(a_list), len(q_list)))
        matrix = np.zeros((len(a_list), len(q_list)))
        print(matrix.shape)
        counter = 0
        for line in f:
            counter += 1
            if counter == 100:
                print(counter)
            line = line.decode('UTF-8')
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            line = line.replace("?", "")
            arr = line.split("\t")
            q = arr[1].split(" ")
            a = arr[5].split(" ")
            for word in q:
                q_index = q_list[word]
                for answer in a:
                    a_index = a_list[answer]
                    matrix[a_index][q_index] = 1
                #answer = a[0]
                #matrix[a_index[answer]][q_index] = 1

        print(matrix)

        #print(arr)



def main():
    word_dict = {}
    q_list = {}
    a_list = {}
    preprocess(word_dict, q_list, a_list)

if __name__ == '__main__':
    main()
