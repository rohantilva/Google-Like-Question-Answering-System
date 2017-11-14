# Indexing and Searching

In this assignment you will take a file of
[Concrete](http://hltcoe.github.io/concrete/)
[Communication](http://hltcoe.github.io/concrete/schema/communication.html#Struct_Communication)
objects, build a token-based index, and implement a simple search
interface over the Communications.

For this assignment you are not allowed to use external libraries, such
as Lucene.  There is some Lucene functionality in concrete-java:
do not use it or read its source code for this assignment.  The
concrete-python source code is also allowed.  One additional
third-party code example you are allowed to use or read is [this basic
inverted priority
queue](https://github.com/vandurme/jerboa/blob/master/src/main/java/edu/jhu/jerboa/util/KBest.java)
implemented in Java by Ben.

If you reference any other code in the context of this assignment, even
a glance (such as on StackExchange) then please cite those references
in your write-up by explaining what that reference provided you and
listing the location of the reference (such as a URL) and the
locations in your code where the reference was used.

## Given

- [x] A Dockerfile that implements the Concrete FetchCommunication
      service for a tarball or zip file of Communications
      ([Dockerfile.concrete_python](/Dockerfile.concrete_python), using
      the installed `fetch-server.py` script).
- [x] A Dockerfile for running querying Search services
      ([Dockerfile.search_client](/Dockerfile.search_client))
- [x] Stub Docker files for indexing and for boolean and weighted
      Search services
- [x] A stub Python implementation of a Search service
      ([search_stub.py](/search_stub.py)).
- [x] A stub Python unit test suite of the stub search service
      ([test_search_stub.py](/test_search_stub.py), runnable in Docker
      with
      [Dockerfile.test_search_stub](/Dockerfile.test_search_stub)).
- [x] An integration test suite that tests essential expected
      behavior of each component of your code
      ([integration_tests](/integration_tests))
- [x] A convenience script that runs a FetchCommunication service on
      a specified tarball or zip file of Communications, runs your
      indexer on that service, runs your Search services against
      the generated index, and executes sample queries against those
      Search services ([run.bash](/run.bash))
- [x] A small toy data set of a few Concrete Communications
      ([wikipedia_test.zip](/wikipedia_test.zip))
- [x] A larger data set of about eight hundred Concrete Communications
      (`/home/tom/cs365/data/wikipedia.zip` on the undergrad network)
- [x] Information retrieval reference for use in constructing the index
      and performing the different modes of search
      ([IR Book](https://nlp.stanford.edu/IR-book/#anchor01) chapters
      one and six).

## Required

- [ ] A [solution.md](/solution.md) file with a clear and concise
      write-up of your solution including acknowledgment of any
      resources (such as StackExchange posts) that you used.
- [ ] A Dockerfile that performs token-based indexing of a tarball or
      zip file of Communications
      ([Dockerfile.index](/Dockerfile.index))
- [ ] A Dockerfile that implements a boolean Concrete Search service on
      top of an index from step 1
      ([Dockerfile.boolean_search](/Dockerfile.boolean_search))
- [ ] A Dockerfile that implements a weighted Concrete Search service
      on top of an index from step 1
      ([Dockerfile.weighted_search](/Dockerfile.weighted_search))

### Detailed requirements

When building the index, use the existing tokenizations in the
Communications and lower-case the text: A Communication's terms should
be formed from the values of the `text` fields of all `Token` objects
in that Communication's tokenizations, lower-cased.  Filter the top 250
terms (by frequency) out of the dictionary when creating the index, but
print the top 50 of those 250 terms to the file
`/mnt/index/top-terms.txt`, one term per line, decreasing by frequency.

In addition to writing the top 50 filtered-out terms, the indexer
should write an index file to `/mnt/index/index.gz`
containing the TF and IDF weights of all but the top 250 terms.  The TF
and IDF weights should be computed using the standard formula as
described in chapter six of the IR Book.  The index file should be
gzipped and have the following format:

```
commID1	commID2	commID3	...
term1	IDF1	index1_1:TF1_1	index1_2:TF1_2	...
term2	IDF2	index2_1:TF2_1	index2_2:TF2_2	...
...
```

For example:

```
Benjamin_Franklin	George_Washington	Martha_Washington	...
dog	0.031	0:3	1:2	...
electricity	0.005	0:15	...
...
```

The first line is a list of the communication IDs of the communications
you have indexed, separated by tabs.  Each of the subsequent lines
contains a term, the IDF value of that term, and then a list of pairs,
all separated by tabs.  Each pair consists of the integer position of
a communication in the first line (using zero-based indexing) and the
frequency of the current line's term in that communication.  Omit pairs
with frequency zero.  The pairs in each line should be sorted according
to the first item in the pair (increasing).

In the above example, the word "dog" has an IDF value of 0.031
and it appears three times in the communication "Benjamin_Franklin" and
two times in the communication "George_Washington".  The word
"electricity" has an IDF value of 0.005 and appears fifteen times in
the communication "Benjamin_Franklin".

You should implement the following two forms of Search for queries
consisting of one or more terms.

* *boolean* (conjunction): Return all documents satisfying the query,
  up to a maximum of `k` documents.  See figures 1.6 and 1.7 in chapter
  one of the IR book.  Queries containing more than one term should be
  interpreted as conjunctions.  For example, for query "dog bark" only
  return documents that contain both "dog" and "bark".
* *weighted*: Return the top `k` documents according to overlap score,
  using TF-IDF weights.  Note that returned documents do not need to
  contain all terms of the query.

In both forms of search your implementations should satisfy the
following criteria.

* A query's terms should be accessed from `SearchQuery.terms` (each
  item in the list is a separate term).
* As many hits as match the query (for weighted search, all documents
  "match the query" in this sense) should be returned, *up to* the
  value of `SearchQuery.k`.
* Search terms not in the vocabulary should be ignored.

Sorting behavior in the case of ties (two documents that both contain
all query terms or two documents with the same overlap score) is left
unspecified; it can be whatever you think is appropriate.

The indexer and both search implementations should satisfy the
following additional criteria.

* Unicode should be handled correctly.  Your indexer output should be
  encoded in UTF-8.  (The indexer input and search implementation
  input/output are decoded from/encoded to UTF-8 automatically by your
  Concrete library.)
* Your code should scale to the larger (approximately 750-document)
  Wikipedia data set at `/home/tom/cs365/data/wikipedia.zip` on
  the undergrad network.  (On an EC2 c4.large instance, indexing should
  complete in under ten minutes and a search on 40k two-term queries
  should complete in under one minute; we find there is little
  difference in performance between a c4.large instance and a t2.medium
  instance in this context.)

Part of your grade will come from the readability of your code.
Specifically, we define readability as informative comments and
interpretable variable and function names, as well as a clear and
concise explanation of your solution in [solution.md](/solution.md).
Additionally, the automated style checks must pass.

Finally, you will earn bonus points for submitting tests for one or
more requirements described previously that are *not* tested in the
provided integration test suite and explaining how to run your tests in
your write-up.  (You will only earn bonus points for tests that pass.)
You may submit *unit tests* that run inside a Docker container and/or
*integration tests* that run Docker containers themselves.  Whereas
unit tests allow you to concisely and thoroughly verify the behavior of
individual functions and classes, integration tests allow you to
coarsely assert that nothing breaks when all of the pieces are put
together.  (Good software includes both unit and integration tests!)

If you submit unit tests, you may use any Python testing framework you
wish; your write-up must include instructions for us to run those tests
with a single Docker run command.  We provide stub unit tests for
[pytest](https://docs.pytest.org/en/latest/getting-started.html)
([test_search_stub.py](/test_search_stub.py)) to help get you started.
(The Dockerfile
[Dockerfile.test_search_stub](/Dockerfile.test_search_stub) illustrates
how to run these tests.)

If you submit integration tests, you must use pytest; we suggest you
build upon the provided integration test suite (you are free to modify
it however you wish).  The provided suite runs on Python 3.5 with
concrete-python 4.13.3 and pytest 3.2.1; your tests must run on those
versions as well.  Note that the integration tests should only interact
with your code via Docker.

### Grading

Your grade for this assignment will be composed approximately as
follows.

* 70%: Correctness
* 20%: Readability
* 10%: Speed

### Testing your solution

#### Style checks

We expect your code is style-checked with
[flake8](http://flake8.pycqa.org/en/latest/), which tests compliance
with the
[PEP8](https://www.python.org/dev/peps/pep-0008/) style guide (and can
also find bugs).  Install flake8 with `pip install flake8` or
`pip install --user flake8` and run it as:

```
flake8
```

The style checks are configured in the [.flake8](/.flake8)
configuration file in this directory; your code is expected to pass
flake8 checks with the provided configuration file.

You may run the `autopep8` tool to automatically fix a subset of the
issues reported by flake8.  Install with `pip install autopep8` or
`pip install --user autopep8` and run it as

```
autopep8 -draa .
```

to print the diff of all suggested changes of files in the current
directory, using an "aggressive" level of two (corresponding to the two
`-a` flags; use one or zero `-a` flags to reduce the number of
changes).  Then, to make the suggested changes, do:

```
autopep8 -iraa .
```

#### Correctness tests

The provided integration test suite will fail on a fresh clone of the
repository (the test suite uses pytest; if you do not have it, you can
install it with `pip install pytest` or `pip install --user pytest`):

```
pytest integration_tests
```

When you have finished the assignment all tests will pass.

Remember that finishing the assignment is a *sufficient* but not
*necessary* condition for all tests passing: as with any test suite,
the provided test suite may succeed even if there is a problem in your
implementation.

#### Speed tests

Once you are confident in the correctness of your code you can measure
how your code scales and try out your search algorithms on the small
[wikipedia_test.zip](/wikipedia_test.zip) data set or the larger
data set at `/home/tom/cs365/data/wikipedia.zip` on the undergrad
network.  For example:

```
./run.bash wikipedia.zip
```

This script writes index container output and the results of the
sample queries in [sample_queries.txt](/sample_queries.txt) to the
`output` directory; it does not perform any tests aside from asserting
that your implementation runs that workload without error.  On startup
the script removes Docker containers and volumes with the same names as
those used later in the script.

You are free to try out your code on the other large data sets in
`/home/tom/cs365/data` as well.

Docker is not currently available on the undergrad grid; to use the
larger data sets you will need to copy it to another system first.

Ensure any large data sets you use are either added to your
[.dockerignore](/.dockerignore) or stored outside your repository;
otherwise the data sets themselves will be added to the Docker build
context, increasing the run-time of the build substantially.

#### Automation

Style checks and integration tests are run automatically by
[Travis CI](https://travis-ci.com/), as specified in
[.travis.yml](/.travis.yml), whenever you push to GitHub.  You can see
the test result by going [travis-ci.com](https://travis-ci.com/) and
signing in with GitHub (using the green button in the upper-right
corner); after signing in, your Travis-enabled repositories will be
listed on the left along with their latest build results.
The build success or failure of a commit will also be listed on the
"commits" page of your GitHub repository: commits for which tests
passed will have a green check mark next to them while commits for
which tests failed will have a red "x" next to them.  You can click on
the check mark or x to see the output from the tests in Travis CI.
(Note that tests will be run once per push; if you make two commits to
master and then push master to GitHub, tests will only be run on the
second commit.)

You are free to modify the Travis CI build for your project
([.travis.yml](/.travis.yml)) however you wish; however, we ask that
you keep your build duration low (less than ten minutes per commit).
By default the provided integration tests are run under Python 3.5.

Note that we will need to manually enable Travis CI for your
repository when it is created.  We will try to do so as quickly as
possible.
