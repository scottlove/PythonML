from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
import numpy as np




#load learning data from sklearn
data = load_iris()
features = data['data']
feature_names = data['feature_names']
target = data['target']
labels = data['target_names'][target]


#get all the petal lengths for all flowers
plength = features[:,2]
#create true/false array for labels == setosa
is_setosa = (labels == 'setosa')
#get max/min length of setosa petals
max_setosa = plength[is_setosa].max()
min_setosa = plength[is_setosa].min()


#create a boolean array for measurements that are actually  virginica
virginica = (labels == 'virginica')
best_acc = -1.0
#b is the number of features - in this case 4
#features has 150 flowers measured, 4 measurements for each flower
b = xrange(features.shape[1])
for fi in b:
    #copy all the measurements for this measurement type (f1 is type 1-4)
    thresh = features[:,fi].copy()
    thresh.sort()

    for t in thresh:
        #create boolean array where true measured means value is greater than te
        pred = (features[:,fi] >t)
        #get the mean value 0 = false, true = 1. sum 1&0 and divide by 150
        acc = (pred == virginica).mean()
        if acc > best_acc:
            best_acc = acc
            best_fi = fi
            best_t = t

print (best_acc)
print (feature_names[best_fi])
print (best_t)