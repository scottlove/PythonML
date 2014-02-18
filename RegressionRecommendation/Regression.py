import numpy as np
from sklearn.cross_validation import KFold



def LinearRegression_noCrossFit(x,y,lm):
    #lm is the sklearn.linear model used ie: LinearRegression, ElasticNet
    lm.fit(x,y)
    #note map(function,iterable) applies function to every item in iterable
    #in this case it predicts value house value of x
    p = map(lm.predict,x)
    e = p-y
    total_error = np.sum(e*e) # sum of squares of errors

    #This is the root mean squared error
    #most data is most 2 std from mean, double rmse to get
    #confidence.  6.6 rmse corresponds to 13.2k difference in price
    rmse_train = np.sqrt(total_error/len(p))
    print('RMSE on training data: {}'.format(rmse_train))


def CrossValidate_LinearRegression(x,y,lm,n_folds=10,):
    #lm is the sklearn.linear model used ie: LinearRegression, ElasticNet
    kf = KFold(len(x),n_folds)
    err = 0;
    for train,test in kf:
        lm.fit(x[train],y[train])
        #note map(function,iterable) applies function to every item in iterable
        #in this case it predicts value house value of x
        p = map(lm.predict,x[test])
        e = p-y[test]
        err += np.sum(e*e)
    rmse_10cv = np.sqrt(err/len(x))
    print('RMSE on 10-fold CV: {}'.format(rmse_10cv))
