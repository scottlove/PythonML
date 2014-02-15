import time
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve, roc_curve, auc
from sklearn.cross_validation import KFold

from utils import plot_roc, plot_pr
from utils import plot_feat_importance
from utils import plot_roc, plot_pr
from utils import plot_feat_importance
from utils import load_meta
from utils import fetch_posts
from utils import plot_feat_hist
from utils import plot_bias_variance
from utils import plot_k_complexity


def measure(clf_class, parameters, name, qa_X, qa_Y,data_size=None, plot=False):

    feature_names = np.array((
    'NumTextTokens',
    'NumCodeLines',
    'LinkCount',
    'AvgSentLen',
    'AvgWordLen',
    'NumAllCaps',
    'NumExclams',
    'NumImages'
    ))

    classifying_answer = "good"
    avg_scores_summary = []
    start_time_clf = time.time()
    if data_size is None:
        X = qa_X
        Y = qa_Y
    else:
        X = qa_X[:data_size]
        Y = qa_Y[:data_size]

    cv = KFold(n=len(X), n_folds=10, indices=True)

    train_errors = []
    test_errors = []

    scores = []
    roc_scores = []
    fprs, tprs = [], []

    pr_scores = []
    precisions, recalls, thresholds = [], [], []

    for train, test in cv:
        X_train, y_train = X[train], Y[train]
        X_test, y_test = X[test], Y[test]

        clf = clf_class(**parameters)

        clf.fit(X_train, y_train)

        train_score = clf.score(X_train, y_train)
        test_score = clf.score(X_test, y_test)

        train_errors.append(1 - train_score)
        test_errors.append(1 - test_score)

        scores.append(test_score)
        proba = clf.predict_proba(X_test)

        label_idx = 1
        fpr, tpr, roc_thresholds = roc_curve(y_test, proba[:, label_idx])
        prb = proba[:, label_idx]
        prb1 = proba[0:]
        precision, recall, pr_thresholds = precision_recall_curve(
            y_test, proba[:, label_idx])

        roc_scores.append(auc(fpr, tpr))
        fprs.append(fpr)
        tprs.append(tpr)

        pr_scores.append(auc(recall, precision))
        precisions.append(precision)
        recalls.append(recall)
        thresholds.append(pr_thresholds)
        # print(classification_report(y_test, proba[:, label_idx] >
        #       0.63, target_names=['not accepted', 'accepted']))

    # get medium clone
    scores_to_sort = pr_scores  # roc_scores
    medium = np.argsort(scores_to_sort)[len(scores_to_sort) / 2]

    if plot:
        plot_roc(roc_scores[medium], name, fprs[medium], tprs[medium])
        plot_pr(pr_scores[medium], name, precisions[medium], recalls[medium], classifying_answer + " answers")

        if hasattr(clf, 'coef_'):
            plot_feat_importance(feature_names, clf, name)

    summary = (name,
               np.mean(scores), np.std(scores),
               np.mean(roc_scores), np.std(roc_scores),
               np.mean(pr_scores), np.std(pr_scores),
               time.time() - start_time_clf)
    print(summary)
    avg_scores_summary.append(summary)
    precisions = precisions[medium]
    recalls = recalls[medium]
    thresholds = np.hstack(([0], thresholds[medium]))
    idx80 = precisions >= 0.8
    p1 = precisions[idx80][0]
    p2 = thresholds[idx80][0]
    print("P=%.2f R=%.2f thresh=%.2f" % (precisions[idx80][0], recalls[
         idx80][0], thresholds[idx80][0]))

    mean_train = np.mean(train_errors)
    mean_test =np.mean(test_errors)

    return mean_train,mean_test ,avg_scores_summary

def bias_variance_analysis(clf_class, parameters, name,X,Y):
    data_sizes = np.arange(60, 2000, 4)

    train_errors = []
    test_errors = []

    for data_size in data_sizes:
        try:
            train_error, test_error,avg_sum = measure(clf_class, parameters, name, X,Y)
            train_errors.append(train_error)
            test_errors.append(test_error)
        except:
            print "data size error********************"
            print data_size

    plot_bias_variance(data_sizes, train_errors, test_errors, name, "Bias-Variance for '%s'" % name)