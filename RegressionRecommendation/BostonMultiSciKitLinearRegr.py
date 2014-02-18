from sklearn.datasets import load_boston
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import Regression as r

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
lr = LinearRegression(fit_intercept=True)
r.LinearRegression_noCrossFit(x,y,lr)
r.CrossValidate_LinearRegression(x,y,lr)
#fit_intercept = True adds the bias term, similar to what was
#done in previous examples

