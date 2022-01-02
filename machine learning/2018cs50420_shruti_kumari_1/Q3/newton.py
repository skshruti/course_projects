import numpy as np
import matplotlib.pyplot as plt
import sys

# getDataX = "../data/q3/logisticX.csv"
# getDataY = "../data/q3/logisticY.csv"
getDataX = sys.argv[1]
getDataY = sys.argv[2]
x=np.genfromtxt(getDataX, delimiter=',')
y=np.genfromtxt(getDataY, delimiter=',')
m=(x.size)/2
temp1 = (x[:,0] - x[:,0].mean()) / x[:,0].std()
temp2 = (x[:,1] - x[:,1].mean()) / x[:,1].std()
x=np.vstack([np.ones((1, int(m))), temp1, temp2])


def h_theta(x,theta,i):
    return 1/(1+np.exp(-np.dot(np.transpose(theta),x[:,i])))

def gen_mat(x,i):
    mat = np.ones((3,3))
    mat[0][0] = 1
    mat[0][1] = x[1][i]
    mat[0][2] = x[2][i]
    mat[1][0] = x[1][i]
    mat[1][1] = (x[1][i])**2
    mat[1][2] = x[1][i]*x[2][i]
    mat[2][0] = x[2][i]
    mat[2][1] = x[1][i]*x[2][i]
    mat[2][2] = (x[2][i])**2
    return mat

def hessian(x,theta):
    matrices = [gen_mat(x,i)*h_theta(x,theta,i)*(1-h_theta(x,theta,i)) for i in range(len(x[0]))]
    return sum(matrices)

def Lgradient_mat(theta,x,y):
    return ((y - [1/(1+np.exp(-np.dot(np.transpose(theta),x)))])*-1*x).sum(axis=1)

def L(theta, x, y):
    total = np.sum([y[i]*np.log(h_theta(x,theta,i)) + (1-y[i])*np.log(1-h_theta(x,theta,i)) for i in range(len(x[0]))])
    return total

def regression(theta, threshold, x, y):
    theta_toplot=[]
    converge = 1000
    while (converge > threshold):
        prev = theta
        delTheta = np.matmul(np.linalg.inv(hessian(x,theta)), Lgradient_mat(theta,x,y))
        theta = theta - delTheta
        converge = abs(L(theta, x, y) - L(prev, x, y))
        theta_toplot.append(theta)
    return theta, theta_toplot

def plot_graph(threshold, x, y):
    theta = [0,0,0]
    theta_learnt, theta_toplot = regression(theta,threshold,x,y)
    label0x1 = []
    label0x2 = []
    label1x1 = []
    label1x2 = []
    for i in range(int(m)):
        if(y[i]==0.0):
            label0x1.append(x[:,i][1])
            label0x2.append(x[:,i][2])
        else:
            label1x1.append(x[:,i][1])
            label1x2.append(x[:,i][2])
            
    x_axis = np.linspace(-3, 3, 30)
    y_axis = -(theta_learnt[1]*x_axis + theta_learnt[0]) / theta_learnt[2]
    plt.plot(x_axis, y_axis, label="decision boundary")
    plt.scatter(label0x1, label0x2, label= "label=0", color= "green", marker= "o", s=30)
    plt.scatter(label1x1, label1x2, label= "label=1", color= "red", marker= "*", s=30)
    plt.legend()
    plt.xlabel('x_1')
    plt.ylabel('x_2')
    plt.show()

# theta = [0,0,0]
# theta_learnt, theta_toplot = regression(theta,3e-2,x,y)
def run(qpart):
    if(qpart=='1'):
        theta = [0,0,0]
        theta_learnt, theta_toplot = regression(theta,3e-2,x,y)
        print(theta_learnt)
    else:
        plot_graph(3e-2,x,y)

run(sys.argv[3])
