## Checkpoint 1: Baseline search service

Due November 16 at 3 pm.

In HW1 you were provided with stub code for setting up a search
service.  You should make use of that and your solutions to HW1 to
assist in this checkpoint: you may copy in any code the instructors
provided from the assignments, as well as any solutions from members
of your team.

Your goal is to build a new search service in its own container,
similarly to HQ1, and to modify your docker-compose file from the
first checkpoint to integrate your container into the system.  The UI
in checkpoint 0 connects to the Lucene search service.  You need to
change this so the UI connects to your search service, your search
service receives the query, then itself calls the Lucene service with
the same query.  In this checkpoint your search service gets the
results back from Lucene and returns to them to the user with no
modification.  This step is ensuring you can stand up a module inside
the pipeline that is a "pass through": it doesn't do anything but
successfully not break the existing system.  This will then be the
stable baseline you will attempt to improve upon.

Similar to checkpoint 0, create an Issue, attach a screenshot
resulting from the same query.  Also in that Issue you should
[reference a
commit](https://help.github.com/articles/autolinked-references-and-urls/)
in your project that corresponds to what you ran to get that
screenshot.  Any instructor should be able to pull your project based
on that commit, stand up the system based on the checked in compose
file, and get the same result from the same query.