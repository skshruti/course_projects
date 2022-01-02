from cvxopt import matrix
from cvxopt import solvers
import numpy as np
import math
from libsvm.svmutil import *
import time
import sys

#trainfile = 'mnist/train.csv'
def train(trainfile):
    traindata = np.genfromtxt(trainfile, delimiter=',')
    Xtrain = traindata[:,:-1]
    ytrain = traindata[:,-1]
    Xtrain = Xtrain/255
    x,y = [],[]
    for i in range(len(Xtrain)):
        if ytrain[i]==0 or ytrain[i]==1:
            #print(Xtrain[i])
            x.append(np.array(Xtrain[i]))
            #0->-1, 1->1
            y.append(1 if ytrain[i]==1 else -1)
    x = np.array(x)
    y = np.array(y)
    y = y.reshape((len(x),1))

    P = matrix(np.matmul(y*x,np.transpose(y*x)), tc='d')
    q = matrix((-1.0*np.ones((1,len(x)))).reshape((len(x),1)), tc='d')
    top = np.diag(np.ones(len(x)))
    bottom = np.diag(-1*np.ones(len(x)))
    G = matrix(np.vstack([top,bottom]), tc='d')
    h = matrix(np.vstack([np.ones(len(x)).reshape((len(x),1)),np.zeros(len(x)).reshape((len(x),1))]), tc='d')
    A = matrix(y.reshape((1,len(x))), tc='d')
    b = matrix(np.zeros(1), tc='d')

    sol = solvers.qp(P,q,G,h,A,b)
    alpha = np.array(sol['x'])
    optVal = sol['primal objective']

    alphasv, xsv, ysv = [],[],[]
    for i in range(len(alpha)):
        if alpha[i] > 1e-6:
            alphasv.append(alpha[i])
            xsv.append(x[i,:])
            ysv.append(y[i])
    alphasv = np.array(alphasv)
    xsv = np.array(xsv)

    alphayx = alpha*y*x
    w = np.sum(alphayx, axis = 0)
    w = w.reshape((784,1))
    term1 = math.inf
    term2 = -math.inf
    for i in range(len(y)):
        if alpha[i] < 1:
            temp = np.matmul(np.transpose(w),x[i])
            if y[i]==1:
                if temp<term1: term1 = temp
            else:
                if temp>term2: term2 = temp
    b = (-term1-term2)/2
    b = b[0]

    return w,b,len(alphasv)
#testfile = 'mnist/test.csv'
def test(testfile,w,b):
    testdata = np.genfromtxt(testfile, delimiter=',')
    Xtest = testdata[:,:-1]
    ytest = testdata[:,-1]
    Xtest = Xtest/255
    Xt,yt = [],[]
    for i in range(len(Xtest)):
        if ytest[i]==0 or ytest[i]==1:
            Xt.append(np.array(Xtest[i]))
            yt.append(1 if ytest[i]==1 else -1)
    Xt = np.array(Xt)
    yt = np.array(yt)
    yt = yt.reshape((len(Xt),1))
    result = {}
    for i in range(len(Xt)):
        y_pred = np.matmul(np.transpose(w),Xt[i]) + b
        if y_pred>=0:
            result[i] = {"original": yt[i], "prediction": 1}
        else:
            result[i] = {"original": yt[i], "prediction": -1}
    return accuracy(result)

def accuracy(results):
    return len([1 for term in results if results[term]['prediction']==results[term]['original']])/len(results)

def K(x, z, gamma = 0.05):
    xsquare = np.sum(x**2,axis=1).reshape((x.shape[0],1))
    zsquare = np.sum(z**2,axis=1).reshape((1,z.shape[0]))
    kxz = -2*np.matmul(x,np.transpose(z))
    normsq = xsquare + zsquare + kxz
    return np.exp(-1*gamma*normsq)

