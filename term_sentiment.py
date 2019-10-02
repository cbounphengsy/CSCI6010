import sys
import json
import codecs
import re
import string

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def dictionary():
    afinnfile = open(sys.argv[1])
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores

def createPython():
    jsonObject = createJSON()
    pythonObject = json.dumps(jsonObject)
    return pythonObject


def createJSON():
    #Encode file into utf-16 to properly read since there was spacing in-between characters
    jsonFile = codecs.open(sys.argv[2], "r", "utf-16")
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
    
def wordValue(word, scores):
    word = str(word.encode("utf-8"))
    value = 0
    for item in scores:
        term = item 
        if (word.find(term) >= 0):
            value += int(scores[item])
    return value

def tweetValue(scores, currentTweet):
    i = 0
    currentScore = 0
    j = 0
    while j < len(currentTweet):
        currentWord = currentTweet[i]
        currentScore += wordValue(currentWord, scores)
        j += 1
        i += 1
    #print currentTweet
    #print currentWord
    ##print dictionary()
    return currentScore

def assignWord(word, prev, nxt, scores, currentTweet):
    word = str(word.encode("utf-8"))
    prev = str(prev.encode("utf-8"))
    nxt = str(nxt.encode("utf-8"))
    wordValue = 0
    prevValue = 0
    nxtValue = 0
    prevCount = 0 
    nxtCount = 0
    stringValue = 0
    for item in scores:
        term = item 
        if (word.find(term) >= 0):
            value = int(scores[item])
        else:
            if prev == "noPrev":
                prevValue = 0
            elif (prev.find(term) >= 0):
                prevValue = float(scores[item])
                prevCount = 1
            else:
                prevCount = 1
                prevValue = 0

            if nxt == "noNext":
                nextValue = 0
            elif (nxt.find(term) >= 0):
                nxtValue = float(scores[item])
                nxtCount = 1
            else:
                nxtCount = 1
                nxtValue = 0
        
        wordValue = (prevValue + nxtValue) / float(prevCount + nxtCount)
        if wordValue == 0:
            stringValue = tweetValue(scores, currentTweet)
            if stringValue >= 0:
                return 1
            elif stringValue < 0:
                return -1
        else:
            return wordValue

def assignValue(scores, tweets):
    j = 0
    k = 0
    termValues = {}
    wordValue = 0
    prev = ""
    nxt = ""
    while j < len(tweets):
        currentTweet = tweets[j]
        words = parseTweet(currentTweet)
        for item in words:
            if j > 0:
                k = j - 1
                prev = tweets[k]
            else:
                prev = "noPrev"
            if j < len(tweets) - 1:
                k = j + 1
                nxt = tweets[k]
            else:
                 nxt = "noNext"
            if tweetFilter(item) == 0:
                wordValue = assignWord(item, prev, nxt, scores, currentTweet)
                term = {item: wordValue}
                termValues.update(term)
        j += 1

    return termValues

#Filter against usernames, links, and special characters
def tweetFilter(word):
    word = str(word.encode("utf-8"))
    if (special(word) == 1):
        return 1
    elif word.find("@") >= 0:
        return 1
    else:
        return 0

def special(word):
    if re.match("^[a-zA-Z0-9_]*$", word):
        return 0
    else:
        return 1

def outputTermSentiment():
    scores = dictionary()
    tweets = getTweets()
    termValues = assignValue(scores, tweets)
    for item in termValues:
        print str(item.encode("utf-8")), termValues[item]
    

def main():
    #sent_file = open(sys.argv[1])
    #tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    outputTermSentiment()

if __name__ == '__main__':
    main()

