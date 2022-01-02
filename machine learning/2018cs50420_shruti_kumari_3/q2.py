import collections
import numpy as np
import json
import random
import math
import sys
import math
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from time import time

#filename = 'poker/poker-hand-testing.data'
def encode(filename):
    dataold = np.genfromtxt(filename, delimiter=',')
    data = np.zeros((dataold.shape[0],86))
    data[:,-1] = dataold[:,-1]
    featAdded = 0
    features = {}
    for i in range(dataold.shape[1]-1):
        values = (dataold[:,i])
        vals = set(dataold[:,i])
        for val in vals:
            features[val]=featAdded
            featAdded+=1
        for j in range(dataold.shape[0]):
            data[j,features[values[j]]] = 1
    mat = data
    df = pd.DataFrame(data=mat.astype(float))
    #df.to_csv(filename.split('.')[0]+'encoded.csv', sep=' ', header=False, float_format='%.2f', index=False)
    return data

def sklearn_network(Xtrain, ytrain, Xtest, ytest):
    network = MLPClassifier(hidden_layer_sizes=(100,100,), solver='sgd')
    start_time = time()
    print("Started training")
    network.fit(Xtrain, ytrain)
    print(f'Training time: {time() - start_time}s')
    predictions = network.predict(Xtrain)
    accuracy = accuracy_score(predictions, ytrain)
    print('Train accuracy:', accuracy)
    predictions = network.predict(Xtest)
    accuracy = accuracy_score(predictions, ytest)
    print('Test accuracy:', accuracy)

def run(trainfile,testfile,qpart):
    if(qpart=='a'):
        encode(trainfile)
        encode(testfile)
    elif(qpart=='b'):
        print('Not implemented')
    elif(qpart=='c'):
        print('Not implemented')
    elif(qpart=='d'):
        print('Not implemented')
    elif(qpart=='e'):
        print('Not implemented')
    elif(qpart=='f'):
        traindata = encode(trainfile)
        Xtrain = traindata[:,:-1]
        ytrain = traindata[:,-1]
        testdata = encode(testfile)
        Xtest = testdata[:,:-1]
        ytest = testdata[:,-1]
        sklearn_network(Xtrain, ytrain, Xtest, ytest)

run(sys.argv[1], sys.argv[2], sys.argv[3])

#bash run.sh 2 poker/poker-hand-training-true.data poker/poker-hand-testing.data a  