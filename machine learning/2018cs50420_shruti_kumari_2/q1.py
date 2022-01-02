import collections
import numpy as np
import json
import random
import math
import sys
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

traindata = []
testdata = []

def getTerms(review, stem, bigram):
    terms = []
    stemmedTerms = []
    review = review.lower()
    delimiters = [',','.','!',':',';',"''",'``','(',')']
    if not stem: 
        terms = word_tokenize(review)
    else: 
        porter = PorterStemmer()
        words = word_tokenize(review)
        stopwordsList = set(stopwords.words('english'))
        for word in words:
            if (word not in stopwordsList) and (word not in delimiters):
                terms.append(porter.stem(word))
                stemmedTerms.append(porter.stem(word))

    if bigram:
        singleTerms = stemmedTerms
        for i in range(len(singleTerms) - 1):
            terms.append(singleTerms[i] + ' ' + singleTerms[i+1])

    return terms

#training 
def train(trainfile, stem, bigram, top, idf, summary):
    Xtrain, ytrain, Xsummary = [],[],[]
    traindata = []
    with open(trainfile,'r') as trainf:
        for line in trainf:
            traindata.append(json.loads(line))

    for review in traindata:
        Xtrain.append(review['reviewText'])
        ytrain.append(review['overall'])
        Xsummary.append(review['summary'])

    terms = {}
    for i in range(len(Xtrain)):
        #print(i)
        review = getTerms(Xtrain[i], stem, bigram)
        for word in review:
            if word in terms:
                terms[word][ytrain[i]] += 1
            else:
                terms[word] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                terms[word][ytrain[i]] += 1
        if summary:
            review = getTerms(Xsummary[i], stem, bigram)
            for word in review:
                if word in terms:
                    terms[word][ytrain[i]] += 1
                else:
                    terms[word] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                    terms[word][ytrain[i]] += 3

    if top!=100:
        frequencies = {}
        for term in terms:
            frequencies[term]=sum([terms[term][category] for category in [1,2,3,4,5]])
        frequencies = sorted(frequencies.items(), key=lambda x: x[1])
        temp = terms
        limit = int(top*len(terms)/100)
        terms = {}
        i = 0
        for term in frequencies:
            if i > limit: break
            terms[term[0]] = temp[term[0]]
            i += 1
    
    nClass = [sum([terms[term][category] for term in terms]) for category in [1,2,3,4,5]]
    probWordCat = {}
    print("vocabulary: ", len(terms))
    for term in terms:
        probWordCat[term]={1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for category in [1,2,3,4,5]:
            tf = terms[term][category]
            if idf:
                tf = (terms[term][category] * 5)/sum([1 for cat in [1,2,3,4,5] if terms[term][cat]>0])
            probWordCat[term][category]=np.log((tf+1)/(nClass[category-1]+len(terms)))
            
    pClass = [np.log(len([Xtrain[i] for i in range(len(Xtrain)) if ytrain[i]==category])/len(Xtrain)) for category in [1,2,3,4,5]]
    
    return probWordCat, pClass

#testing 
def test(testfile, probWordCat, pClass, stem, bigram, summary):
    Xtest, ytest,Xsummary = [],[],[]
    testdata = []
    with open(testfile,'r') as testf:
        for line in testf:
            testdata.append(json.loads(line))

    for review in testdata:
        Xtest.append(review['reviewText'])
        ytest.append(review['overall'])
        Xsummary.append(review['summary'])

    results = {}
    for i in range(len(Xtest)):
        review = getTerms(Xtest[i], stem, bigram)
        if summary:
            summary = getTerms(Xsummary[i], stem, bigram)
            review = np.hstack([review,summary])
        predClass, maxProb = 0, -math.inf
        for j in range(1,6):
            probs = [probWordCat[word][j] if word in probWordCat else 0 for word in review] 
            prob = pClass[j-1]+np.sum(probs)
            if prob>maxProb:
                maxProb = prob
                predClass = j
        results[Xtest[i]] = {'prediction': predClass, 'original': ytest[i]}
        
    return results

def randomPred(testfile):
    Xtrain, Xtest, ytrain, ytest = [],[],[],[]
    testdata = []
    with open(testfile,'r') as testf:
        for line in testf:
            testdata.append(json.loads(line))

    for review in testdata:
        Xtest.append(review['reviewText'])
        ytest.append(review['overall'])

    results = {}
    for i in range(len(Xtest)):
        results[Xtest[i]] = {'prediction': random.randint(1,5), 'original': ytest[i]}
        
    print('Accuracy on test data (random prediction): ', accuracy(results))

def majorPred(trainfile, testfile):
    Xtrain, Xtest, ytrain, ytest = [],[],[],[]
    traindata = []
    with open(trainfile,'r') as trainf:
        for line in trainf:
            traindata.append(json.loads(line))

    for review in traindata:
        ytrain.append(review['overall'])
        
    predictions = collections.Counter(ytrain)
    mostProbPred = max(predictions, key=predictions.get)
    
    testdata = []
    with open(testfile,'r') as testf:
        for line in testf:
            testdata.append(json.loads(line))

    for review in testdata:
        Xtest.append(review['reviewText'])
        ytest.append(review['overall'])

    results = {}
    for i in range(len(Xtest)):
        results[Xtest[i]] = {'prediction': mostProbPred, 'original': ytest[i]}
        
    print('Accuracy on test data (major prediction): ', accuracy(results))

def accuracy(results):
    return len([1 for term in results if results[term]['prediction']==results[term]['original']])/len(results)

def getF1score(confMat):
    fscores = {}
    for i in range(5):
        tp = confMat[i,i]
        fp = sum([confMat[j][i] for j in range(5)])-confMat[i,i]
        fn = sum([confMat[i][j] for j in range(5)])-confMat[i,i]
        fscores[i+1]=tp/(tp+(fp+fn)/2)
    #print(fscores, sum(fscores.values())/5)
    return sum(fscores.values())/5

def part1(trainfile, testfile):
    probWordCat, pClass = train(trainfile, False, False, 100, False, False)
    resultsTrain = test(trainfile, probWordCat, pClass, False, False, False)
    print('Accuracy on training data: ', accuracy(resultsTrain))
    results = test(testfile, probWordCat, pClass, False, False, False)
    print('Accuracy on test data: ', accuracy(results))
    confMat = np.zeros((5,5))
    for result in results:
        i = int(results[result]['original']) - 1
        j = results[result]['prediction'] - 1
        confMat[i][j] += 1
    print(getF1score(confMat))
    return results

def part2(trainfile, testfile):
    randomPred(testfile)
    majorPred(trainfile, testfile)

def part3(trainfile, testfile, part):
    if part==1: results = part1(trainfile, testfile)
    if part==4: results = part4(trainfile, testfile)
    if part==51: results = bigram(trainfile, testfile)
    if part==52: results = idf(trainfile, testfile)
    if part==53: results = removeRedundance(trainfile, testfile,10)
    confMat = np.zeros((5,5))
    for result in results:
        i = int(results[result]['original']) - 1
        j = results[result]['prediction'] - 1
        confMat[i][j] += 1
    print(confMat)
    return confMat

def part4(trainfile, testfile):
    probWordCat, pClass = train(trainfile, True, False, 100, False, False)
    resultsTrain = test(trainfile, probWordCat, pClass, True, False, False)
    print('Accuracy on training data with stemming: ', accuracy(resultsTrain))
    results = test(testfile, probWordCat, pClass, True, False, False)
    print('Accuracy on test data with stemming: ', accuracy(results))
    confMat = np.zeros((5,5))
    for result in results:
        i = int(results[result]['original']) - 1
        j = results[result]['prediction'] - 1
        confMat[i][j] += 1
    print(getF1score(confMat))
    return results

def bigram(trainfile, testfile):
    probWordCat, pClass = train(trainfile, True, True, 100, False, False)
    results = test(testfile, probWordCat, pClass, True, True, False)
    print('Accuracy on test data with stemming (bigram): ', accuracy(results))
    confMat = np.zeros((5,5))
    for result in results:
        i = int(results[result]['original']) - 1
        j = results[result]['prediction'] - 1
        confMat[i][j] += 1
    print(getF1score(confMat))
    return results

def idf(trainfile, testfile):
    probWordCat, pClass = train(trainfile, True, True, 100, True, False)
    results = test(testfile, probWordCat, pClass, True, True, False)
    print('Accuracy on test data with stemming (bigram+idf): ', accuracy(results))
    confMat = np.zeros((5,5))
    for result in results:
        i = int(results[result]['original']) - 1
        j = results[result]['prediction'] - 1
        confMat[i][j] += 1
    print(getF1score(confMat))
    return results

def removeRedundance(trainfile, testfile, top):
    probWordCat, pClass = train(trainfile, True, False, top, False, False)
    resultsstemming = test(testfile, probWordCat, pClass, True, False, False)
    print('Accuracy on test data with stemming (non-redundant): ', accuracy(resultsstemming))
    confMat = np.zeros((5,5))
    for result in resultsstemming:
        i = int(resultsstemming[result]['original']) - 1
        j = resultsstemming[result]['prediction'] - 1
        confMat[i][j] += 1
    print(getF1score(confMat))

def part5(trainfile, testfile, top):
    bigram(trainfile, testfile)
    idf(trainfile, testfile)
    removeRedundance(trainfile, testfile, top)

def part6(trainfile, testfile, part):
    confMat = part3(trainfile, testfile, part)
    print(getF1score(confMat))

def part7(trainfile, testfile):
    probWordCat, pClass = train(trainfile, False, False, 100, False, True)
    resultsTrain = test(trainfile, probWordCat, pClass, False, False, True)
    print('Accuracy on training data: ', accuracy(resultsTrain))
    results = test(testfile, probWordCat, pClass, False, False, True)
    print('Accuracy on test data: ', accuracy(results))
    confMat = np.zeros((5,5))
    for result in results:
        i = int(results[result]['original']) - 1
        j = results[result]['prediction'] - 1
        confMat[i][j] += 1
    print(getF1score(confMat))
    return results

trainfile = 'reviews_Digital_Music_5/Music_Review_train.json'
testfile = 'reviews_Digital_Music_5/Music_Review_test.json'

def run(trainfile,testfile,qpart):
    if(qpart=='a'):
        part1(trainfile,testfile)
    elif(qpart=='b'):
        part2(trainfile, testfile)
    elif(qpart=='c'):
        part3(trainfile, testfile, 1)
    elif(qpart=='d'):
        part4(trainfile,testfile)
    elif(qpart=='e'):
        part5(trainfile, testfile, 10)
    elif(qpart=='f'):
        part6(trainfile, testfile, 51)
    elif(qpart=='g'):
        part7(trainfile, testfile)
    else:
        print('please provide correct part number')

run(sys.argv[1], sys.argv[2], sys.argv[3])
