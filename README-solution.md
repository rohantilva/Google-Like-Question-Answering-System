Total Recall
==
Knowledge Discovery From Text, Fall 2017
Final Project

Group:
Bryan Ki, Jordan Peykar, Rohan Tilva, Matthew Lee, and Hannah Cowley



---
# Table of Contents
1. [Architecture](#architecture)
2. [How to Run](#how-to-run)
3. [Improvements](#improvements)
    * [Query Expansion](#query-expansion)
    * [Stemming](#stemming)
    * [Ranking and Classification](#ranking-and-classification)
4. [Other Things We Tried](#other-things-we-tried)
5. [Error Analysis](#error-analysis)
5. [Results](#results)
6. [Areas for Improvement](#areas-for-improvement)
7. [Conclusions](#conclusions)
8. [Sources](#sources)

---
## Architecture

![](https://i.imgur.com/KOIFQGn.png)

---
## How to Run
_Note, there is no-need to re-preprocess train/dev/test data, or re-train our MLP model -- all are saved to pickles. Instructions are included in Step 1 in case you'd like to re-run._
1. Train model 
    a. `python3 ranking/test_preprocess.py`: saves pickles of preprocessed train, dev, and test data
    b. `python3 ranking/train_model.py`: uses the preprocessed data to train the MLP. Saves a pickle of this model to `trained_model.p`
2. Standup UI
    a. `docker build -t search-passthrough -f  Dockerfile.search .`
    b. `docker-compose up`
3. Enter query into UI and hit enter

---

## Improvements
### Query Expansion
Query Expansion aims to broaden the scope of the question being asked. For example, when searching "Who created the first computer?" We would like to expand the scope of the question to examples such as: "Who invented the first computer?" "Who designed the first computer?" "Who created the fundamental computer?"

Our team implemented query expansion by using the Natural Language Toolkit's (NLTK) WordNet. We stemmed each word in the query and tagged each word. Then, we found synonyms for adjectives, adverbs, and verbs. When creating similar queries for verbs, we do not create synonym for linking verbs such as is, are, was, am. This is so that the expansion of verbs is more likely to target main verbs of the sentence. A list of queries was then formed, with the original query being the first in the list and was fed individually into the search model.

One of the main challenges using Wordnet's synonym set feature (synset) was that the list of synonyms was too broad and varied. For example, a synonym for the word "run" was the word "chop-chop." For our queries, we aimed to expand the search on verbs, adverbs, and adjectives, but by then end of the expansion, some of the queries meant something completely different from the original query.

One possible upgrade to our QA model to look into would be to somehow recieve synonyms based on the relative similarity of the synonym and the original word. This would allow for the scope of the queries to widen, but not so much that the original query loses meaning.

Synset was able to find synonyms very quickly, and expansion of the queries did not take a large toll on perfomance.

### Stemming

Stemming was used to get the root form of each verb in the query. By stripping the tenses of each verb, we were able to get the root verb, which led to more successful and accurate queries. Stemming was also useful for the results portion as well. Stemming the results allowed us to accurately perform cosine similarity on verbs that may have not been the same tense.


### Ranking and Classification: Additional Features
#### TF-IDF Cosine Similarity
We took the cosine similarity between each of the words in the query and each of the words in the answer, for each question/answer pair. When calculating TF-IDF scores, we stopword filtered by removing the top 200 most frequently used question words and the top 200 most frequently used answer words. We then took the cosine similarity between the tf-idf scores, creating a sparse vector according to cosine similarity between unique question and answer words found in the dataset.
#### Question Words
We assumed the first word in the query to be an identifying word for what kind of question is being asked. Therefore, we indexed the first word of the query and compared it to a list of question words, `["", who", "what", "when", "where", "why", "how", "is", "whom"]`. If the query question word matched one of the words in the list, then the index of the matching word was marked. If no matching question word was found, then index 0 was marked, corresponding to the empty string. We hoped that this feature would help the model to find more accurate answers, as it would help to differentiate between queries and answer candidates that had the same subjects, but really answer different questions. For example, although the queries "How deep is the ocean?" and "Why is the ocean deep?" have the same number of words, most of the same exact words, and the same subject, they clearly are asking for two different answers. Thus, matching question word to answer could help differentiate among answer choices that, without this feature, might be seen to satisfy either query.

#### Sums of word embeddings
For this feature we decided to measure the cosine similarity of the two sentences by summing the individual word embeddings into a vector for the query and a vector for the answer. This feature can easily calculate a similarity between 0 and one of the query words to the answer words. The big issue with this method however is that in rare cases the word embedding sum can be close for two very different sentences. Since word embeddings are of length greater than 300, this overlap is rare.

#### Determinants of word embeddings
The determinant of the word embedding vectors, which is the measure of linear independence, allowed us to evaluate the cosine similarity between all of the involved items (Boratto et al. 2016). Before, we were using cosine similarity to measure two different full sentences, but with the determinant, we were able to use this same type of metric to measure the similarity of all the word embedding vectors. This metric was essential as it allowed us to compare vectors for our word embeddings feature.

#### % Overlap between query and answer (Jaccard Similarity)
As another similarity measure in addition to cosine similarity, we decided to quantify the number of words that each question/answer pair had in common. To do this, we took the intersection of the query and the answer (to find common words), and then took the union of the query and answer (to find the total number of distinct words). We then divided the number of words in the intersection by the number of words in the union. Effectively, this serves as the percentage of words in common between the query and answer. By including this as a feature, we hoped that the model would be able to better classify answers that were yes/no instances (pairs with a higher percentage for this feature would be more likely to have an answer that correctly answered the question). 

#### SpaCy sentence similarity metric
The sentence similarity metric is able to use context clues to determine similarity between sentences. For example, in the sentence "I got new Schwinn pedals", SpaCy is able to use "pedals" to determine the word "Schwinn" that is out of the vocabulary that spaCy has stored.
SpaCy also uses a 4-layer CNN with individual units who have receptive fields sensitive to 4-grams on either side of the word in question to classify the unknown vocabulary word. The module uses the same word embeddings that were used in the other features to complete this task.
This capability is fitting for our task because a user's query may not have identical words to the answer. Therefore, by calculating the similarity between question and answer, we are more able to understand words that may not be included in our dataset.
The documentation for this can be found [here](https://spacy.io/usage/vectors-similarity).

### Ranking and Classification: Using a Multi-Layer Perceptron
Although we started off with an SVM, we found better F1 scores from a multi-layer perceptron model instead. A multi-layer perceptron uses linear perceptrons stacked into layers. The advantage of the multi-layer approach is that having hidden layers can discriminate between classes of non-linearly separable data. We think that this model worked because the high-dimensional space within which question/sentence pairs are encoded as 1 or 0 may not be able to be separated by a hyperplane. Therefore, a MLP is well-suited to this discrimination task. 
Our MLP was taken from scikit-learn. We trained it through trying various parameter combinations, using subtractive balancing, and resampling (similarly to homework 2). You can find our model pickled `trained_model.p`, but details of the model have been reproduced below:

**Model Details:**
```python
MLPClassifier(activation='tanh', alpha=9.999999999999999e-05,
       batch_size='auto', beta_1=0.9, beta_2=0.999, early_stopping=False,
       epsilon=1e-08, hidden_layer_sizes=(100,), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
       solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
       warm_start=False)
```

### Ranking and Classification: Using Logistic Regression
When evaluating success @k, we found that with our MLP we were getting really horrible results. Upon looking at our probabilities of yes versus no for individual instances, we found that our MLP was predicting either 0 or ~1 each time. Therefore, although our model had good recall (ie: all positive instances were .98 and above), many negative instances were included in there too (ie: a negative instance may be marked with probability of being positive = .9888, while a positive instance may be marked as probability = .9887). When switching to a logistic regression model (albeit, at the last minute), we found our model was predicting a more continuous distribution of probabilities. 
We found that our preprocessing for all of the features described above was taking far too long, so this logistic regression only uses three features: cosine similarity of tfidf vectors, question words, and Jaccard Similarity (percent overlap). 

### Ranking and Classification: Using continuous predictions for ranking
With the SVM that we used originally, we received hard predictions regarding yes/no instances. Unfortunately, this left us with no real method to rerank our answers, so we had the idea of using probabilities to rerank instead -- question/answer pair instances with higher probability of being a "YES"-instance would be ranked higher than instances with lower probabilities of being a "YES"-instance. We received these probabilities by using the MLP's `model.predict_proba(x)` function which, instead of giving yes/no predictions, gave a tuple of probabilities: one value for the probability of not answering the question, and one value for the probability of actually answering the question. 

### Ranking and Classification: Modified Subtractive Balance
When training our model, we realized that without using subtractive balancing, our model only predicted "no" for the most part, since there were much more training instances labeled "no" than labeled "yes". So, we incorporated subtractive balancing (the code taken from HW2), meaning that we trained our model on an equal number of "yes" and "no" instances. This allowed our model to actually predict "yes" in some cases rather than always predicting "no". We also had the idea of modifying (increasing) the number of negative instances trained on, since this would be more indicative of the real data (since there are more negative instances than positive instances). We found that increasing the number of negative instances by 80% increased the F1 score consistently by .03 or .04. For example, if there were 1000 positive instances being trained on, there were about 1800 negative instances being trained on.

For example, this is the one line we changed in the subtractive balance method to accomplish what we wanted:
```python
id_bal = np.array(id_pos + id_neg[:int(num_pos * 1.8)])
```

---
## Other Things We Tried

### Classification Feature: Concrete-ly annotated POS tagging
For a long time we worked on getting the part of speech tagging from the wikipedia text to train our model on. However, we ended up giving up on this feature because getting the concrete-ly annotated information and then performing computations over it proved to be too slow. Given a better algorithm for obtaining this information and matching up, for example, the subject of the question to the subject in the answer, we think that this feature could have greatly improved our classifier. 

### Classification Model: SVM
An SVM was the first classifier we used to receive F1 scores. With the SVM, we were unable to break F1 scores of .15, so we ended up switching our classifier to an MLP, which gave consistently higher F1 scores. We hypothesize that the MLP was better suited for the data since the data may not be linearly separable (the SVM is a linear classifier). 


### Classification Model: Keras Sequential Model
In an attempt to build off the MLP classifier that we used from scikit-learn, we attempted to build our own deep net using Keras. Our group has little Machine Learning experience, and were roadblocked by simple issues that we could not resolve. In this case, the problem that roadblocked us was the fact that we did not know what the shape of the first layer was (and thus we could not specify the number of input layers into the model). Members in our group are only versed in using PyTorch and Keras for images, in which case the input number of layers would be, let's say, the number of pixels in the image. However, there was no equivalent for these question/answer pair sentences. With more time, ML experience, and a better understanding of input shapes, we believe we could have made a deep net work for classifying our query/answer candidate pairs, and we believe it would have yielded better performance than the MLP.

## Error Analysis
**Questions we got wrong (on dev):**

We found that questions that necessitated a numeric answer (such as a date or number) were more frequently wrong than questions that asked for answers that were non-numeric. We hypothesize that this is because there are often many different numbers associated with subjects. For example, if a question query was "How big is the Pacific Ocean?", then the search engine might return results for the sizes of different oceans, not necessarily for the size of the Pacific Ocean. Thus it could be confounded by similar results, but not exact results, leading to negative instances. 

We also found that certain questions that started with specific words were more frequently wrong than others. For example, we found questions that started with "Where" and "What" to be more frequently wrong. We determined this by printing out the misclassified dev questions, and then determining what the ratio of questions that started with a given word was to the total number of incorrect questions. We also calculated this for the whole dev dataset: number of instances which started with a given question word divided by the number of total dev instances. We then compared the proportions as is shown in the following picture. 

![](https://i.imgur.com/XEn00nY.png)

As was stated earlier, we can see that "where" questions and "what" questions have a higher probability of being classified wrong by the model.

![](https://i.imgur.com/Xk1XRlj.png)
In this graph, we see red bars correspond to the proportion of the question type that we got wrong on dev out of all the query/answer pairs we misclassified. In blue, we see how often these types of questions appear in the data. We disproportionately get where and what questions wrong.


**Questions we got right (on dev):**
![](https://i.imgur.com/99JL8C1.png)
This graph, by contrast, breaks down the classifications we get right by the question word they start with. We see that we get about proportional results for this one. This corresponds to our relatively high recall scores.

In addition, the number of positive dev instances is a lot greater than negative instances, meaning the model classified the majority of answers correctly. We observed that questions that were clearly not ambiguous (clearly only had one answer) were usually classified correctly.


---
## Results

**Baseline Success @k:**
Run on entire WikiQA dataset
|     K   | Success    |
| ------------- | ------------- |
| 1    | 0.0 |
| 10      | 0.06  |
| 100 | 0.18  |
| 1000 | 0.30   |


**Final Success @k: Logistic Regression**
_Both re-ranking and query expansion implemented. Using a **Logistic Regression model** with only the 3 features described above_
|     K   | Success   |
| ------------- | ------------- |
| 1    |  0.0 |
| 10      | .01 |
| 100 | .09  |
| 1000 | .30  |

**Final Success @k: MLP**
_Both re-ranking and query expansion implemented. Using a **MLP** with only the 3 features described above_


|     K   | Success   |
| ------------- | ------------- |
| 1    |  0.00 |
| 10      | 0.0 |
| 100 | .04  |
| 1000 |  .26 |


**Checkpoint 3 MLP F1, Precision, and Recall on Dev:**
|     Metric  | Value   |
| ------------- | ------------- |
| Precision    | .08  |
| Recall      | .55 |
| F1 | .133  |

**Final MLP F1, Precision, and Recall:**
_With all 6 classifier features_
|     Metric  | Dev Result | Test Result |
| ------------- | -------| ------------- |
| Precision    | .11 | .11|
| Recall      | .54  | .3 |
| F1 | .18 | .16 | 


**Final Logistic Regression F1, Precision, and Recall:**
_With only the 3 simple classifier features_
|     Metric  | Dev Result | Test Result |
| ------------- | -------| ------------- |
| Precision    |.10  | .10 |
| Recall      | .24  | .23 |
| F1 | .14 | .14  | 

**Graph of F1 Scores On Dev Over Project:**
![](https://i.imgur.com/nykddgW.png)

We found that F1 scores increased as the number of features implemented increased. Initially, our first feature, tf-idf cosine similarity, we started at a score of 0.09. With stop-world filtering, increased to 0.12. After implementing the Multilayer Perceptron Neural Network, there was a considerable increase in F1 score to 0.16, and finally after substractive balancing, we reached our maximum F1 score of 0.18. 


---
## Areas for Improvement
* Increasing F1 scores
    * Better feature engineering
    * Using a deep net instead
    * More positive data
* MLP parameter adjustment
    * Need more ML knowledge to be able to completely optimize our MLP
* Using a classifier that provides more continuous probability results
    * Needed more time to train our logistic regression model; we could probably make this better


---
## Conclusions
We found that all of our features, particularly stemming and using query expansion, and switching to the MLP classifier significantly improved our scores. Our F1 score grew from when we started (0.09 to 0.18). For future studies, we would like to investigate using a deep neural network as our classifier, including more features, and adding more positive data.

---
## Sources
* L. Boratto, S. Carta, G. Fenu and R. Saia, "Exploiting a Determinant-Based Metric to Evaluate a Word-Embeddings Matrix of Items," 2016 IEEE 16th International Conference on Data Mining Workshops (ICDMW), Barcelona, 2016, pp. 984-991.
    * See section on determinants of word embeddings
* Chen, Tongfei and Van Durme, Benjamin. Discriminative Information Retrieval for Question Answering Sentence Selection. In Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: Volume 2, Short Papers, pages 719-725. 2017.
    * Got an example of success @k from this paper
* Dong, Li and Mallinson, Jonathan and Reddy, Siva, and Lapata, Mirella. Learning to Paraphrase for Question Answering. 2017.
    * Gave multiple ideas about paraphrasing for query expansion. Although we didn't have time to implement paraphrasing, it helped us understand query expansion a little bit better.

---
