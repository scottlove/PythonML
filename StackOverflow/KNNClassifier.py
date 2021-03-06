import sklearn.neighbors as n
import numpy as np
import CreateClassificationVectors as cc
from sklearn.cross_validation import KFold
try:
    import ujson as json  # UltraJSON if available
except:
    import json



X,Y = cc.get_XY_vectors()
knn = n.KNeighborsClassifier()
knn.fit(X,Y)

scores = []
cv = KFold(n=len(X), k=10, indices=True)
for train,test in cv:
    X_train, Y_train = X[train],Y[train]
    X_test, Y_test = X[test],Y[test]
    clf = n.KNeighborsClassifier()
    clf.fit(X_train,Y_train)
    scores.append(clf.score(X_test,Y_test))


print("Mean(scores)=%.5f\tStddev(scores)=%.5f"%(np.mean(scores),np.std(scores)))