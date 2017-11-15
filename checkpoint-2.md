## Checkpoint 2: Search evaluation

In this checkpoint you will implement and run the evaluation code for
the search task you will demo in the final presentations.  In the
previous checkpoints you made use of the provided UI, here you will
make use of the code in HW1 for interacting with a search service from
the command line, to batch a set of queries and evaluate their
results.

Success @k
==========

Following (Chen and Van Durme,
2017)[http://www.aclweb.org/anthology/E/E17/E17-2114.pdf] which you
are encouraged to skim, we will use success @k as one of the metrics.
This value reports for a given value of k: do the results 1...k
contain at least one positive result to the query?  We are concerned
with k = 1, 10, 100, 1000.  You are responsible for writing the
evaluation script that will compute these values.  For a given query
you know the title, section and sentence number, along with UUIDs, of
the one or more correct answer, as provided in:

  (data/WikiQA-match/)[data/WikiQA-match/]

Provided a ranked list of responses to that query (search results) you
iterate through the list, looking for the first case of a correct
answer, until you hit 1,000.  When you find the first correct answer,
you update counters for 1, 10, 100, 1000 that track how many correct
answers you have seen in the first 1, 10, 100, 1000 results, across
all queries.  When you have done this for all queries, you average the
values of each counter by the number of queries.  For example, if on
every query you managed to get a correct answer in the top-10 search
results, then the counter for 10 would be equal to the number of
queries.  When you average by the number of queries, the final value
for success @10 would be 1.0.  See Figure 3 of (Chen and Van Durme
2017) for a comparable set of values for this task, where that figure
computed success @k for all values of k from 1 to 1000.  (But note
that Chen and Van Durme were concerned with all of Wikipedia, not the
subset that is part of the WikiQA fetch service: one would expect
higher success scores using just the subset contained in this smaller
fetch service).

Note that some questions in WikiQA do not have correct answers.  You
should skip those cases when computing success @k, we are only
concerned with the value of this measure for cases where there is a
known answer in the collection.  Which questions do not have correct
answers you can determine for yourself based on the data input file:
they are simply the questions with no associated candidates that were
labeled as correct.


Baseline success @k
===================

Submit to gradescope an Issue .pdf with a reference to the commit that
enables this checkpoint.  That issue should have as the last comment the commit, and a small text table that says:

```
Baseline success @k
1: <value>
10: <value>
100: <value>
1000: <value>
```

You will get these values by submitting queries to your system
constructed in the previous checkpoint.  The queries will be the
questions from the dev set.  The purpose here is to ensure you can
query your system from the command line, using queries from data/, and
that you can compute success @ k.  The files stored in
data/WikiQA-match/ provides an alignment from WikiQA to sentences in
the communications, which you will need for computing the results
(which sentences from which communications answer the given query you
are submitting).