def traingauss(x,y,classpos,classneg):
    P = matrix(K(x,x)*y*np.transpose(y), tc='d')
    q = matrix((-1.0*np.ones((1,len(x)))).reshape((len(x),1)), tc='d')
    top = np.diag(np.ones(len(x)))
    bottom = np.diag(-1*np.ones(len(x)))
    G = matrix(np.vstack([top,bottom]), tc='d')
    h = matrix(np.vstack([np.ones(len(x)).reshape((len(x),1)),np.zeros(len(x)).reshape((len(x),1))]), tc='d')
    A = matrix(y.reshape((1,len(x))), tc='d')
    b = matrix(np.zeros(1), tc='d')

    sol = solvers.qp(P,q,G,h,A,b)
    alpha = np.array(sol['x'])
    optVal = sol['primal objective']

    term1 = math.inf
    term2 = -math.inf
    wTphix = np.sum(alpha*y*K(x,x), axis = 0)
    for i in range(len(y)):
        if alpha[i] < 1:
            temp = wTphix[i]
            if y[i]==1:
                if temp<term1: term1 = temp
            else:
                if temp>term2: term2 = temp
    b = (-term1-term2)/2

    alphasv, xsv, ysv = [],[],[]
    for i in range(len(alpha)):
        if alpha[i] > 1e-6:
            alphasv.append(alpha[i])
            xsv.append(x[i,:])
            ysv.append(y[i])
    alphasv = np.array(alphasv)
    xsv = np.array(xsv)

    return b, alphasv, xsv, ysv

def testgauss(Xt,yt, b, alphasv, xsv, ysv, classpos, classneg):
    result = {}
    wTx = np.sum(alphasv*ysv*K(xsv,Xt), axis = 0)
    for i in range(len(Xt)):
        y_pred = wTx[i] + b
        if y_pred>=0:
            result[i] = {"original": yt[i], "prediction": 1}
        else:
            result[i] = {"original": yt[i], "prediction": -1}
    return accuracy(result), result

def get_traindata(trainfile, classpos, classneg): 
    traindata = np.genfromtxt(trainfile, delimiter=',')
    Xtrain = traindata[:,:-1]
    ytrain = traindata[:,-1]
    Xtrain = Xtrain/255
    x,y = [],[]
    for i in range(len(Xtrain)):
        if ytrain[i]==classpos or ytrain[i]==classneg:
            x.append(np.array(Xtrain[i]))
            y.append(1 if ytrain[i]==classpos else -1)
    x = np.array(x)
    y = np.array(y)
    y = y.reshape((len(x),1))
    return x,y

def get_testdata(testfile, xlabels, classpos, classneg): 
    testdata = np.genfromtxt(testfile, delimiter=',')
    Xtest = testdata[:,:-1]
    ytest = testdata[:,-1]
    Xtest = Xtest/255
    Xt,yt,yori,xori = [],[],[],[]
    for i in range(len(Xtest)):
        if ytest[i]==classneg or ytest[i]==classpos:
            Xt.append(np.array(Xtest[i]))
            yt.append(1 if ytest[i]==classpos else -1)
            yori.append(ytest[i])
            xori.append(xlabels[i])
    Xt = np.array(Xt)
    yt = np.array(yt)
    yt = yt.reshape((len(Xt),1))
    return Xt, yt, yori, xori

def trainlibsvm(trainfile, gauss):
    traindata = np.genfromtxt(trainfile, delimiter=',')
    Xtrain = traindata[:,:-1]
    ytrain = traindata[:,-1]
    Xtrain = Xtrain/255
    x,y = [],[]
    for i in range(len(Xtrain)):
        if ytrain[i]==0 or ytrain[i]==1:
            x.append(np.array(Xtrain[i]))
            y.append(1 if ytrain[i]==1 else -1)
    x = np.array(x)
    y = np.array(y)
    y = y.reshape((len(x),1))

    svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]
    problem = svm_problem(y.reshape(y.shape[0]), x)
    param = svm_parameter('-s 0 -t 0')
    if gauss: param = svm_parameter('-s 0 -t 2 -g 0.05')
    model = svm_train(problem, param)

    return model

def testlibsvm(trainfile, model):
    testdata = np.genfromtxt(testfile, delimiter=',')
    Xtest = testdata[:,:-1]
    ytest = testdata[:,-1]
    Xtest = Xtest/255
    Xt,yt = [],[]
    for i in range(len(Xtest)):
        if ytest[i]==0 or ytest[i]==1:
            Xt.append(np.array(Xtest[i]))
            yt.append(1 if ytest[i]==1 else -1)
    Xt = np.array(Xt)
    yt = np.array(yt)
    yt = yt.reshape((len(Xt),1))

    a, b, val = svm_predict(yt.reshape(yt.shape[0]), Xt, model)

