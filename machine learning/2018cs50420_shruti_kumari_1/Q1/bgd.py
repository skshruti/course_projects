#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import sys
# getDataX = '../data/q1/linearX.csv'
# getDataY = '../data/q1/linearY.csv'
getDataX = sys.argv[1]
getDataY = sys.argv[2]
x=np.genfromtxt(getDataX, delimiter=',')
y=np.genfromtxt(getDataY, delimiter=',')
m=x.size
x = (x - x.mean()) / x.std()
x=np.vstack([np.ones((1, m)), x])
theta_toplot=[]
# for i in range(1, x.shape[0]):
#     x[i] = (x[i] - x[i].mean(axis=0)) / x[i].std(axis=0)

def J(theta, x, y, m):
    total = np.sum([(y - np.dot(np.transpose(theta),x))**2])
    return total/(2*m)

def regression(theta, threshold, eta, x, y):
    theta_toplot=[]
    converge = J(theta, x, y, m)
    while (converge > threshold):
        prev = theta
        delTheta = (eta/m) * ((np.dot(np.transpose(theta),x) - y)*x).sum(axis=1)
        theta = theta - delTheta
        converge = abs(J(theta, x, y,  m) - J(prev, x, y, m))
        theta_toplot.append(theta)
    return theta, theta_toplot

def plot_graph(x,theta_learnt):
    x_axis = x[1]
    y_axis = np.dot(np.transpose(theta_learnt),x) 
    plt.plot(x_axis, y_axis, label="h_theta(x)")
    plt.scatter(x_axis, y, label= "data", color= "green",
                marker= "o", s=30)
    plt.legend()
    plt.xlabel('Acidity')
    plt.ylabel('Density')
    plt.title('Hypothesis function')
    plt.show()

def plot_mesh(threshold,eta,x,y):
    theta = np.zeros(2)
    theta_learnt, theta_toplot = regression(theta,threshold,eta, x,y)
    theta_toplot=np.array(theta_toplot)
    def f(valx, valy):
        theta_temp = np.array([valx,valy])
        return J(theta_temp,x,y,m)

    a = np.linspace(0, 2, 100)
    b = np.linspace(-1, 1, 100)

    X, Y = np.meshgrid(a, b)
    Z = np.vectorize(f)(X, Y)
    ax = plt.axes(projection='3d')

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                            cmap='viridis', edgecolor='none');

    for theta_temp in theta_toplot:
        a = theta_temp[0]
        b = theta_temp[1]
        z = J(np.array([a,b]),x,y,m)
        ax.scatter(a, b, z, c='b', marker='o')
        plt.pause(5)

    ax.set_xlabel('theta_0')
    ax.set_ylabel('theta_1')
    ax.set_zlabel('J(theta)')
    ax.set_title('Error function')
    plt.show()

def f(valx, valy):
    theta_temp = np.array([valx,valy])
    return J(theta_temp,x,y,m)
def plot_contour(threshold,eta,x,y):
    theta = np.zeros(2)
    theta_learnt, theta_toplot = regression(theta,threshold,eta, x,y)
    theta_toplot=np.array(theta_toplot)

    a = np.linspace(0, 2, 100)
    b = np.linspace(-1, 1, 100)

    X, Y = np.meshgrid(a, b)
    Z = np.vectorize(f)(X, Y)
    ax = plt.axes()
    ax.contour(X, Y, Z, 20, cmap='RdGy')
    for theta_temp in theta_toplot:
        a = theta_temp[0]
        b = theta_temp[1]
        z = J(np.array([a,b]),x,y,m)
        ax.scatter(a, b, z, c='b', marker='o')
        plt.pause(2)
    ax.set_xlabel('theta_0')
    ax.set_ylabel('theta_1')
    ax.set_title('Eta: '+str(eta))
    plt.show()


theta = np.zeros(2)
threshold = 1e-10
eta = 0.01
def run(qpart):
    if(qpart=='1'):
        theta_learnt, theta_toplot = regression(np.zeros(2),threshold,eta,x,y)
        print(theta_learnt)
    elif(qpart=='2'):
        theta_learnt, theta_toplot = regression(np.zeros(2),threshold,eta,x,y)
        plot_graph(x,theta_learnt)
    elif(qpart=='3'):
        plot_mesh(threshold,eta,x,y)
    elif(qpart=='4'):
        plot_contour(threshold,eta,x,y)
    elif(qpart=='5'):
        # print("Plotting contour for eta = 0.001")
        # plot_contour(threshold,0.001,x,y)
        # print("Plotting contour for eta = 0.025")
        # plot_contour(threshold,0.025,x,y)
        print("Plotting contour for eta = 0.1")
        plot_contour(threshold,0.1,x,y)


run(sys.argv[3])