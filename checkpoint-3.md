## Checkpoint 3: Training and evaluating baseline classifier

Due: November 28, 2017


Train a classifier to predict whether a given sentence contains the
answer to a given question.  For the final project this classifier will be integrated into your search
module for reranking the sentences returned from Lucene based on your
query, which should leave to an improved search evaluation score (as
defined in checkpoint 2).  

In this checkpoint we are not concerned
with that integration yet, but instead just wish to ensure you have
trained a classifier on the original WikiQA data.  As one of the
evaluations you need to report on in the final presentation and the
writeup, you need to say how well your classifier does on this WikiQA
dataset, independent of the IR aspect of the task (that is, this
evaluation assumes someone else already searched for and retrieved a
set of sentences, and you are purely concerned with your
classification quality).

For this checkpoint, you need to train a classifier on WikiQA-train,
and optimize with WikiQA-dev, then report your best results on
WikiQA-dev (not WikiQA-test: that is for the end of the semester
only).

You may use any kind of classifier, provided it is not a pregenerated
system already optimized for question answering: we are assuming
something like the SVM or Logistic Regression routines in
scikit-learn.  If in doubt, ask the instructors.

You may use any kind of features, and are encouraged to spend real
effort on this aspect of the project.  What kind of features?  Here
are some examples of binary features that could be useful:

* The question starts with the word 'how' ('where', 'which', ...)
* The answer candidate sentence contains a named entity of type location (as represented in concrete as a TokenTagging)
* The answer candidate sentence has a verb that matches a verb in the question (verbs are linguistic 'parts-of-speech', where there is a TokenTagging layer that contains these automatic annotations)
* The question starts with 'where' and the answer candidate sentence has a named entity of type location
* The main verb of the question (the first token beneath the root node of a depedency parse analysis stored in Concrete) is a synonym in WordNet of a verb in the candidate sentence

A non-binary feature that is between 0 and 1 might be:

* The cosine similarity of the TF IDF vectors of the question and the answer candidate (measuring how many terms overlap, weighted by their IDF)

There are months of features that could be, and have been, defined.  You are encouraged to look through the question answering academic literature in the course of the final project to determine useful potential features.  For this checkpoint you need to at least implement cosine similarity of the question and the answer candidate as a feature.

Submit an Issue .pdf with a reference to the salient commit, and with a small table of your results, which should be:

P:
R:
F1:

After you satisfy this baseline checkpoint, your goal for the project
on this line is to improve the classifier as best as you can.


F1/P/R
========

[F1/P/R](https://en.wikipedia.org/wiki/F1_score), such as (implemented
in
scikit-learn)[http://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html],
is a standard set of metrics for information extraction.  In this case
you have a binary classification problem: for each candidate sentence,
you need to predict whether it does, or does not, answer the question.
A true positive is if you say "yes" and the correct label is "yes"
(1).  A true negative is if you say "no" and the correct label is "no"
(0).  A false positive is if you say "yes" and the answer was "no",
and a false negative is if you say "no" and the answer was "yes".

Construct a classifier, compute F1/P/R, report the results from dev as
according to the instructions above.
