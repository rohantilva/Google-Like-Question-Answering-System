class WordEmbeddings:
    def __init__(self):
        from sklearn.metrics.pairwise import cosine_similarity
        import spacy
        import numpy as np
        from numpy import array
        from numpy import matrix
        self.nlp = spacy.load('en')
        self.cosine = cosine_similarity
        self.array = array
        self.matrix = matrix
        self.np = np

    def getDetVal(self, query, answer):
        # query = query.replace(","," ")
        # query = query.replace("'"," ")
        # query = query.replace('"',"")
        # query = query.replace("/"," ")
        # query = query.replace("?","")
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

    def getSumVal(self, query, answer):
        # query = query.replace(","," ")
        # query = query.replace("'"," ")
        # query = query.replace('"',"")
        # query = query.replace("/"," ")
        # query = query.replace("?","")
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

# wordEm = WordEmbeddings()
# print(wordEm.getDetVal("hello world", "hello one of us"))
# print(wordEm.getDetVal("hello world", "hello world"))  
# print(wordEm.getSumVal("hello world", "hello one of us")) 
# print(wordEm.getSumVal("hello world", "hello world"))