def get_classes():
    classes = set()
    for i in range(10):
        for j in range(10):
            if i!=j and (j,i) not in classes:
                classes.add((i,j))
    return classes

def accuracy_multiclass(results):
    count = 0
    for result in results:
        temp = {0:results[result][0]['count'],
                1:results[result][1]['count'],
                2:results[result][2]['count'],
                3:results[result][3]['count'],
                4:results[result][4]['count'],
                5:results[result][5]['count'],
                6:results[result][6]['count'],
                7:results[result][7]['count'],
                8:results[result][8]['count'],
                9:results[result][9]['count']}
        maxcount = max(temp, key= lambda x: temp[x])
        results[result]['prediction'] = maxcount
        count += results[result]['prediction']==results[result]['original']
    return count/len(results)

def get_testdata_mc(testfile, xlabels, classpos, classneg): 
    testdata = np.genfromtxt(testfile, delimiter=',')
    Xtest = testdata[:,:-1]
    ytest = testdata[:,-1]
    Xtest = Xtest/255
    Xt,yt,yori,xori = [],[],[],[]
    for i in range(len(Xtest)):
        Xt.append(np.array(Xtest[i]))
        yt.append(1 if ytest[i]==classpos else -1)
        yori.append(ytest[i])
        xori.append(xlabels[i])
    Xt = np.array(Xt)
    yt = np.array(yt)
    yt = yt.reshape((len(Xt),1))
    return Xt, yt, yori, xori

def train_multiclass(trainfile, classes):
    alphasvs,xsvs, ysvs, bs= {},{},{},{}
    for (classpos,classneg) in classes:
        x, y = get_traindata(trainfile, classpos, classneg)
        b, alphasv, xsv, ysv = traingauss(x,y, classpos, classneg)
        alphasvs[(classpos,classneg)] = alphasv
        xsvs[(classpos,classneg)] = xsv
        ysvs[(classpos,classneg)] = ysv
        bs[(classpos,classneg)] = b
    return alphasvs,xsvs,ysvs,bs,classes

def test_multiclass(alphasvs,xsvs,ysvs,bs,classes,testfile,xlabels):
    results = {}
    for (classpos,classneg) in classes:
        alphasv, xsv, ysv, b = alphasvs[(classpos,classneg)], xsvs[(classpos,classneg)], ysvs[(classpos,classneg)], bs[(classpos,classneg)]
        Xt, yt, yori, xori = get_testdata_mc(testfile, xlabels, classpos, classneg)
        wTx = np.sum(alphasv*ysv*K(xsv,Xt), axis = 0)
        for i in range(len(Xt)):
            if xori[i] not in results:
                results[xori[i]] = {'original':yori[i],
                                    0:{'count':0,'score':0},
                                    1:{'count':0,'score':0},
                                    2:{'count':0,'score':0},
                                    3:{'count':0,'score':0},
                                    4:{'count':0,'score':0},
                                    5:{'count':0,'score':0},
                                    6:{'count':0,'score':0},
                                    7:{'count':0,'score':0},
                                    8:{'count':0,'score':0},
                                    9:{'count':0,'score':0}}
            y_pred = wTx[i] + b
            if y_pred>=0:
                results[xori[i]][classpos]['count']+=1
                results[xori[i]][classpos]['score']=wTx
            else:
                results[xori[i]][classneg]['count']+=1
                results[xori[i]][classneg]['score']=wTx
    return results

def trainlibsvm_mc(trainfile, gauss):
    traindata = np.genfromtxt(trainfile, delimiter=',')
    Xtrain = traindata[:,:-1]
    ytrain = traindata[:,-1]
    Xtrain = Xtrain/255
    x,y = [],[]
    for i in range(len(Xtrain)):
        x.append(np.array(Xtrain[i]))
        y.append(ytrain[i])
    x = np.array(x)
    y = np.array(y)
    y = y.reshape((len(x),1))

    svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]
    problem = svm_problem(y.reshape(y.shape[0]), x)
    param = svm_parameter('-s 1 -t 0')
    if gauss: param = svm_parameter('-s 0 -t 2 -g 0.05')
    model = svm_train(problem, param)

    return model
    

