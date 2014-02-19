import numpy as np
from scipy import sparse
from sklearn.linear_model import LassoCV, RidgeCV, ElasticNetCV
from sklearn.cross_validation import KFold
from load_ml100k import load





def movie_norm(xc):
    #XC has all the ratings for all users except test user
    xc = xc.copy().toarray()

    #convert x1 to 1 dimensional array for average of all reviews each user made
    x1 = np.array([xi[xi > 0].mean() for xi in xc])
    x1 = np.nan_to_num(x1)

    for i in range(xc.shape[0]):
        #normalize to 0 = average by subtracting average review score from each review
        xc[i] -= (xc[i] > 0) * x1[i]
    return xc, x1

#reviews is a sparce CSC array
def learn_for(i,reviews):
    u = reviews[i] #isolate this user
    #Numpy tricks: array converts back from sparce
    #ravel conversts to simple one dimensional
    #array of indices that that user selected movie
    ps, = np.where(u.toarray().ravel() > 0)

    #Build an array with indices [0..N] except i
    us = np.delete(np.arange(reviews.shape[0]), i)
    x = reviews[us][:,ps].T
    y = u.data
    err = 0
    eb = 0
    kf = KFold(len(y), n_folds=4)
    for train,test in kf:
        xc,x1 = movie_norm(x[train])
        #subtract the mean review score from y[train] movie rating
        #so x and y are normalized to same value when fitting
        reg.fit(xc, y[train]-x1)

        #Now check the fit using the x[test] data
        xc,x1 = movie_norm(x[test])
        p = np.array([reg.predict(xi) for xi in  xc]).ravel()
        e = (p+x1)-y[test]
        err += np.sum(e*e)
        eb += np.sum( (y[train].mean() - y[test])**2 )
    return np.sqrt(err/float(len(y))), np.sqrt(eb/float(len(y)))


reviews = load()
reg = ElasticNetCV(fit_intercept=True, alphas=[0.0125, 0.025,0.05,.125,.25,.5,1.,2.,4.])

whole_data = []
for i in range(reviews.shape[0]):
    s = learn_for(i,reviews)
    print(s[0] < s[1])
    print(s)
    whole_data.append(s)
