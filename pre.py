import numpy as np
import gzip
from scipy.sparse import csr_matrix
np.set_printoptions(threshold=np.nan)

def preprocess(word_dict, q_list, a_list, min_count=3):
    count = 0
    count1 = 0
    with gzip.open('data/WikiQA/WikiQA-train.tsv.gz', 'rb') as f:
        for line in f:
            line = line.decode('UTF-8')
            for ch in ["\n", "\r", "?"]:
                if ch in line:
                    line = line.replace(ch, "")
            arr = line.split("\t")
            q = arr[1].split(" ")
            a = arr[5].split(" ")
            for word in q:
                if word not in q_list.keys():
                    q_list[word] = [0, count]
                    count += 1
                q_list[word][0] += 1
            for word in a:
                if word not in a_list.keys():
                    a_list[word] = [0, count1]
                    count1 += 1
                a_list[word][0] += 1
                    
        f.seek(0)
        #matrix = csr_matrix((len(a_list), len(q_list)))
        trunc_q_list = dict(
            (k, v) for (k, v) in q_list.items() if v[0] >= min_count)
        trunc_a_list= dict(
            (k, v) for (k, v) in a_list.items() if v[0] >= min_count)
        matrix = np.zeros((len(trunc_a_list.keys()), len(trunc_q_list.keys())))
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
            sub_q_index = 0
            sub_a_index = 0
            sorted_qs = sorted(q_list.keys())
            sorted_as = sorted(a_list.keys())
            for word in q:
                a_index = None
                q_index = None
                if q_list[word][0] >= min_count:
                    q_index = q_list[word][1] - sub_q_index
                else:
                    sub_q_index += 1
                for answer in a:
                    if a_list[word][0] >= min_count:
                        a_index = a_list[answer][1] - sub_a_index
                        matrix[a_index][q_index] = 1
                    else:
                        sub_a_index += 1
                    if a_index and q_index:
                        
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
