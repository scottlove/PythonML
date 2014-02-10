
import os
import scipy as sp
import sys
import StemmedCountVectorizer as sc


def dist_raw(v1,v2):
    delta = v1-v2
    return sp.linalg.norm(delta.toarray())


def dist_norm(v1,v2):
    #normalized vector is a unit vector
    v1_normalized = v1/sp.linalg.norm(v1.toarray())
    v2_normalized = v2/sp.linalg.norm(v2.toarray())
    delta = v1_normalized -v2_normalized
    return sp.linalg.norm(delta.toarray())


def countWords():
    DIR = "C:/Dev/Building Machine Learning Systems with Python/1400OS_Code/1400OS_03_Codes/1400OS_03_Codes/data/toy"

    posts= [open(os.path.join(DIR,f)).read() for f in os.listdir(DIR)]
    #vectorizer = sk.CountVectorizer(min_df=1)
    #vectorizer = sk.CountVectorizer(min_df=1, stop_words='english')
    vectorizer = sc.StemmedCountVectorizer(min_df=1, stop_words='english')
    X_train= vectorizer.fit_transform(posts)
    num_samples,num_features = X_train.shape
    #print ("#samples: %d, #features: %d" % (num_samples, num_features))
    #print(vectorizer.get_feature_names())
    new_post = "imaging databases"
    new_post_vec = vectorizer.transform([new_post])
    # print(new_post_vec)
    # print(new_post_vec.toarray())

    #now calculate similarity of new post to teh old posts
    #this is unnormalized, not taking in account of duplicated words in sentence.
    best_doc = None
    best_dist = sys.maxint
    best_i = None
    for i in range(0, num_samples):
        post = posts[i]
        if(post == new_post):
            continue
        post_vec = X_train.getrow(i)

        #d = dist_raw(post_vec, new_post_vec)
        d = dist_norm(post_vec, new_post_vec)
        print"=== Post %i with dist=%.2f: %s"%(i,d,post)

        if d<best_dist:
            best_dist = d
            best_i = i

    print("Best post is %i with dist=%.2f" % (best_i,best_dist))



countWords()
