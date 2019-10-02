import sys
import json
import codecs

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

def sentiment(tweets, scores):
    sentimentValue = 0
    i = 0
    while i < len(tweets):   
        currentTweet = parseTweet(getTweets()[i])
        sentimentValue = tweetValue(scores, currentTweet)
        i += 1
        #print ("Tweet #" + str(i) + " Sentiment Value: " + str(sentimentValue))
        print str(sentimentValue)

def outputTweetSentiment():
    scores = dictionary()
    tweets = getTweets()
    sentiment(tweets, scores)

def main():
    #sent_file = open(sys.argv[1])
    #tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    outputTweetSentiment()
    

if __name__ == '__main__':
    main()
