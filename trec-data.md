## TREC QA

(TREC QA
data)[http://cs.jhu.edu/~xuchen/packages/jacana-qa-naacl2013-data-results.tar.bz2]
: This contains questions, answer sentences, and in every positive
answer sentence, the last two lines gives the answer string and the
token indices to the correct answer.

This TREC data could be used in various ways:

* Additional data to supplement your question/sentence WikiQA classifier

* First train a question/sentence classifier only on the TREC data,
  then when training a WikiQA model, add one new feature to your
  model: the prediction of your TREC-based model.  By doing this
  "stacked" version of the classifier, you allow your WikiQA model to
  learn how much to trust the TREC model.  It could be that the TREC
  questions and answers are not similar enough to the WikiQA data to
  be that beneficial, and so then your WikiQA model would learn to
  ignore the predictions of that model.  Or it could be they are very
  related, and so the WikiQA model would learn to trust the TREC model
  significantly, putting a high weight on that "feature"

* The TREC data answer patterns: you might consider running a version
  of your query generator against Wikipedia where you use the TREC
  question and supplement it with the answer to that question.  You
  could take the resulting sentences from Wikipedia and treat those as
  correct sentences for the question.  You can then use that as
  additional data for improving your query generator and your question
  classifier.  This process would be noisy: it isn't guaranteed you'd
  find sentences that actually answer the question.  You could either
  simply train on noisy data, or you might consider running an MTurk
  HIT to validate whether these sentences do in fact answer the
  questions, just like you did in HW3.  If you'd like to run a HIT,
  ask the instructors.  NOTE: this will require the full Concretely
  Annotated Wikipedia, and then building an index for that.  The
  Lucene module you are using in this project has instructions on
  building a new index, so it is possible for you to build this
  yourself.  If sufficient interest exists for this effort, we might
  coordinate and build a single index and host it for everyone.

