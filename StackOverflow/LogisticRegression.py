import sklearn.neighbors as n
import numpy as np
import CreateClassificationVectors as cc
from sklearn.linear_model import LogisticRegression as lr

from sklearn.cross_validation import KFold
try:
    import ujson as json  # UltraJSON if available
except:
    import json



X,Y = cc.get_XY_vectors()

# precision, recall, thresholds = precision_recall_curve()
# thresholds = np.hstack([0],thresholds[medium])



scores = []
cv = KFold(n=len(X), k=10, indices=True)
for train,test in cv:
    X_train, Y_train = X[train],Y[train]
    X_test, Y_test = X[test],Y[test]
    clf = lr(C=100)
    clf.fit(X_train,Y_train)
    scores.append(clf.score(X_test,Y_test))


print("Mean(scores)=%.5f\tStddev(scores)=%.5f"%(np.mean(scores),np.std(scores)))
