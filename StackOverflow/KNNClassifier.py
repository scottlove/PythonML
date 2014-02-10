import sklearn.neighbors as n
import numpy as np
import re
from data import chosen,chosen_meta,filtered,filtered_meta
from sklearn.cross_validation import KFold
try:
    import ujson as json  # UltraJSON if available
except:
    import json

import utils


def extract_features_from_body(s):
    #sample just using number of links as the feature
    link_count_in_code = 0

    #Count links in code to later subract them
    for match_str in code_match.findall(s):
        link_count_in_code += len (link_match.findall(match_str))

    count = []
    count.append(len(link_match.findall(s)) - link_count_in_code)
    return count
    #return len(link_match.findall(s)) - link_count_in_code


#fixed the link match which was not working.
code_match = re.compile('<pre>(.*?)</pre>',re.MULTILINE|re.DOTALL)
#link_match = re.compile('<a href="http://.*?".*?>(.*?) </a>',re.MULTILINE|re.DOTALL)
link_match = re.compile('http(.*?)',re.MULTILINE|re.DOTALL)



meta, id_to_idx, idx_to_id = utils.load_meta(chosen_meta)

temp = {}
#rewrote this to handle some bad data
all_answers = []
for q,v in meta.iteritems():
    try:
        key = q
        value = v['ParentId']
        try:
            if (value != -1):
                all_answers.append(q)
        except:
            print q
    except:
        print v


y = [meta[aid]['Score'] > 0 for aid in all_answers]
Y = np.asarray(y)
x = [extract_features_from_body(text) for post_id,text in utils.fetch_posts(chosen) if post_id in all_answers]
X = np.asarray(x)

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