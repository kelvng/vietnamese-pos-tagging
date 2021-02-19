# coding=utf-8

import string
import numpy
import sklearn.svm as svm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
import io
from collections import defaultdict
import random

tagsetDict = {"Np" : 0,
              "Nc" : 1,
              "Nu" : 2,
              "N" : 3,
              "V" : 4,
              "A" : 5,
              "P" : 6,
              "R" : 7,
              "L" : 8,
              "M" : 9,
              "E" : 10,
              "C" : 11,
              "CC" : 12,
              "I" : 13,
              "T" : 14,
              "Y" : 15,
              "Z" : 16,
              "X" : 17 }
inverseTagsetDict = {tagsetDict[k]:k for k in tagsetDict}

wordBank = defaultdict()
bigramBank = defaultdict()
bigramDict = defaultdict(int)

bigramFreq = {x:[0]*18 for x in tagsetDict}
mostCommonBigrams = defaultdict()

prevParts = None

f_tagged = io.open("corpus/VNTQcorpus-small.tagged.txt", encoding='utf-8').readlines()
# f = io.open("corpus/VNTQcorpus-small.txt", encoding='utf-8').readlines()

# Separate train and test set
# train = f_tagged[:int(len(f)/2)]
# test = f_tagged[int(len(f)/2):]
train = f_tagged[:15000]
test = f_tagged[15000:30000]

# Get training data
for line in train:
    l_split = line.split()
    for i,w in enumerate(l_split):
        parts = w.split("/")
        if i >= 1:
            prevParts = l_split[i-1].split("/")
        if len(parts) == 1 or \
            parts[1] not in tagsetDict:
            continue

        # if prev parts is a punctuation get the one before that
        if i >= 2 and prevParts[1] in string.punctuation:
            prevParts = l_split[i-2].split("/")

        word = parts[0]
        pos = parts[1]

        if i >= 1:
            prevWord = prevParts[0]
            prevPos = prevParts[1]
            bigramBank[ word ] = (pos, prevWord, prevPos)
            bigramDict[ (pos, prevPos) ] += 1
            #calculate pos after pos
            #bigramFreq[prevPos][tagsetDict[pos]] += 1

        # Makes word map to list of pos tags
        if word not in wordBank:
            wordBank[word] = [pos]
        else:
            wordBank[word] += [pos]

for k in bigramFreq:
    maxFreq = 0
    maxPos = "Np"
    for i,x in enumerate(bigramFreq[k]):
        if x > maxFreq:
            maxFreq = x
            maxPos = inverseTagsetDict[i]
    mostCommonBigrams[k] = maxPos


print ("finished getting training data")


#####################################################################
# Features
def feature(word,wordIdx, lineSize, line):
    feat = [1]

    # print("word is : " + str(word))
    # print("wordIdx is : " + str(wordIdx))
    # print("linesize is : "  + str(lineSize))

    # how far word is into sentence
    sentPercent = float(wordIdx)/float(lineSize)
    feat.append(sentPercent)

    # 0.8516463095298431

    if word[0].isupper() and wordIdx != 0:
        feat.append(1)
    else:
        feat.append(0)

    # label pos tags for each word
    posIdx_array = ([0] * len(tagsetDict))
    posSet = []
    if word in wordBank:
        posSet = wordBank[word]
    else:
        # see word we don't know
        if wordIdx == 0:
            posSet = list(tagsetDict.keys())[0] # Naive: always choose Np for word we havent seen
            posIdx_array[tagsetDict[posSet]] = 1
            return feat + posIdx_array + [0]
        else:
            prevWord = line[wordIdx-1]  #TODO this is questionable
            if prevWord in wordBank:
                prevPos = wordBank[prevWord]
                maxPos = mostCommonBigrams[prevPos]
                if prevPos == "E":
                    maxPos = 3
                posIdx_array[tagsetDict[maxPos]] = 1
                feat += posIdx_array + [tagsetDict[maxPos]]
                return feat
            else:
                posSet = list(tagsetDict.keys())[0]  # Naive: always choose Np for word we havent seen
                posIdx_array[tagsetDict[posSet]] = 1
                feat += posIdx_array + [0]
                return feat

    for pos in posSet:
        posIdx = tagsetDict[pos]
        posIdx_array[posIdx] += 1.0/len(wordBank[word])
    feat += (posIdx_array) + [0]

    # Don't put features here!

    return feat
#####################################################################


# Create y (list of pos tags) and x (feature) data
y = []
X_train = []
for line in train:
    l_split = line.split()
    for i,w in enumerate(l_split):
        parts = w.split("/")
        word = parts[0]
        len_line = len(l_split)

        if len(parts) == 1 or parts[1] not in tagsetDict:
            continue
        y.append(wordBank[word][0]) # [0] for first word tagged pos
        X_train.append(feature(word,i,len_line, l_split))

print ("finished creating y and xtrain")

print ( len(X_train) )
print ( len(y) )

print(X_train[0:10])
train_fit = OneVsRestClassifier(LinearSVC(random_state=0)).fit(X_train,y)

print ("finished fitting")

X_test = []
correct_results = []
# Get testing data
for line in test:
    l_split = line.split()
    for i,w in enumerate(l_split):
        len_line = len(l_split)
        parts = w.split("/")
        if len(parts) == 1 or parts[1] not in tagsetDict:
            continue
        word = parts[0]
        pos = parts[1]
        if word in string.punctuation or word == ":.":
            continue
        X_test.append(feature(word,i,len_line,l_split))
        correct_results.append(pos)

print("finished getting testing data")

predicted_results = train_fit.predict(X_test)
print(predicted_results[:10])
print(correct_results[:10])

numCorrect = 0
for cor,pred in zip(correct_results, predicted_results):
    if cor == pred:
        numCorrect += 1

accuracy = 1.0*numCorrect/len(correct_results)
print(accuracy)