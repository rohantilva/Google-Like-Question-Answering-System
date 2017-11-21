## Answer Triggering

Following the terminology of the [WikiQA
article](https://aclweb.org/anthology/D15-1237), you will report your
answering triggering score for values of 1, 10, 100, and 1000.  This
means: given a query and a ranked list of items, you have a binary
classification decision to make for the first 1, then 10, then 100,
then 1000 items.  That decision is whether you think there does exist
a correct answer in that set of items.  This binary decision is the
sort your system would want to make in deciding whether to return a
set of results to a user, or how many results: you may have a list of
1,000 items in your reranker, but decide that, e.g., only 27 of them
are remotely likely to contain the right answer, so then you might in
a product decide to give the user just 27 results, rather than the
full 1,000 you started with and reranked.

Similarly to initial training of a classifier, you may make use of
train and dev, and only run on test for the final evaluation.

Suggested approach: create extra dev data out of your training set.
When you have a fit model trained as you already know how to do, then
use this special held-out dev data for fitting a scalar threshold on
your model output score that maximizes F1.  This just means, if your
model outputs a score between 0.0 and 1.0 (say if using logistic
regression) then for each ranked list of items, remove anything that
is below some threshold score T, compute F1.  Try different values of
T, create a plot with T on the x-axis, F1 on the Y axis, take the
value of T that gives the highest value of F1.  This is an example of
what commonly referred to as "trading off precision and recall".

Computing the score
-------------------

To compute this score, you iterate through the rank list similarly to
when computing success @k.  But here you will have some model that
looks at the returned elements, and makes that binary classification
decision "this set does/does not have any correct answers in it".

The numbers to report here are [Precision, Recall and
F1](https://machinelearningmastery.com/classification-accuracy-is-not-enough-more-performance-measures-you-can-use/),
at each value of 1, 10, 100, and 1000.  For example, if you have N
queries, leading to N rank lists, then for each list of the first 10
you will ask: "does this have a right answer?", you will know whether
you got that question right or not, since you will check the lists
with your answer key.

You are authorized to make use of the eval.py script associated with
the WikiQA project for computing answer triggering scores.  You can
find that by downloading the WikiQA bundle from Microsoft, then
reading their sparse README.  The eval script is not commented, and
assumes you are working with the original WikiQA data files, but some
may fine it a useful reference.
