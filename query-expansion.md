## Query Expansion

To improve your initial search results you may want to add extra words
to your query.  Two examples of how you could generate extra terms are:

* WordNet
* Pre-trained embeddings (e.g., glove, word2vec, MV-LSA)

NLTK has an API for WordNet: that is a good starting point for that resource.

The word embeddings are all based on a notion of cosine similarity =
semantic closeness.  Various packages exist for finding similar words
based on pretrained embeddings, such as [Gensim's support for
word2vec](https://radimrehurek.com/gensim/models/word2vec.html).
