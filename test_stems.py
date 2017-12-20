from query_utils import stem
from query_utils import return_search_results
 
sentence = "Who was the first president to get impeached?"

print(stem(sentence))
print(return_search_results(sentence))
