import sys
import json
import codecs
import re
import string
from collections import Counter

def createPython():
    jsonObject = createJSON()
    pythonObject = json.dumps(jsonObject)
    return pythonObject


def createJSON():
    #Encode file into utf-16 to properly read since there was spacing in-between characters
    jsonFile = codecs.open(sys.argv[1], "r", "utf-16")
    fullJSON = []
    for line in jsonFile:
        currentJSON = json.loads(line)
        fullJSON.append(currentJSON)
    return fullJSON

def getTweets():
    jsonObject = createJSON()
    tweetArray = []
    #f = open("jsonOutput.txt" ,"w")
    i = 0
    j = 0
    #count = 0
    oldcontent = jsonObject[i]['statuses'][0]
    while i < len(jsonObject):
        #count += 1
        content = jsonObject[i]['statuses'][0]
        if oldcontent == content:
            j +=1
            tweet = jsonObject[i]['statuses'][j]['text']
            tweetArray.append(tweet)
        else:
            j  = 0
            content = jsonObject[i]['statuses'][j]
            tweet = jsonObject[i]['statuses'][j]['text']
            tweetArray.append(tweet)
            oldcontent = jsonObject[i]['statuses'][0]
        #f.write("#" + str(count) + " : "+ str(tweet.encode("utf-8")) + "\n\n")
        i +=1
    return tweetArray

def parseTweet(tweet):
    words = tweet.split()
    return words

def allWords(tweets):
    i = 0
    allWords = []
    while i < len(tweets):
        currentWords = parseTweet(getTweets()[i])
        for item in currentWords:
            allWords.append(item)
        i += 1
    return allWords

def distinct(array):
    distinct = [] 
    for item in array: 
        if item not in distinct: 
            distinct.append(item) 
    return distinct 

#Filter against usernames, links, numbers, and special characters
def tweetFilter(words):
    filteredWords = []
    for item in words:
        word = str(item.encode("utf-8"))
        if (special(word) == 1):
            words.remove(item)
        elif word.find("@") >= 0:
            words.remove(item)
        else:
            filteredWords.append(item)
    return filteredWords

def special(word):
    if re.match("^[a-zA-Z_]*$", word):
        return 0
    else:
        return 1

def countTerms(terms):
    return Counter(terms)

def outputFreq():
    termFreq = {}
    wordsArray = allWords(getTweets())
    filterArray = tweetFilter(wordsArray)
    totalFreq = 0
    for item in filterArray:
        totalFreq += 1
    count = countTerms(filterArray)
    for term in count:
        singleCount = float(count[term])
        newFreq = float(totalFreq)
        freqValue = singleCount/newFreq
        singleFreq ={term: freqValue}
        termFreq.update(singleFreq)
    for freq in termFreq:
        print str(freq), termFreq[freq]

def main():
    outputFreq()

if __name__ == '__main__':
    main()