def testlibsvm_mc(testfile, model):
    testdata = np.genfromtxt(testfile, delimiter=',')
    Xtest = testdata[:,:-1]
    ytest = testdata[:,-1]
    Xtest = Xtest/255
    Xt,yt = [],[]
    for i in range(len(Xtest)):
        Xt.append(np.array(Xtest[i]))
        yt.append(ytest[i])
    Xt = np.array(Xt)
    yt = np.array(yt)
    yt = yt.reshape((len(Xt),1))

    a, b, val = svm_predict(yt.reshape(yt.shape[0]), Xt, model)
    return a,b,val


def part1a(trainfile,testfile):
    print("\n\nsvm model with linear kernel")
    start_time = time.time()
    w,b,nSV = train(trainfile)
    print('\ntraining time: ')
    print("--- %s seconds ---" % (time.time() - start_time))
    print("b: ", b, "nSV: ", nSV)
    print('Test accuracy: ', test(testfile,w,b))

def part1b(trainfile,testfile):
    testdata = np.genfromtxt(testfile, delimiter=',')
    counter, xlabels = 0, []
    for i in range(len(testdata)):
        xlabels.append(counter)
        counter += 1
    print("\n\nsvm model with gaussian kernel")
    x, y = get_traindata(trainfile, 1, 0)
    start_time = time.time()
    b, alphasv, xsv, ysv = traingauss(x,y, 1, 0)
    print('\ntraining time: ')
    print("--- %s seconds ---" % (time.time() - start_time))
    print("b: ", b, "nSV: ", len(xsv))
    Xt,yt,yori,xlabels = get_testdata(testfile, xlabels, 1, 0)
    acc, results = testgauss(Xt,yt,b,alphasv, xsv, ysv, 1, 0)
    print('Test accuracy: ', acc)

def part1c(trainfile,testfile):
    print("\n\nlibsvm with linear kernel")
    start_time = time.time()
    model = trainlibsvm(trainfile, False)
    print('\ntraining time: ')
    print("--- %s seconds ---" % (time.time() - start_time))
    testlibsvm(testfile, model)
    print("\n\nlibsvm with gaussian kernel")
    start_time = time.time()
    model = trainlibsvm(trainfile, True)
    print('\ntraining time: ')
    print("--- %s seconds ---" % (time.time() - start_time))
    testlibsvm(testfile, model)

def part2a(trainfile,testfile):
    testdata = np.genfromtxt(testfile, delimiter=',')
    counter, xlabels = 0, []
    for i in range(len(testdata)):
        xlabels.append(counter)
        counter += 1
    print("\n\nsvm model multiclass with gaussian kernel")
    start_time = time.time()
    classes = get_classes()
    alphasvs,xsvs, ysvs, bs, classes = train_multiclass(trainfile, classes)
    print('\ntraining time: ')
    print("--- %s seconds ---" % (time.time() - start_time))
    results = test_multiclass(alphasvs,xsvs, ysvs, bs, classes,testfile,xlabels)
    print('Test accuracy: ', accuracy_multiclass(results))
    return results

def part2b(trainfile,testfile):
    print("\n\nlibsvm multi class with gaussian kernel")
    start_time = time.time()
    model = trainlibsvm_mc(trainfile, True)
    print('\ntraining time: ')
    print("--- %s seconds ---" % (time.time() - start_time))
    a, b, val = testlibsvm_mc(testfile, model)

def part2c(results):
    confMat = np.zeros((10,10))
    for result in results:
        i = int(results[result]['original']) - 1
        j = results[result]['prediction'] - 1
        confMat[i][j] += 1
    print(confMat)

trainfile = 'mnist/train.csv'
testfile = 'mnist/test.csv'

import json
def run(trainfile,testfile,part,qpart):
    if part=='0':
        if(qpart=='a'):
            part1a(trainfile,testfile)
        elif(qpart=='b'):
            part1b(trainfile, testfile)
        elif(qpart=='c'):
            part1c(trainfile, testfile)
    elif part=='1':
        if(qpart=='a'):
            results = part2a(trainfile,testfile)
        elif(qpart=='b'):
            part2b(trainfile, testfile)
        elif(qpart=='c'):
            print('confusion matrix for multi class gaussian')
            results = part2a(trainfile,testfile)
            part2c(results)
        elif(qpart=='d'):
            print('not implemented')
    else:
        print('please provide correct part name: ',qpart)
run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
