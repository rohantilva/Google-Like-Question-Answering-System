Simple Search Demo

This repo contains a `Dockerfile` for a simple web application for
querying a Concrete SearchService server.

The repo also contains a `docker-compose.yml` file for standing up:

  - the web based UI on port 8080
  - a FetchCommunicationService on port 9090
  - a Lucene-based SearchService on port 9091

The `docker-compose.yml` file assumes that you have a Zip archive in
the current directory named `comms.zip` that contains the
Concrete Communications you want to search. 

Building the Search Index
-------------------------

Before you can search through the Communications, you must first index
them using Lucene with the command:

    ./build-index.sh

This shell script simply runs `docker-compose` to build the index.
The indexing process can take a while.  On one relatively new laptop,
the process took roughly 10 minutes per GB of (uncompressed)
Communication files, but your mileage will vary.

The search index only needs to be built once per Document Corpus.
The index files are stored on a
[Docker volume](https://docs.docker.com/engine/admin/volumes/volumes/)
named `simplesearchdemo_index_volume`.
This Docker volume persists across container restarts.  Reindexing a
Corpus will add duplicate search results to the existing search index.


Deleting the Search Index
-------------------------

To remove the search index volume file, you will first need to remove
any containers that use the volume.  First, make certain that all
containers for this application are stopped using:

    docker-compose down
	docker-compose rm

You may also need to remove all stopped containers using:

    docker container prune

Once all containers using the volume have been removed, you can remove
the search index volume using:

	docker volume rm simplesearchdemo_index_volume


Standing up the Search Application
----------------------------------

Once the search index has been created, you can stand up the search
application using the command:

    docker-compose up

You should now be able to interact with the search application by
going to:

http://localhost:8080


Using the Concretely Annotated WikiQA Corpus
--------------------------------------------

A Docker image containing a FetchCommunicationService service bundled
with the "WikiQA Corpus" is available on Docker Hub:

  https://hub.docker.com/r/hltcoe/fetch-wikiqa-corpus/

The WikiQA corpus is a subset of
[Concretely Annotated Gigaword (CAW)](http://dx.doi.org/10.7281/T1/D06YVM).
A more detailed description of the corpus is available on the GitHub
page for the Docker image:

  https://github.com/hltcoe/fetch-wikiqa-corpus

If you would like to use the WikiQA corpus, please follow the
instructions in the [docker-compose.yml](docker-compose.yml) file
for editing the Docker image used for the 'fetch' service.

Please note that the `fetch-wikiqa-corpus` Docker image does not
include a pre-built search index.  You must still follow the
instructions in the 'Building the Search Index' section above.
=======
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

Additional data may be released in future checkpoints.

## Checkpoints

* [Checkpoint 0: Running provided system](checkpoint-0.md)
* [Checkpoint 1: Creating baseline search service](checkpoint-1.md)

## Removing the index

The
[README from simple-search-demo](https://github.com/hltcoe/simple-search-demo/blob/master/README.md)
contains instructions for removing Docker Compose and Docker state,
such as removing containers that have been created and removing the
index volume.  However, note your index volume will not be named
`simplesearchdemo_index_volume`, as that README suggests.  Run `docker
volume ls` to find the actual volume name.

## Docker Compose
## Checkpoint 0: Running provided system

Due November 13 at 3 pm.

Over the course of the project you will take a simple [existing search
system](https://github.com/hltcoe/simple-search-demo)
and extend its functionality.  That system
consists of multiple Docker containers including a prebuilt user
interface (UI), a fetch service atop articles from Wikipedia that
contain answer candidate sentences from WikiQA, and a basic Lucene
service that supports indexing communications.

For the first checkpoint you need to clone `simple-search-demo` and
follow [its
README](https://github.com/hltcoe/simple-search-demo/blob/master/README.md)
to run the search system.  (Note that you will need to modify the
`docker-compose.yml` file.)  Stand up the UI and type the query:

```
clarence clemons
```

You should see sentences returned back.

You should then copy the contents of that repository into your copy
of this repository and build off that for future
development (renaming that project's `README.md` to
`README-compose.md`).

Now redo the experiment: in your final project
repository that now has the `simple-search-demo` items in it, verify
you can then stand up the UI and submit the same query, getting the
same results.

Take a screenshot of these search results and attach them to the
Issue.  A PDF rendering of the Issue should be
submitted to Gradescope as proof that you have started the final
project and can run the basic system.  (Congratulations!)


### Docker Compose

Here we comment on new (to you) technology used in this checkpoint,
[Docker Compose](https://docs.docker.com/compose/overview/).

Docker Compose is one of the ways that Docker containers begin to be
especially useful.  A compose file allows you to start mixing and
matching components into larger workflows, on the assumption that the
individual components are containerized and working.  (In homework 1
we used a bash script, `run.bash`, to manage a network of Docker
containers: Docker Compose is a more robust way of doing this.)  In
this project, you have access to a UI, a fetch service, and a Lucene
index all pre-baked and assembled into a workflow.  In this checkpoint
you need to slightly modify the compose file to make use of the WikiQA
fetch service.  In the future you will add another container, your own
search service, as part of the larger workflow.

You will not be using them in this course, but be aware there is
experimental development within Docker for things called [stacks and
bundles](https://docs.docker.com/compose/bundles/).  We mention them
here only so you are aware that while currently there is Docker
Compose, in the future some related but different technology will
replace it.  However, the underlying concept of composing (or
"stacking" or "bundling") containers remains the same.
