import numpy as np
import matplotlib.pyplot as plt
import sys
#set m to 1 million
m=10**6
#generate x
x_0 = np.ones(m)
x_1 = np.random.normal(3, 4, m)
x_2 = np.random.normal(-1, 4, m)
x=np.vstack([x_0,x_1,x_2])
#generate y
theta = [3,1,2]
e = np.random.normal(0, 2, m)
y = theta[0] + theta[1]*x[1] + theta[2]*x[2] + e
#getData = ../data/q2/q2test.csv
getData = sys.argv[1]
data=np.genfromtxt(getData, delimiter=',')[1:]
testm = data.size/3
testx=np.vstack([np.ones(int(testm)),data[:,0],data[:,1]])
testy=data[:,2]

def J(theta, x, y, m):
    sum = np.sum([(y - np.dot(np.transpose(theta),x))**2])
    return sum/(2*m)

def create_batches(x,y,batch_size,m):
    batchesX = np.split(x, m//batch_size, axis=1)
    batchesY = np.split(y, m//batch_size)
    return batchesX,batchesY

def regression(theta, threshold, eta, x, y, batch_size, mean_size, m):
    past_mean = 1000
    pastJs =[]
    thetas_toplot = []
    converge = False
    add_theta = 0
    while (not converge):
        batchesX, batchesY = create_batches(x, y, batch_size, m)
        for i in range(len(batchesX)):
            if(add_theta % 25 == 0): thetas_toplot.append(theta)
            prev = theta
            batchX, batchY = batchesX[i], batchesY[i]
            delTheta = (eta/batch_size) * ((np.dot(np.transpose(theta),batchX) - batchY)*batchX).sum(axis=1)
            theta = theta - delTheta
            curJ = J(theta, batchX, batchY, m)
            pastJs.append(curJ)
            if(len(pastJs) == mean_size):
                cur_mean = np.mean(pastJs)
                #print(cur_mean, past_mean, cur_mean - past_mean)
                if((past_mean - cur_mean) < threshold): converge = True
                pastJs = []
                past_mean = cur_mean
            if(converge):
                return theta, thetas_toplot
            add_theta+=1
    return theta, thetas_toplot


# theta = np.zeros(3)
# threshold = 1e-12
# eta = 0.001

# batch_sizes = [1, 100, 10000, 1000000]

# print(regression(theta,1e-12,eta,x,y,1,50000))
# print(regression(theta,1e-10,eta,x,y,100,5000))
# print(regression(theta,1e-8,eta,x,y,10000,500))
# print(regression(theta,1e-6,eta,x,y,1000000,50))

def plot_graph(batch_size, threshold, eta, mean_size, x, y):
    theta = np.zeros(3)
    theta_learnt, theta_toplot = regression(theta,threshold,eta,x,y,batch_size,mean_size,m)
    theta_toplot=np.array(theta_toplot)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter(theta_toplot[:,0], theta_toplot[:,1], theta_toplot[:,2], c='b', marker='o')
        
    ax.set_xlabel('theta_0')
    ax.set_ylabel('theta_1')
    ax.set_zlabel('theta_2')
    ax.set_title('Batch size: '+ str(batch_size))
    plt.show()

eta = 0.001
def run(qpart):
    if(qpart == '1'):
        print("Data sampled successfully")
    elif(qpart == '2'):
        print("Running on batch size: 1")
        theta_learnt, theta_toplot = regression(np.zeros(3),1e-12,eta,x,y,1,50000,m)
        print(theta_learnt, "\n\n")
        print("Running on batch size: 100")
        theta_learnt, theta_toplot = regression(np.zeros(3),1e-10,eta,x,y,100,5000,m)
        print(theta_learnt, "\n\n")
        print("Running on batch size: 10000")
        theta_learnt, theta_toplot = regression(np.zeros(3),1e-8,eta,x,y,10000,500,m)
        print(theta_learnt, "\n\n")
        print("Running on batch size: 1000000")
        theta_learnt, theta_toplot = regression(np.zeros(3),1e-6,eta,x,y,1000000,50,m)
        print(theta_learnt, "\n\n")
    elif(qpart == '3'):
        print("Running on batch size: 1")
        theta_learnt, theta_toplot = regression(np.zeros(3),1e-12,eta,x,y,1,50000,m)
        print("error in new dataset: ", J(theta_learnt, testx, testy, testm), "\n\n")
        print("Running on batch size: 100")
        theta_learnt, theta_toplot = regression(np.zeros(3),1e-10,eta,x,y,100,5000,m)
        print("error in new dataset: ", J(theta_learnt, testx, testy, testm), "\n\n")
        print("Running on batch size: 10000")
        theta_learnt, theta_toplot = regression(np.zeros(3),1e-8,eta,x,y,10000,500,m)
        print("error in new dataset: ", J(theta_learnt, testx, testy, testm), "\n\n")
        print("Running on batch size: 1000000")
        theta_learnt, theta_toplot = regression(np.zeros(3),1e-6,eta,x,y,1000000,50,m)
        print("error in new dataset: ", J(theta_learnt, testx, testy, testm), "\n\n")
    elif(qpart == '4'):
        print("Running on batch size: 1")
        plot_graph(1, 1e-12, eta, 50000, x, y)
        print("Running on batch size: 100")
        plot_graph(100, 1e-10, eta, 5000, x, y)
        print("Running on batch size: 10000")
        plot_graph(10000, 1e-8, eta, 500, x, y)
        print("Running on batch size: 1000000")
        plot_graph(1000000, 1e-6, eta, 50, x, y)

run(sys.argv[2])