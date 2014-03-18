
import numpy as np

from sklearn.base import BaseEstimator
import json

from utils import load_sent_word_net
import nltk


#vectorizer that assigns sentiments based
#on SentiWordNet. It assigns positive or negative to most words
#inherites from base estimator
class LinguisticVectorizer(BaseEstimator):
    def get_feature_names(self):
        return np.array(['sent_neut', 'sent_pos', 'sent_neg',
         'nouns', 'adjectives', 'verbs', 'adverbs',
         'allcaps', 'exclamation', 'question'])

    def fit(self, documents, y=None):
        #not implementing so just return self
        return self

    def _get_sentiments(self, d):

        sent_word_net = load_sent_word_net()

        poscache_filename = "poscache.json"
        try:
            poscache = json.load(open(poscache_filename, "r"))
        except IOError:
            poscache = {}
        # http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        #import pdb;pdb.set_trace()
        sent = tuple(nltk.word_tokenize(d))
        #pos_tag tags tokens with part of speech (noun, verb etc)
        if poscache is not None:
            if d in poscache:
                tagged = poscache[d]
            else:
                poscache[d] = tagged = nltk.pos_tag(sent)
        else:
            tagged = nltk.pos_tag(sent)

        pos_vals = []
        neg_vals = []

        nouns = 0.
        adjectives = 0.
        verbs = 0.
        adverbs = 0.

        for w,t in tagged:
            p, n = 0,0
            sent_pos_type = None
            if t.startswith("NN"):
                sent_pos_type = "n"
                nouns += 1
            elif t.startswith("JJ"):
                sent_pos_type = "a"
                adjectives += 1
            elif t.startswith("VB"):
                sent_pos_type = "v"
                verbs += 1
            elif t.startswith("RB"):
                sent_pos_type = "r"
                adverbs += 1

            if sent_pos_type is not None:
                sent_word = "%s/%s"%(sent_pos_type, w)

                if sent_word in sent_word_net:
                    p,n = sent_word_net[sent_word]

            pos_vals.append(p)
            neg_vals.append(n)

        l = len(sent)
        avg_pos_val = np.mean(pos_vals)
        avg_neg_val = np.mean(neg_vals)
        #import pdb;pdb.set_trace()
        return [1-avg_pos_val-avg_neg_val, avg_pos_val, avg_neg_val,
                nouns/l, adjectives/l, verbs/l, adverbs/l]


    def transform(self, documents):
        obj_val, pos_val, neg_val, nouns, adjectives, verbs, adverbs = np.array([self._get_sentiments(d) for d in documents]).T

        allcaps = []
        exclamation = []
        question = []

        for d in documents:
            allcaps.append(np.sum([t.isupper() for t in d.split() if len(t)>2]))

            exclamation.append(d.count("!"))
            question.append(d.count("?"))

        result = np.array([obj_val, pos_val, neg_val, nouns, adjectives, verbs, adverbs, allcaps,
            exclamation, question]).T

        return result
