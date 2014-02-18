from sklearn.datasets import load_boston
from matplotlib import pyplot as plt
import Regression as r

from sklearn.linear_model import ElasticNet


def plot_boston(x,y,slope,c=0):
    plt.scatter(x,y, color='r')
    plt.xlabel("RM")
    plt.ylabel("House Price")
    #    plt.plot([0,x.max()+1],[0,slope*(y.max()+1)], '-', lw=4)

    xmin = x.min()
    xmax = x.max()
    #plot formula is [x1,x2],[y1,y2]
    plt.plot([xmin,xmax],[slope*xmin + c, slope*xmax + c], '-', lw=4)
    plt.show()






boston = load_boston()
x = boston.data
y = boston.target

#ElasticNet is penalized model combining L1 and L2 models (Lasso and Ridge)
#results in higher training error, but improved crossvalidation error
lr = ElasticNet(fit_intercept=True,alpha=0.5)

r.LinearRegression_noCrossFit(x,y,lr)
r.CrossValidate_LinearRegression(x,y,lr)

