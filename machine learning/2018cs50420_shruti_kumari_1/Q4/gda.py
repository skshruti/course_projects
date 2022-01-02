import numpy as np
import matplotlib.pyplot as plt
import sys
# getDataX = "../data/q4/q4x.dat"
# getDataY = "../data/q4/q4y.dat"
getDataX = sys.argv[1]
getDataY = sys.argv[2]
x = np.genfromtxt(getDataX, delimiter="  ")
temp1 = (x[:,0] - x[:,0].mean()) / x[:,0].std()
temp2 = (x[:,1] - x[:,1].mean()) / x[:,1].std()
mean = np.mean(x, axis=0).reshape((2, 1))
stddev = np.sqrt(np.var(x, axis=0).reshape((2, 1)))
x=np.vstack([temp1, temp2])
y = np.genfromtxt(getDataY, delimiter=" ", dtype="str")
y = np.array([1 if y[i]=='Alaska' else 0 for i in range(len(y))])
m = x.size/2

def myphi(y,m):
    temp = np.array([1 if y[i]==1 else 0 for i in range(int(m))]).sum()
    return temp/m
#myphi(y,m)

def mymu0(x,y,m):
    num = np.array([x[:,i] if y[i]==0 else [0,0] for i in range(int(m))]).sum(axis=0)
    den = np.array([1 if y[i]==0 else 0 for i in range(int(m))]).sum()
    return num/den
#mymu0(x,y,m)

def mymu1(x,y,m):
    num = np.array([x[:,i] if y[i]==1 else [0,0] for i in range(int(m))]).sum(axis=0)
    den = np.array([1 if y[i]==1 else 0 for i in range(int(m))]).sum()
    return num/den
#mymu1(x,y,m)

def getmu(val,x,y,m):
    if val==0:
        return mymu0(x,y,m)
    else:
        return mymu1(x,y,m)

def mysigma(x,y,m):
    matrix = np.zeros((2,2))
    for i in range(int(m)):
        mat = (x[:,i]-getmu(y[i],x,y,m)).reshape((1,2))
        matT = np.transpose(x[:,i]-getmu(y[i],x,y,m)).reshape((2,1))
        matrix = matrix + np.dot(matT,mat)
    return matrix/m
#mysigma(x,y,m)

def mysigma0(x,y,m):
    matrix = np.zeros((2,2))
    count = 0
    for i in range(int(m)):
        if(y[i]==0):
            mat = (x[:,i]-mymu0(x,y,m)).reshape((1,2))
            matT = np.transpose(x[:,i]-mymu0(x,y,m)).reshape((2,1))
            matrix = matrix + np.dot(matT,mat)
            count+=1
    return matrix/count

def mysigma1(x,y,m):
    matrix = np.zeros((2,2))
    count = 0
    for i in range(int(m)):
        if(y[i]==1):
            mat = (x[:,i]-mymu1(x,y,m)).reshape((1,2))
            matT = np.transpose(x[:,i]-mymu1(x,y,m)).reshape((2,1))
            matrix = matrix + np.dot(matT,mat)
            count+=1
    return matrix/count

def lhslinear(phi):
    return np.log(phi/(1 - phi))

def lhsquad(phi,sigma0,sigma1):
    temp1 = np.log(phi/(1-phi))
    temp2 = (1/2)*np.log(np.linalg.det(sigma0) / np.linalg.det(sigma1))
    return temp1+temp2

def rhslinear(x,sigmainv,mu0,mu1):
    x=x.reshape((2,1))
    mu0=mu0.reshape((2,1))
    mu1=mu1.reshape((2,1))
    temp1 = -2*np.matmul(np.transpose(x), np.matmul(sigmainv, mu1))
    temp2 = 2*np.matmul(np.transpose(x), np.matmul(sigmainv, mu0))
    temp3 = np.matmul(np.transpose(mu1), np.matmul(sigmainv, mu1))
    temp4 = -1*np.matmul(np.transpose(mu0), np.matmul(sigmainv, mu0))
    temp5 = (temp1+temp2+temp3+temp4)/2
    return temp5[0]

def rhsquad(x,sigma0inv,sigma1inv,mu0,mu1):
    temp1 = -1*np.dot(np.transpose(x - mu0), np.dot(sigma0inv, x - mu0))
    temp2 = np.dot(np.transpose(x - mu1), np.dot(sigma1inv, x - mu1))
    return (temp1 + temp2)/2

def plotdblinear(sigma, x, y, m, mean, stddev, dbl, dbq):
    label0x1 = []
    label0x2 = []
    label1x1 = []
    label1x2 = []
    for i in range(int(m)):
        if(y[i]==0):
            label0x1.append((x[:,i][0]*stddev[0])+mean[0])
            label0x2.append((x[:,i][1]*stddev[1])+mean[1])
        else:
            label1x1.append((x[:,i][0]*stddev[0])+mean[0])
            label1x2.append((x[:,i][1]*stddev[1])+mean[1])

    mu0=mymu0(x,y,m)
    mu1=mymu1(x,y,m)
    phi=myphi(y,m)    
    x1 = np.linspace(50, 200, 100)
    x2 = np.linspace(300, 500, 100)
    X1, X2 = np.meshgrid(x1, x2)
    RHS = np.zeros((100, 100))
    sigmainv = np.linalg.inv(sigma)
    for i in range(100):
        for j in range(100):
            RHS[i,j] = rhslinear(np.array([(x1[j] - mean[0])/stddev[0], (x2[i] - mean[1])/stddev[1]]), sigmainv, mu0, mu1)
    LHS = lhslinear(phi)
    if dbl: plt.contour(X1, X2, RHS, levels=[LHS])
    plt.scatter(label0x1, label0x2, label= "Canada", color= "green", marker= "o", s=30)
    plt.scatter(label1x1, label1x2, label= "Alaska", color= "red", marker= "*", s=30)
    plt.legend()
    plt.xlabel('x_1')
    plt.ylabel('x_2')
    
    if dbq:
        RHS = np.zeros((100, 100))
        sigma0=mysigma0(x,y,m)
        sigma1=mysigma1(x,y,m)
        for i in range(100):
            for j in range(100):
                RHS[i,j] = rhsquad(np.array([((x1[j] - mean[0])/stddev[0])[0], ((x2[i] - mean[1])/stddev[1])[0]]), np.linalg.inv(sigma0), np.linalg.inv(sigma1), mu0, mu1)   
        LHS = lhsquad(phi, sigma0, sigma1)        
        plt.contour(X1, X2, RHS, levels=[LHS])
    plt.show()


def run(qpart):
    if(qpart=='1'):
        print("phi: ", myphi(y,m))
        print("mu0: ", mymu0(x,y,m))
        print("mu1: ", mymu1(x,y,m))
        print("sigma: ", mysigma(x,y,m))
    elif(qpart=='2'):
        plotdblinear(mysigma(x,y,m), x, y, m, mean, stddev, 0,0)
    elif(qpart=='3'):
        plotdblinear(mysigma(x,y,m), x, y, m, mean, stddev, 1,0)
    elif(qpart=='4'):
        print("mu0: ", mymu0(x,y,m))
        print("mu1: ", mymu1(x,y,m))
        print("sigma0: ", mysigma0(x,y,m))
        print("sigma1: ", mysigma1(x,y,m))
    elif(qpart=='5'):
        plotdblinear(mysigma(x,y,m), x, y, m, mean, stddev, 1,1)

run(sys.argv[3])
