import collections
import numpy as np
import json
import random
import math
import sys
import math
from sklearn.metrics import accuracy_score
import os
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import pandas as pd

#trainfile = 'bank_dataset/bank_train.csv'
def get_data(file):
    data = np.genfromtxt(file, delimiter=';', dtype='<U')
    for i in range(1,data.shape[0]):
        for j in range(data.shape[1]):
            val = 0
            try:
                val = (int(data[i][j]))
            except:
                val = ((data[i][j].split("\""))[1])
            data[i][j] = val

    X = data[1:,:-1]
    y = data[1:,-1]
    return X, y

class Node:
    def __init__(self, num):
        self.num = num
        self.children = {}
        self.label = None
        self.attr = None
        self.median = None

def median(l):
    l.sort()
    if(len(l)%2 == 0):
        return (l[len(l)//2 - 1]+l[len(l)//2])/2
    else:
        return l[len(l)//2]

def entropy(y):
    if(len(y)==0): 
        return math.inf
    yes = (len([1 for i in range(len(y)) if y[i]=='yes']))/len(y)
    no = (len([1 for i in range(len(y)) if y[i]=='no']))/len(y)
    if(yes==0 or no==0): return 0
    else: return -1*(yes*np.log(yes) + no*np.log(no))

def binary_split(x,y,attr,val):
    xleft, yleft, xright, yright = [],[],[],[]
    for i in range(x.shape[0]):
        if(int(x[i,attr])<=val):
            xleft.append(x[i,:])
            yleft.append(y[i])
        else:
            xright.append(x[i,:])
            yright.append(y[i])
    return np.array(xleft), np.array(yleft), np.array(xright), np.array(yright)

def category_specific(x,y,attr,val):
    xtemp, ytemp = [],[]
    for i in range(x.shape[0]):
        if(x[i,attr]==val):
            xtemp.append(x[i,:])
            ytemp.append(y[i])
    return np.array(xtemp), np.array(ytemp)

def chooseBestAttr(x, y):
    #print("choosing attr for: ",len(x),len(y))
    nattrs = Xtrain.shape[1]
    minentropy = math.inf
    bestattr = -1
    for attr in range(nattrs):
        try:
            int(x[0,attr])
            l = [int(x[i,attr]) for i in range(x.shape[0])]
            val = median(l)
            xleft, yleft, xright, yright = binary_split(x,y,attr,val)
            curE = ((len(yleft)*entropy(yleft)) + (len(yright)*entropy(yright)))/len(y)
            if curE<minentropy:
                #print("changing best attr to ", attr, "because of ", curE)
                bestattr = attr
                minentropy = curE
        except ValueError:
            vals = set([x[i,attr] for i in range(x.shape[0])])
            curE = 0
            for val in vals:
                xval, yval = category_specific(x,y,attr,val)
                curE += (len(yval)*entropy(yval))/len(y)
            if curE<minentropy:
                #print("changing best attr to ", attr, "because of str", curE)
                bestattr = attr
                minentropy = curE
    if abs(entropy(y) - minentropy) < 1e-9: return -1
    #print("returning best attr ", bestattr, "ori: ", entropy(y), "cur: ", minentropy)
    return bestattr

num_nodes = 0
val_accuracies = {}
train_accuracies = {}
test_accuracies = {}
def grow_tree(node, x, y, Xvalset, yvalset, Xtest, ytest, Xtrain, ytrain):
    global num_nodes
    print(num_nodes)
    if (len(set(y))==1):
        node.label = y[0]
        return node
    attr = chooseBestAttr(x, y)
    if attr==-1:
        node.label = (collections.Counter(y)).most_common(1)[0][0]
        return node
    node.attr = attr
    try:
        int(x[0,attr])
        leftnode = Node(num_nodes)
        num_nodes += 1
        leftnode.label = (collections.Counter(y)).most_common(1)[0][0]
        val_accuracies[num_nodes] = accuracy(Xvalset,yvalset, root)
        train_accuracies[num_nodes] = accuracy(Xtrain,ytrain, root)
        test_accuracies[num_nodes] = accuracy(Xtest,ytest, root)
        #print(num_nodes, val_accuracies[num_nodes], train_accuracies[num_nodes], test_accuracies[num_nodes])
        
        rightnode = Node(num_nodes)
        num_nodes += 1
        rightnode.label = (collections.Counter(y)).most_common(1)[0][0]
        val_accuracies[num_nodes] = accuracy(Xvalset,yvalset, root)    
        train_accuracies[num_nodes] = accuracy(Xtrain,ytrain, root)
        test_accuracies[num_nodes] = accuracy(Xtest,ytest, root)
        #print(num_nodes, val_accuracies[num_nodes], train_accuracies[num_nodes], test_accuracies[num_nodes])
        
        l = [int(x[i,attr]) for i in range(x.shape[0])]
        val = median(l)
        node.median = val
        xleft, yleft, xright, yright = binary_split(x,y,attr,val)
        node.children["l"]=leftnode
        node.children["r"]=rightnode
        #print("leftnode: ", leftnode.num, "length: ", len(xleft), "rightnode: ", rightnode.num, "length: ", len(xright))
        grow_tree(leftnode, xleft, yleft, Xvalset, yvalset, Xtest, ytest, Xtrain, ytrain)
        grow_tree(rightnode, xright, yright, Xvalset, yvalset, Xtest, ytest, Xtrain, ytrain)
    except ValueError:
        vals = set([x[i,attr] for i in range(x.shape[0])])
        for val in vals:
            xval, yval = category_specific(x,y,attr,val)
            newnode = Node(num_nodes)
            newnode.label = (collections.Counter(y)).most_common(1)[0][0]
            num_nodes += 1
            val_accuracies[num_nodes] = accuracy(Xvalset,yvalset, root)
            train_accuracies[num_nodes] = accuracy(Xtrain,ytrain, root)
            test_accuracies[num_nodes] = accuracy(Xtest,ytest, root)
            #print(num_nodes, val_accuracies[num_nodes], train_accuracies[num_nodes], test_accuracies[num_nodes])
            node.children[val]=(newnode)
            #print("newnode: ", newnode.num, "length: ", len(xval))
            grow_tree(newnode, xval, yval, Xvalset, yvalset, Xtest, ytest, Xtrain, ytrain)

def findlabel(root, x):
    attr = root.attr
    if attr is None:
        return root.label
    else:
        if root.median is None:
            val = x[attr]
            if val not in root.children:
                return root.label
            return findlabel(root.children[val],x)
        else:
            if int(x[attr])<=root.median:
                return findlabel(root.children["l"],x)
            else:
                return findlabel(root.children["r"],x)

def accuracy(x,y,root):
    corr = 0
    preds = set()
    for i in range(len(x)):
        preds.add(findlabel(root, x[i]))
        corr += findlabel(root, x[i])==y[i]
    return corr/len(x)

node_accuracies = {}
def nodeAccuracies(root, x, y):
    attr = root.attr
    count = np.count_nonzero(y == root.label)
    node_accuracies[root.num] = count
    if attr is None:
        return
    else:
        if root.median is None:
            for val in root.children:                
                xval, yval = category_specific(x,y,attr,val)
                nodeAccuracies(root.children[val], xval, yval)
        else:
            xleft, yleft, xright, yright = binary_split(x,y,attr,root.median)
            nodeAccuracies(root.children["l"], xleft, yleft)
            nodeAccuracies(root.children["r"], xright, yright)

def prune(node, x, y, Xvalset, yvalset):
    node_accuracy = node_accuracies[node.num]
    for child in node.children:
        prune(node.children[child], x, y, Xvalset, yvalset)
    children_accuracy = sum([node_accuracies[node.children[child].num] for child in node.children])
    if children_accuracy<=node_accuracy:
        #print('pruning node')
        node.attr = None
        node.children = {}
    else:
        node_accuracies[node.num] = children_accuracy

def encode(dataold):
    data = np.zeros((dataold.shape[0],50), dtype='<U15')
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            data[i,j]='0'
    featAdded = 0
    features = {}
    for i in range(dataold.shape[1]-1):
        try:
            int(dataold[0,i])
            for j in range(dataold.shape[0]):
                data[j,i] = dataold[j,i]
            featAdded+=1
        except:
            values = (dataold[:,i])
            vals = set(dataold[:,i])
            for val in vals:
                features[val]=featAdded
                featAdded+=1
            for j in range(dataold.shape[0]):
                data[j,features[values[j]]] = 1
    return data

def gridSearch(x, y):
    n_estimators, max_features, min_samples_split = [50, 150, 250, 350, 450], [0.1, 0.3, 0.5, 0.7, 0.9], [2, 4, 6, 8, 10]
    maxoob = -math.inf
    nest, mfeatures, msamples = None, None, None
    for est in n_estimators:
        for feat in max_features:
            for samp in min_samples_split:
                #print(est, feat, samp)
                rfc = RandomForestClassifier(n_estimators=est, max_features=feat, min_samples_split=samp, criterion='entropy', oob_score=True)
                rfc.fit(x, y)
                #print(rfc.oob_score_)
                if rfc.oob_score_ > maxoob:
                    nest = est
                    mfeatures = feat
                    msamples = samp
                    maxoob = rfc.oob_score_
    return nest, mfeatures, msamples, maxoob

def randomForest(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest):
    rfc = RandomForestClassifier(n_estimators=350, max_features=0.3, min_samples_split=10, criterion='entropy', oob_score=True)
    rfc.fit(Xtrain, ytrain)
    print('Out-of-bag:', rfc.oob_score_)
    predictions = rfc.predict(Xtrain)
    print('Train:', accuracy_score(ytrain, predictions))
    predictions = rfc.predict(Xvalset)
    print('Validation:', accuracy_score(yvalset, predictions))
    predictions = rfc.predict(Xtest)
    print('Test:', accuracy_score(ytest, predictions))

def gridSearch(x, y):
    n_estimators, max_features, min_samples_split = [50, 150, 250, 350, 450], [0.1, 0.3, 0.5, 0.7, 0.9], [2, 4, 6, 8, 10]
    maxoob = -math.inf
    nest, mfeatures, msamples = None, None, None
    for est in n_estimators:
        for feat in max_features:
            for samp in min_samples_split:
                print(est, feat, samp)
                rfc = RandomForestClassifier(n_estimators=est, max_features=feat, min_samples_split=samp, criterion='entropy', oob_score=True)
                rfc.fit(x, y)
                print(rfc.oob_score_)
                if rfc.oob_score_ > maxoob:
                    nest = est
                    mfeatures = feat
                    msamples = samp
                    maxoob = rfc.oob_score_
    return nest, mfeatures, msamples, maxoob

def analysis(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest):
    val = {}
    test = {}
    train = {}
    n_estimators, max_features, min_samples_split = [50, 150, 250, 350, 450], [0.1, 0.3, 0.5, 0.7, 0.9], [2, 4, 6, 8, 10]
    for samp in min_samples_split:
        print(samp)
        rfc = RandomForestClassifier(n_estimators=350, max_features=0.3, min_samples_split=samp, criterion='entropy', oob_score=True)
        rfc.fit(Xtrain, ytrain)
        predictions = rfc.predict(Xtrain)
        train[samp] = accuracy_score(ytrain, predictions)
        predictions = rfc.predict(Xvalset)
        val[samp] = accuracy_score(yvalset, predictions)
        predictions = rfc.predict(Xtest)
        test[samp] = accuracy_score(ytest, predictions)
    x = list(val.keys())
    plt.xlabel('min_samples_split')
    plt.ylabel('accuracy')
    plt.plot(x, list(val.values()), label = "Validation set")
    plt.plot(x, list(test.values()), label = "Test set")
    plt.legend()
    plt.show()
    val = {}
    test = {}
    train = {}
    for est in n_estimators:
        print(est)
        rfc = RandomForestClassifier(n_estimators=est, max_features=0.3, min_samples_split=10, criterion='entropy', oob_score=True)
        rfc.fit(Xtrain, ytrain)
        predictions = rfc.predict(Xtrain)
        train[est] = accuracy_score(ytrain, predictions)
        predictions = rfc.predict(Xvalset)
        val[est] = accuracy_score(yvalset, predictions)
        predictions = rfc.predict(Xtest)
        test[est] = accuracy_score(ytest, predictions)
    x = list(val.keys())
    plt.xlabel('n_estimators')
    plt.ylabel('accuracy')
    plt.plot(x, list(val.values()), label = "Validation set")
    plt.plot(x, list(test.values()), label = "Test set")
    plt.legend()
    plt.show()
    val = {}
    test = {}
    train = {}
    for feat in max_features:
        print(feat)
        rfc = RandomForestClassifier(n_estimators=350, max_features=feat, min_samples_split=10, criterion='entropy', oob_score=True)
        rfc.fit(Xtrain, ytrain)
        predictions = rfc.predict(Xtrain)
        train[feat] = accuracy_score(ytrain, predictions)
        predictions = rfc.predict(Xvalset)
        val[feat] = accuracy_score(yvalset, predictions)
        predictions = rfc.predict(Xtest)
        test[feat] = accuracy_score(ytest, predictions)
    x = list(val.keys())
    plt.xlabel('max_features')
    plt.ylabel('accuracy')
    plt.plot(x, list(val.values()), label = "Validation set")
    plt.plot(x, list(test.values()), label = "Test set")
    plt.legend()
    plt.show()


trainfile = 'bank_dataset/bank_train.csv'
testfile = 'bank_dataset/bank_test.csv'
valfile = 'bank_dataset/bank_val.csv'
Xtrain, ytrain = get_data(trainfile)
Xtest, ytest = get_data(testfile)
Xvalset, yvalset = get_data(valfile)

def growAndPlot(x, y, Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest):
    grow_tree(root, x, y, Xvalset, yvalset, Xtest, ytest, Xtrain, ytrain)
    print("Accuracy on train set: ", accuracy(Xtrain,ytrain,root))
    print("Accuracy on test set: ", accuracy(Xtest,ytest,root))
    print("Accuracy on validation set: ", accuracy(Xvalset,yvalset,root))
    xaxis = list(val_accuracies.keys())
    plt.plot(xaxis, list(val_accuracies.values()), label = "Validation set")
    plt.plot(xaxis, list(train_accuracies.values()), label = "Train set")
    plt.plot(xaxis, list(test_accuracies.values()), label = "Test set")
    plt.legend()
    plt.show()
    
def part1(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest):
    x, y = Xtrain[:1000, :], ytrain[:1000]
    #x, y = Xtrain, ytrain
    print('Multi Class Split')
    growAndPlot(x, y, Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest)
    # print('One Hot Encoding')
    # growAndPlot(encode(x), y, encode(Xtrain), ytrain, encode(Xvalset), yvalset, encode(Xtest), ytest)

def part2(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest):
    print('Pruning')
    #x, y = Xtrain[:1000, :], ytrain[:1000]
    x, y = Xtrain, ytrain
    growAndPlot(x, y, Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest)
    nodeAccuracies(root, Xvalset, yvalset)
    prune(root, x, y, Xvalset, yvalset)
    print("Accuracy on train set after pruning: ", accuracy(Xtrain,ytrain,root))
    print("Accuracy on test set after pruning: ", accuracy(Xtest,ytest,root))
    print("Accuracy on validation set after pruning: ", accuracy(Xvalset,yvalset,root))

def part3(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest):
    randomForest(encode(Xtrain), ytrain, encode(Xvalset), yvalset, encode(Xtest), ytest)

def part4(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest):
    analysis(encode(Xtrain), ytrain, encode(Xvalset), yvalset, encode(Xtest), ytest)

root = Node(0)
def run(trainfile,testfile,valfile,qpart):
    Xtrain, ytrain = get_data(trainfile)
    Xtest, ytest = get_data(testfile)
    Xvalset, yvalset = get_data(valfile)
    if(qpart=='a'):
        part1(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest)
    elif(qpart=='b'):
        part2(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest)
    elif(qpart=='c'):
        part3(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest)
    elif(qpart=='d'):
        part4(Xtrain, ytrain, Xvalset, yvalset, Xtest, ytest)
run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
#bash run.sh 1 bank_dataset/bank_train.csv bank_dataset/bank_test.csv bank_dataset/bank_val.csv b
