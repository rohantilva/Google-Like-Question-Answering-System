# Checkpoint 0: Running provided system

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
