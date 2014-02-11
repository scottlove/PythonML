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

    #fixed the link match which was not working.
    code_match = re.compile('<pre>(.*?)</pre>',re.MULTILINE|re.DOTALL)
    #link_match = re.compile('<a href="http://.*?".*?>(.*?) </a>',re.MULTILINE|re.DOTALL)
    link_match = re.compile('http(.*?)',re.MULTILINE|re.DOTALL)
    #sample just using number of links as the feature
    link_count_in_code = 0

    #Count links in code to later subract them
    for match_str in code_match.findall(s):
        link_count_in_code += len (link_match.findall(match_str))

    count = []
    count.append(len(link_match.findall(s)) - link_count_in_code)
    return count
    #return len(link_match.findall(s)) - link_count_in_code


def get_answers_list(meta):

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
                continue
        except:
            continue
    return all_answers

def get_XY_vectors():
    meta, id_to_idx, idx_to_id = utils.load_meta(chosen_meta)
    all_answers = get_answers_list(meta)

    Y = np.asarray([meta[aid]['Score'] > 0 for aid in all_answers])
    x = [extract_features_from_body(text) for post_id,text in utils.fetch_posts(chosen) if post_id in all_answers]
    X = np.asarray(x)
    return X,Y
