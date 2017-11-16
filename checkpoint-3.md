## Checkpoint 3: Training and evaluating baseline classifier

Due: November 29, 2017 at 3 pm.

Train a classifier to predict whether a given sentence contains the
answer to a given question.  After this checkpoint you will integrate
this classifier into your search module to re-rank the sentences
returned from Lucene based on the query.  This should improve the
performance of the overall system (evaluated as in checkpoint 2).  

In this checkpoint we are not concerned
with that integration yet, but instead just wish to ensure you have
trained a classifier on the original WikiQA data.
In the final
presentation and in the write-up you will need to say how well your
classifier performs on this WikiQA
dataset, *independent* of the IR (search) aspect of the system.
That is, the evaluation for *this* checkpoint looks at the quality of
the classifier predictions only; it is not affected by the IR
performance in any way.  (However, we would expect that if you improve
the performance of your classifier, measured by the evaluation for
*this* checkpoint, then you will also improve the performance of your
overall system, measured by the evaluation developed in checkpoint 2.)

For this checkpoint, you need to train a classifier on WikiQA-train
and tune with WikiQA-dev, then report your best results on
WikiQA-dev (not WikiQA-test: that is for the end of the semester
only).

### Model

You may use any kind of classifier, provided it is not a ready-made
question answering system: we are assuming
something like the SVM or Logistic Regression models in
scikit-learn.  (If in doubt, ask the instructors.)

### Features

You may use any kind of features, and are encouraged to spend time
thinking about and developing your features.  Here
are some examples of binary features that could be useful:

* The question starts with the word 'how' ('where', 'which', ...)
* The answer candidate sentence contains a named entity of type location (as represented in concrete as a TokenTagging)
* The answer candidate sentence has a verb that matches a verb in the question (verbs are linguistic 'parts-of-speech', where there is a TokenTagging layer that contains these automatic annotations)
* The question starts with 'where' and the answer candidate sentence has a named entity of type location
* The main verb of the question (the first token beneath the root node of a depedency parse analysis stored in Concrete) is a synonym in WordNet of a verb in the candidate sentence

A non-binary feature that is between 0 and 1 might be:

* The cosine similarity of the TF IDF vectors of the question and the answer candidate (measuring how many terms overlap, weighted by their IDF)

There are months of features that could be, and have been, defined.  You are encouraged to look through the question-answering academic literature in the course of the final project to determine useful potential features.  **For this checkpoint you need to at least implement cosine similarity of the question and the answer candidate as a feature.**

### Evaluation

[F1/P/R (F1 score, precision, and
recall)](https://en.wikipedia.org/wiki/F1_score), such as [implemented
in
scikit-learn](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html),
is a standard set of metrics for information extraction.  In this
project
you have a binary classification problem: for each candidate sentence,
you need to predict whether it does, or does not, answer the question.
A true positive is if you say "yes" and the correct label is "yes"
(1).  A true negative is if you say "no" and the correct label is "no"
(0).  A false positive is if you say "yes" and the answer was "no",
and a false negative is if you say "no" and the answer was "yes".

Construct a classifier, compute F1/P/R, report the results on dev
according to the instructions above.

### Submission

Submit an Issue .pdf to gradescope with a reference to the salient
commit along with a small table of your results in the following
format:

```
P:
R:
F1:
```

After you satisfy this checkpoint, your goal for the project is to
improve the overall question answering system as best as you can; one
way to do this is to improve the classifier.
