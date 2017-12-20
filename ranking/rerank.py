def rerank(self, dictUUID, results):
    for result in results.searchResultItems:
        if result.sentenceId in dictUUID:
            result.score = dictUUID[result.sentenceId]
    return results
