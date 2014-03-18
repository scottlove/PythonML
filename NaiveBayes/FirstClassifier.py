import utils as u
import numpy as np

from sklearn.metrics import precision_recall_curve, auc
from sklearn.cross_validation import ShuffleSplit
import gridSearchModel
import Models




# This is first basic niave_bayes classifier for tweets
# process is as follows:
#     1) uploaded test data using provided load_sanders_data
#     2) determine best modes fit using gridSearchModel (this takes about hour).  Once you run this
#        populate get_best_model with these params
#     3) to train a model for scenarion (such as identifying tweets with and without sentiment)
#         a) adjust tweet labels to classes you interest in
#             example: in sentiment case we are having two classes positive and negative tweets get 1, others 0
#         b)create a pipeline to proccess the data.  A pipeline
#           sequentially applies a list of transforms, estimator must be last item
#             The pipeline we are using has a TfidfVectorizer followed by a MultinomialNB classifier.
#             TfidfVectorizer:
#                 Converts a collection of raw documents to a matrix of TF-IDF features. This is done
#                 internally by tokenizing the document and applying Term Frequency Inverse Document Frequency
#                 Normalization.  The goal of using tf-idf instead of the raw frequencies of occurrence of a token in
#                 a given document is to scale down the impact of tokens that occur very frequently in a given corpus
#                 and that are hence empirically less informative than features that occur in a small
#                 fraction of the training corpus.
#                 -preprocessor is run first, in case cleaning emoticons and abreviations
#            c) Then train the model.




def train_model(clf_factory,X,Y,name,plot=False):
    #setting random_state to get deterministic behaviour
    cv = ShuffleSplit(n=len(X), n_iter=10, test_size=0.3,indices=True,random_state=0)
    scores = []
    pr_scores =[]
    precisions, recalls, thresholds = [], [], []
    for train,test in cv:
        X_train,y_train = X[train],Y[train]
        X_test,y_test = X[test],Y[test]
        clf = clf_factory()
        clf.fit(X_train,y_train)
        train_score= clf.score(X_train,y_train)
        test_score = clf.score(X_test,y_test)
        scores.append(test_score)
        #clf.predict_prob returns the probability for class for entry in X_test
        proba = clf.predict_proba(X_test)

        #precision is the ability of the classifier not to label as positive  a sample that is negative
        #recall is teh ability to find all the positive samples
        precision,recall,pr_thresholds = precision_recall_curve(y_test,proba[:,1])
        pr_scores.append(auc(recall,precision))
        precisions.append(precision)
        recalls.append(recall)
        thresholds.append(pr_thresholds)

    if plot:
        scores_to_sort = pr_scores
        phase= "02"
        median = np.argsort(scores_to_sort)[len(scores_to_sort)/2]
        u.plot_pr(pr_scores[median],name,phase,precisions[median],recalls[median],label=name)

    summary = (np.mean(scores),np.std(scores),np.mean(pr_scores),np.std(pr_scores))

    print ("%.3f\t%.3f\t%.3f\t%.3f"%summary)



def runJustPosandNeg(X,Y):
    classes = np.unique(Y)
    for c in classes:
            print("#%s: %i" % (c, sum(Y==c)))

    #for initial pass, just using positive or negative tweets
    pos_neg_idx = np.logical_or(Y=="positive",Y=="negative")
    X=X[pos_neg_idx]
    Y=Y[pos_neg_idx]
    #update Y to have 0 for neg, 1 for pos
    Y= Y=="positive"
    train_model(Models.create_ngram_model,X,Y,"posVsNeg",True)

def sentimentAndNoSentiment(X,Y):
    #Y now contains 1 for tweets that were positive or negative
    #and 0 for neutral or irrelevant
    Y= u.tweak_labels(Y,["positive","negative"])
    classes = np.unique(Y)
    for c in classes:
            print("#%s: %i" % (c, sum(Y==c)))
    train_model(Models.get_best_model,X,Y,"sentimentVsNoSentiment",True)

def posVsRest(X,Y):
    #Y now contains 1 for tweets that were positive
    #and 0 for negative, neutral or irrelevant
    Y= u.tweak_labels(Y,["positive"])
    classes = np.unique(Y)
    for c in classes:
            print("#%s: %i" % (c, sum(Y==c)))
    train_model(Models.create_ngram_model,X,Y,"posVsRest",True)

def findBestEstimator(X,Y):
    best_clf = gridSearchModel.grid_search_model(Models.create_ngram_model,X,Y)

X,Y = u.load_sanders_data()
runJustPosandNeg(X,Y)
#sentimentAndNoSentiment(X,Y)
#posVsRest(X,Y)

#find best estimator for sentiment vs no sentiment
#Y= u.tweak_labels(Y,["positive","negative"])
#findBestEstimator(X,Y)
