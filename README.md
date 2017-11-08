# KDFT Fall 2017, Final Project: Question Answer Retrieval

Your task is to construct a system that allows a user to type in a
natural language question as a search query, and be presented with
resulting sentences from Wikipedia that may answer that question.  The
deliverables of this project will include a working system, a writeup that
includes performance numbers on how well you can classify sentences as
to whether they answer a given question, and a presentation plus demo
to the rest of the class on the day scheduled for the KDFT final exam.

This project is broken into multiple checkpoints.  These are meant to
help guide your structuring of the project, and to encourage you to
break up lead responsibility for different parts of the project among
team members. Each checkpoint as they are revealed should be added to
your repository as an Issue, assigned to a member of your team
(hopefully different members for different issues).  You are all
responsible for the project's success, but each issue should have a
leader that is taking responsibility for the item being accomplished.
When submitting a checkpoint to gradescope, please include a saved
.pdf of the given issue as part of the materials.  The pdf should be
called:

```
  issue-checkpoint-NUMBER.pdf
```

You are encouraged to organize your project by creating other issues
as well, but please track the main deliverables of your effort with a
due date and title corresponding to these checkpoints.  You are
encouraged to make use of issues to track key communications with your
team members, rather than by email.

Data will be provided in the data/ repository, with the essential
batch stemming from the WikiQA dataset, the same that you partially
annotated in HW3.  Additional data may be released in future
checkpoints.  You should train on train, development with dev, and
test on test.  Please refrain from using test until the end of the
semester.  Make use of dev as your test set until time to write the
final report; randomly sample however large an intial dev set as you'd
like from train.  Only when explicitly told through instructions that
it is appropriate to run on test, should you run on test.

## Checkpoint 0: Running provided system
## Due: 11/13

You will take an existing [simple search
demonstration](https://github.com/hltcoe/simple-search-demo) system
and extend it to include the functionality needed.  That system
consists of multiple Docker containers including a prebuilt user
interface (UI), a fetch service atop articles from Wikipedia that
contain answer candidate sentences from WikiQA, and a basic Lucene
service that supports indexing communications.

For the first checkpoint you need to first follow the README of that
project and run it (noting that you have to modify the docker-compose
file).  Stand up the UI and type the query:

```
clarence clemons
```

You should see sentences returned back.

You should then copy the contents of that repository into your version
of this final project repository and use that as the base for future
development.  (Renaming that project's README.md to README-compose.md)

Now redo the experiment: checkout a copy of your final project
repository that now has the simple-search-demo items in it, verify you
can then stand up the UI and submit the same query, getting the same
results.

Take a screenshot of the resulting search results.  This should be
submitted to gradescope as proof that you have started the final
project and can run the basic system.  Congratulations.


Docker Compose
--------------

Here we comment on new (to you) technology used in this checkpoint,
(Docker Compose)[https://docs.docker.com/compose/overview/].

Docker Compose is one of the ways that Docker containers begin to be
especially useful.  A compose file allows you to start mixing and
matching components into larger workflows, on the assumption that
individual systems are containerized and working.  In this final
project, you have access to a UI, a fetch service, and a Lucene system
all pre-baked and assembled into a workflow.  In this checkpoint you
need to lightly modify the compose file to make use of the WikiQA
fetch service.  In the future you will add another container, your own
search service, as part of the larger workflow.

You will not be using them in this course, but be aware there is
experimental development within Docker for things called (stacks and
bundles)[https://docs.docker.com/compose/bundles/].  We mention this
here only so you are aware that while currently there is Docker
Compose, in the future some related but different technology will
replace it.  Whether today or in the future, the underlying concept
remains that containers can be composed, or stacked, or bundled, into
larger systems.

