
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.naive_bayes import  MultinomialNB
import cleanTweets as cT
import LinguisticVectorizer as lv
from sklearn.pipeline import Pipeline, FeatureUnion

#use the parameters returned by gridSearchModel.py
def get_best_union_model():

    best_params = dict(all__tfidf__ngram_range=(1, 2),
                       all__tfidf__min_df=1,
                       all__tfidf__stop_words=None,
                       all__tfidf__smooth_idf=False,
                       all__tfidf__use_idf=False,
                       all__tfidf__sublinear_tf=True,
                       all__tfidf__binary=False,
                       clf__alpha=0.01,
                       )

    #best_clf = create_ngram_model(best_params)
    best_clf = create_union_model(best_params)
    return best_clf


def create_union_model(params=None):

    tfidf_ngrams = TfidfVectorizer(preprocessor=cT.preprocessor,
                                   analyzer="word")
    ling_stats = lv.LinguisticVectorizer()
    #Feature union evaluates estimators in parrallel and
    #combines output vectors
    all_features = FeatureUnion([('ling', ling_stats), ('tfidf', tfidf_ngrams)])
    #all_features = FeatureUnion([('tfidf', tfidf_ngrams)])
    #all_features = FeatureUnion([('ling', ling_stats)])
    clf = MultinomialNB()
    pipeline = Pipeline([('all', all_features), ('clf', clf)])

    if params:
        pipeline.set_params(**params)

    return pipeline



#use the parameters returned by gridSearchModel.py
def get_best_model():

    best_params = dict(vect__ngram_range=(1, 2),
                       vect__min_df=1,
                       vect__stop_words=None,
                       vect__smooth_idf=False,
                       vect__use_idf=False,
                       vect__sublinear_tf=True,
                       vect__binary=False,
                       clf__alpha=0.01,
                       )

    #best_clf = create_ngram_model(best_params)
    best_clf = create_ngram_model(best_params)
    return best_clf

def create_ngram_model(params=None):
    tfidf_ngrams = TfidfVectorizer(preprocessor=cT.preprocessor, ngram_range=(1,3),analyzer="word",binary=False)
    clf = MultinomialNB()
    #sequentially apply a list of transforms, estimator must be last item
    pipeline = Pipeline([('vect',tfidf_ngrams),('clf',clf)])
    if params:
        #update parameters opitimized with gridSearchModel
        pipeline.set_params(**params)

    return pipeline

