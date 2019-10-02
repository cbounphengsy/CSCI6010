import sys
import json
import codecs
import operator
from collections import Counter


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

def getHashtags():
    jsonObject = createJSON()
    hashtagArray = []
    finalArray = []
    #f = open("hashtagOutput.txt" ,"w")
    #count = 0
    i = 0
    j = 0
    oldcontent = jsonObject[i]['statuses'][0]
    while i < len(jsonObject):
        #count += 1
        content = jsonObject[i]['statuses'][0]
        if oldcontent == content:
            j +=1
            hashtags = jsonObject[i]['statuses'][j]['entities']['hashtags']
            hashtagArray.append(hashtags)
        else:
            j  = 0
            content = jsonObject[i]['statuses'][j]
            hashtags = jsonObject[i]['statuses'][j]['entities']['hashtags']
            hashtagArray.append(hashtags)
            oldcontent = jsonObject[i]['statuses'][0]
        #f.write("#" + str(count) + " : "+ str(hashtags) + "\n\n")
        i += 1

    for subArray in hashtagArray:
        for item in subArray:
            singleHashtag = item['text']
            finalArray.append(singleHashtag)

    return finalArray

def countHashtags(hashtags):
    return Counter(hashtags)

def outputTen():
    hashtags = getHashtags()
    count = countHashtags(hashtags)
    top = dict(sorted(count.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
    for item in top:
        print item, top[item]

def main():
    outputTen()
    

if __name__ == '__main__':
    main()
