def func(strs: list):
    result = ""
    for char in range(len(min(strs, key=len))):
        comparisonCharsList = []
        for word in range(len(strs)):
            comparisonCharsList += strs[word][char]
        if comparisonCharsList.count(comparisonCharsList[0]) == len(comparisonCharsList):
            result += comparisonCharsList[0]
        else:
            return result
    return result
