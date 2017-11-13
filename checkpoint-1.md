## Checkpoint 1: Baseline search service

Due November 16 at 3 pm.

In HW1 you were provided with stub code for setting up a search
service.  You should make use of that and your solutions to HW1 to
assist in this checkpoint: you may copy in any code the instructors
provided from the assignments, as well as any solutions from members
of your team.

Your goal is to build a new search service in its own container,
similarly to HW1, and then to modify the docker-compose file to
integrate your container into the system.  The UI in checkpoint 0
connects to the Lucene search service as well as the fetch service.
When a search is entered in the UI, the search query is sent to the
Lucene search service, the search results are received from Lucene, and
those results---the *Communication IDs* of the top documents matching
the query---are then sent to the fetch service to retrieve the *text*
of each Communication (and return it to the user next to the
Communication ID.)

Change this setup so that the UI connects to your search service, your
search service receives the query, then itself calls the Lucene service
with the same query, receives the search results from Lucene, and then
returns those search results unmodified to the UI.  (The UI will then
use the fetch service to get the Communication text for each
Communication ID, as before.)

In this checkpoint we are ensuring you can stand up a module inside the
pipeline that is a "pass-through:" your code is inserted into the
system and executed for each search query, but the user-visible
behavior of the system is unchanged.  This will be the stable baseline
you will attempt to improve upon later in the project.

After inserting your pass-through search service in the pipeline,
create an Issue and attach a screenshot of the results of the same
query from checkpoint 0, this time executed on the internally modified
system.  Also in that Issue you should
[reference a
commit](https://help.github.com/articles/autolinked-references-and-urls/)
in your project that corresponds to the code you ran to produce that
screenshot.  An instructor should be able to check out your project at
that commit, stand up the system using the same commands listed in the
original `simple-search-demo` README, enter the query into the UI, and
get the same results (using an EC2 instance like yours, with just
Docker and Docker Compose installed.)
