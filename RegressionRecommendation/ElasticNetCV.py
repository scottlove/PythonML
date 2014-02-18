import numpy as np
from scipy import sparse
from sklearn.linear_model import LassoCV, RidgeCV, ElasticNetCV
from sklearn.cross_validation import KFold

DATA_DIR = r"C:/Dev/Datasets/Movies/ml-100k/"


def movie_norm(xc):
    xc = xc.copy().toarray()
    x1 = np.array([xi[xi > 0].mean() for xi in xc])
    x1 = np.nan_to_num(x1)

    for i in range(xc.shape[0]):
        xc[i] -= (xc[i] > 0) * x1[i]
    return xc, x1

def learn_for(i,sparceArray):
    u = sparceArray[i] #isolate this user
    #Numpy tricks: array converts back from sparce
    #ravel conversts to simple one dimensional
    #array of indices that that user selected movie
    ps, = np.where(u.toarray().ravel() > 0)

    #Build an array with indices [0..N] except i
    us = np.delete(np.arange(sparceArray.shape[0]), i)
    x = sparceArray[us][:,ps].T
    y = u.data
    err = 0
    eb = 0
    kf = KFold(len(y), n_folds=4)
    for train,test in kf:
        xc,x1 = movie_norm(x[train])
        reg.fit(xc, y[train]-x1)

        xc,x1 = movie_norm(x[test])
        p = np.array([reg.predict(xi) for xi in  xc]).ravel()
        e = (p+x1)-y[test]
        err += np.sum(e*e)
        eb += np.sum( (y[train].mean() - y[test])**2 )
    return np.sqrt(err/float(len(y))), np.sqrt(eb/float(len(y)))

data = np.array([[int(tok) for tok in line.split('\t')[:3]] for line in open(DATA_DIR + 'u.data')])
ij = data[:,:2]
ij -= 1 # original data is in 1-based system
values = data[:,2]

#ij.T transposes array. Changes 10K by 2, to 2 by 10000k. 1st row is UserID
#second is Item ID. In Sparce matrix input UserID is the row, ItemID is the column.
#Most entries are empty, so create a sparce matrix.
reviews = sparse.csc_matrix((values,ij.T)).astype(float)

reg = ElasticNetCV(fit_intercept=True, alphas=[0.0125, 0.025,0.05,.125,.25,.5,1.,2.,4.])

whole_data = []
for i in range(reviews.shape[0]):
    s = learn_for(i,reviews)
    print(s[0] < s[1])
    print(s)
    whole_data.append(s)
