## Checkpoint 2: Search evaluation

In this checkpoint you will implement and run the evaluation code for
the search task you will demo in the final presentations.  In the
previous checkpoints you made use of the provided UI, here you will
make use of some code from HW1 for interacting with a search service
from the command line, to process a batch of queries and evaluate the
results.

### Success @k

Following [Chen and Van Durme,
2017](http://www.aclweb.org/anthology/E/E17/E17-2114.pdf) (which you
are encouraged to skim), we will evaluate a question answer retrieval
system using the success @k metric.  We will consider four different
values of k: 1, 10, 100, and 1000.  For a given value of k, success @k
is the fraction of queries in the evaluation set for which a correct
answer to the query appears in the top k results for that query.  For
example, for every query you managed to get a correct answer in the top
10 hits, success @10 would be 1.

You are responsible for writing an evaluation script that computes
success @k.  For each query, the title, section and sentence number,
and UUIDs of the correct answer(s) can be found in the provided data:

[data/WikiQA-match/](data/WikiQA-match)

You may wish to compare your results to Figure 3 of Chen and Van Durme
(2017) for a comparable set of values for this task, which shows
success @k for all values of k from 1 to 1000.  However, note that Chen
and Van Durme were concerned with all of Wikipedia, not just the subset
provided in the WikiQA fetch service; we should expect higher success
@k in this restricted subset.  (Why?)

Note that some questions in WikiQA do not have any correct answers.
You should skip those cases when computing success @k, we are only
concerned with the value of this measure for cases where there is a
known answer in the collection.  Which questions do not have correct
answers you can determine for yourself based on the data input file:
they are simply the questions with no associated candidates that were
labeled as correct.


### Baseline success @k

Submit to gradescope a .pdf of the Issue for this checkpoint.  The last
comment on the Issue should indicate the commit representing your code
for this checkpoint as well as a small text table of the following
format:

```
Baseline success @k
1: <value>
10: <value>
100: <value>
1000: <value>
```

These scores should be computed using the evaluation script you write
for this checkpoint and the baseline search system (with the
pass-through module) you developed for the previous checkpoint.
You should run the evaluation script on the **dev set** to compute
these scores.  The purpose here is to ensure you can query your system
from the command line---using queries from data/---and compute success
@k.  The files under data/WikiQA-match/ provide an alignment from
WikiQA to sentences in the communications, which you will need to
compute the results (which sentences from which communications answer
the given query you are submitting).
