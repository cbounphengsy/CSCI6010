import sys
import json
import codecs
import operator
from collections import Counter

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def createPython():
    jsonObject = createJSON()
    pythonObject = json.dumps(jsonObject)
    return pythonObject

def dictionary():
    afinnfile = open(sys.argv[1])
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores

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
    #f = open("tweetOutput.txt" ,"w")
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

def tweetValue(scores, words):
    i = 0
    currentScore = 0
    j = 0
    while j < len(words):
        currentWord = words[i]
        currentScore += wordValue(currentWord, scores)
        j += 1
        i += 1
    #print words
    #print currentWord
    ##print dictionary()
    return currentScore

def sentiment(tweet, scores):
    sentimentValue = 0
    words = parseTweet(tweet)
    sentimentValue = tweetValue(scores, words)
    return sentimentValue

def getPlaces():
    jsonObject = createJSON()
    locArray = []
    finalArray = {}
    #f = open("locOutput.txt" ,"w")
    #count = 0
    i = 0
    j = 0
    sentimentValue = 0
    oldcontent = jsonObject[i]['statuses'][0]
    while i < len(jsonObject):
        #count += 1
        content = jsonObject[i]['statuses'][0]
        if oldcontent == content:
            j +=1
            loc = jsonObject[i]['statuses'][j]['place']
            tweet = jsonObject[i]['statuses'][j]['text']
            sentimentValue = sentiment(tweet, dictionary())
            locArray.append(loc)
        else:
            j  = 0
            content = jsonObject[i]['statuses'][j]
            loc = jsonObject[i]['statuses'][j]['place']
            tweet = jsonObject[i]['statuses'][j]['text']
            sentimentValue = sentiment(tweet, dictionary())
            locArray.append(loc)
            oldcontent = jsonObject[i]['statuses'][0]
        #f.write("#" + str(count) + " : "+ str(loc)  + str(sentimentValue) + "\n\n")
        i += 1

    for subArray in locArray:
        if subArray != None:
            if subArray["country_code"] == "US":
                state = {subArray['full_name']: sentimentValue}
                finalArray.update(state)

    return finalArray

def getLocations():
    jsonObject = createJSON()
    locArray = []
    finalArray = {}
    i = 0
    j = 0
    sentimentValue = 0
    oldcontent = jsonObject[i]['statuses'][0]
    while i < len(jsonObject):
        content = jsonObject[i]['statuses'][0]
        if oldcontent == content:
            j +=1
            loc = jsonObject[i]['statuses'][j]['user']['location']
            tweet = jsonObject[i]['statuses'][j]['text']
            sentimentValue = sentiment(tweet, dictionary())
            locArray.append(loc)
        else:
            j  = 0
            content = jsonObject[i]['statuses'][j]
            loc = jsonObject[i]['statuses'][j]['user']['location']
            tweet = jsonObject[i]['statuses'][j]['text']
            sentimentValue = sentiment(tweet, dictionary())
            locArray.append(loc)
            oldcontent = jsonObject[i]['statuses'][0]
        i += 1

    for subArray in locArray:
        if subArray != "":
            state = {subArray: sentimentValue}
            finalArray.update(state)

    return finalArray

def avgArray(locArray):
    stateArray = []
    avgArray = {}
    for loc in locArray:
        stateArray.append(loc)
    stateArray = list(dict.fromkeys(stateArray))
    for state in stateArray:
        total = 0
        avg = 0
        num = 0
        for item in locArray:
            if state == item:
                total += locArray[item]
                num += 1
        avg = total/num
        avgState = {state: avg}
        avgArray.update(avgState)

    return avgArray

def outputState():
    locArray = getPlaces()
    locations = avgArray(locArray)
    newArray = getLocations()
    news = avgArray(newArray)
    finalArray = {}
    finalArray.update(locations)
    finalArray.update(news)
    #print locations
    top = dict(sorted(finalArray.iteritems(), key=operator.itemgetter(1), reverse=True)[:1])
    state = ""
    score = 0
    for item in top:
        score = top[item]
        for abbrev in states:
            if item.find(abbrev) >= 0:
                state = abbrev
    print state, score

def main():
    outputState()

if __name__ == '__main__':
    main()
