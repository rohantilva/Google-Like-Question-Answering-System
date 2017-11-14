from boolean_search import SearchHandler


def test_alive():
    assert SearchHandler().alive()


'''def test_docsByTerm():
    qt = ["cat", "dog", "fish"]
    with open("./sample_index.txt", "r") as f:
        f.readline()
        qms = SearchHandler().docsByTerm(qt, f)
    assert len(qms) != 0
    assert qms.keys() == {'cat', 'dog', 'fish'}

def test_returnDocList():
    qt = ["cat", "dog", "fish"]
    documents = ["doc1", "doc2", "doc3", "doc4"]
    k = 4
    with open("./sample_index.txt", "r") as f:
        f.readline()
        qms = SearchHandler().docsByTerm(qt, f)
    docs = SearchHandler().returnDocList(qms, documents, k)
    assert len(docs) != 0
    assert docs[0].communicationId == "doc1"
'''


def test_oneTerm_twoHits():
    documents = []
    qt = ["zucchini"]
    with open("./sample_index.txt", "r") as f:
        documents = f.readline().split()
        qms = SearchHandler().docsByTerm(qt, f)
    docs = SearchHandler().returnDocList(qms, documents, 10)
    assert len(docs) == 2


def test_oneTermNoHits():
    qt = ["blarp!"]
    with open("./sample_index.txt", "r") as f:
        documents = f.readline().split()
        qms = SearchHandler().docsByTerm(qt, f)
    docs = SearchHandler().returnDocList(qms, documents, 10)
    assert len(docs) == 0
