class WordEmbeddings:
    def __init__(self):
        from sklearn.metrics.pairwise import cosine_similarity
        import spacy
        from numpy import array
        self.nlp = spacy.load('en')
        self.cosine = cosine_similarity
        self.array = array

    def getArray(self, query, answer):
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

wordEm = WordEmbeddings()
print(wordEm.getArray("hello world", "hello one of us")) 
