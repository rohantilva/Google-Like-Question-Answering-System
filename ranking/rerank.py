def rerank(dictUUID, results):
    for result in results.searchResultItems:
        if result.sentenceId.uuidString in dictUUID:
            result.score = dictUUID[result.sentenceId.uuidString]
    return results
