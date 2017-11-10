# KDFT Fall 2017, Final Project: Question Answer Retrieval

Your task is to construct a system that allows a user to type in a
natural language question as a search query, and be presented with
sentences from Wikipedia that may answer that question.  The
deliverables of this project will include a working system, a writeup that
includes performance numbers on how well you can classify sentences as
to whether they answer a given question, and a presentation plus demo
to the rest of the class on the day scheduled for the final exam.

This project is broken into multiple checkpoints.  These are meant to
help structure the project, and to encourage you to
break up lead responsibility for different parts of the project among
team members. Each checkpoint as they are revealed should be added to
your repository as a GitHub Issue, assigned to a member of your team
(hopefully different members for different Issues).  You are all
responsible for the project's success, but each Issue should have a
leader that is taking responsibility for the item being accomplished.
When submitting a checkpoint to Gradescope you will include a saved
pdf of the given Issue.  The pdf should be called:

```
issue-checkpoint-NUMBER.pdf
```

(For example, `issue-checkpoint-0.pdf` for the initial checkpoint.)

You are encouraged to organize your project by creating other Issues
as well, but please track the main deliverables of your effort with a
due date and title corresponding to these checkpoints.  You are
encouraged to make use of Issues to track key communications with your
team members, rather than by email.

Data will be provided under `data/`, with the essential
data set coming from WikiQA, the same set that you partially
annotated in HW3.  Additional data may be released in future
checkpoints.  You should train on train, tune based on dev, and
test on test.  Please refrain from using test until the end of the
semester.  Make use of dev as your test set until time to write the
final report.  Only when explicitly told through instructions that
it is appropriate to run on test, should you run on test.

## Checkpoints

* [Checkpoint 0: Running provided system](checkpoint-0.md)
* [Checkpoint 1: Creating baseline search service](checkpoint-1.md)