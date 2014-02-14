from sklearn.datasets import load_boston
from matplotlib import pyplot as plt
import numpy as np

def plot_boston(x,y,slope,c=0):
    plt.scatter(x,y, color='r')
    plt.xlabel("RM")
    plt.ylabel("House Price")
    plt.plot([0,x.max()+1],[0,slope*(x.max()+1)]-c, '-', lw=4)
    plt.show()

boston = load_boston()

#convert to multiple dimensions first dimension is example, second is attributes
#in this case there is only examples and attribute is number of rooms [n,1] shape
x = boston.data[:,5]

#adding the [v,1] is the bias
x = np.array([[v,1] for v in x])
y = boston.target
slope,bias,_,_ = np.linalg.lstsq(x,y)


plot_boston(boston.data[:,5],boston.target,slope[0])
