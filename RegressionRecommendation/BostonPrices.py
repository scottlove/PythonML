from sklearn.datasets import load_boston
from matplotlib import pyplot as plt
import numpy as np

def plot_boston(x,y,slope,c=0):
    plt.scatter(x,y, color='r')
    plt.xlabel("RM")
    plt.ylabel("House Price")
#    plt.plot([0,x.max()+1],[0,slope*(y.max()+1)], '-', lw=4)

    xmin = x.min()
    xmax = x.max()
    #plot formula is [x1,x2],[y1,y2]
    plt.plot([xmin,xmax],[slope*xmin + bias, slope*xmax + bias], '-', lw=4)
    plt.show()

boston = load_boston()

#convert to multiple dimensions first dimension is example, second is attributes
#in this case there is only examples and attribute is number of rooms [n,1] shape
x = boston.data[:,5]

#adding the [v,1] is the bias
x = np.array([[v,1] for v in x])
y = boston.target
(slope,bias),res,_,_ = np.linalg.lstsq(x,y)

#This is the root mean squared error
#most data is most 2 std from mean, double rmse to get
#confidence.  6.6 rmse corresponds to 13.2k difference in price
rmse = np.sqrt(res[0]/len(x))
print rmse




#plot_boston(boston.data[:,5],boston.target,slope,bias)
