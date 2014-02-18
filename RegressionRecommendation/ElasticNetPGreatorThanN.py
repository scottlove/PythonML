from sklearn.datasets import load_boston
from sklearn.linear_model import ElasticNetCV
import Regression as r
from sklearn.datasets import load_svmlight_file



data,target = load_svmlight_file
x = boston.data
y = boston.target

#ElasticNetCV creates subfolds and set alfpha internally
lr = ElasticNetCV(fit_intercept=True)

r.LinearRegression_noCrossFit(x,y,lr)
r.CrossValidate_LinearRegression(x,y,lr)
