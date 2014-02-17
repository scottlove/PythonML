from sklearn.cross_validation import ShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import f1_score


def grid_search_model(clf_factory, X, Y):

    #Use a shufflesplit for cross validation
    cv = ShuffleSplit(n=len(X), n_iter=10, test_size=0.3, indices=True, random_state=0)

    #The parameters we want to vary
    param_grid = dict(vect__ngram_range=[(1, 1), (1, 2), (1, 3)],
                      vect__min_df=[1, 2],
                      vect__stop_words=[None, "english"],
                      vect__smooth_idf=[False, True],
                      vect__use_idf=[False, True],
                      vect__sublinear_tf=[False, True],
                      vect__binary=[False, True],
                      clf__alpha=[0, 0.01, 0.05, 0.1, 0.5, 1],
                      )

    #f1_score is as an F-measure, which will be used to chose best estimator
    #F1 score is weighted average of the precision and recall
    grid_search = GridSearchCV(clf_factory(),
                               param_grid=param_grid,
                               cv=cv,
                               score_func=f1_score,
                               verbose=10)
    grid_search.fit(X, Y)
    clf = grid_search.best_estimator_
    print clf

    return clf
