## Extra Negative Data

In the paper: [Automatically Extracting High-Quality Negative Examples
for Answer Selection in Question
Answering](https://dl.acm.org/citation.cfm?id=3080645&CFID=1008380102&CFTOKEN=30185839),
the authors propose a simple strategy for extracting extra negative
examples for training a question answer selection system.  Relevant
here: they provide their data which should supplement the TREC data
discussed in another idea for the project; also, this technique
presumably could be replicated on the Wikipedia documents.  Why
restrict yourself to the negative data just gotten from WikiQA itself?
We did the work to align that data to the original Wikipedia page, why
not use other sentences from the same document to help train your
ranker?

Does this improve your results?  Does this improve your results as
compared to taking a the same number of sentences but chosen randomly
from other documents?
