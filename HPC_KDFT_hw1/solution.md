# Homework #1 Solutions and References:

## General Solution Notes:
For indexing and searching, I chose to use python dictionaries. In the past, when I've been doing any sort of data science in python, I've used
dictionaries - I've found them pretty handy and reasonably fast. Of particular use here was python's `sort` function, and also `OrderedDict`
from the `collections` module. The use of these two additional helpers aided me in ordering dictionaries based on term freqency in the case
of the `index_tokens.py` program, and in ordering outputs of the `weighted_search.py` program. 

I added 5 additional test cases, testing that only the specific value of k asked for returning in `boolean_search.py` and `weighted_search.py` were
returned by the programs. (It actually helped me catch an error in my weighted search where I wasn't checking k correctly! Yay!)

### Challenges Of Note:
I was unable to execute `./run.bash wikipedia.zip`, for a reason unknown to me. It's possible that it was just taking too long and I became impatient (running it on a t2.micro instance). However, `./run.bash wikipedia_test.zip` works rather quickly ~1mins, so I'm quite pleased with the result.

### References Used:
* Converting strings to lower case and making sure it's in unicode: https://stackoverflow.com/questions/6797984/how-to-convert-string-to-lowercase-in-python
* Concrete tutorial: http://concrete-python.readthedocs.io/en/latest/README.html#reading-concrete
* Sorting a dictionary by values: https://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
https://stackoverflow.com/questions/11753660/sorting-python-dictionary-based-on-nested-dictionary-values
* IDF calculation: https://nlp.stanford.edu/IR-book/pdf/06vect.pdf
* Creating files in new directories: https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
* Writing a gzip: https://docs.python.org/2/library/gzip.html
* I used the concrete documentation, api documentation, and Chandler's help liberally. (Thanks again, Chandler!)
* Elaine Wong provided a very helpful 40k 2-term query list
