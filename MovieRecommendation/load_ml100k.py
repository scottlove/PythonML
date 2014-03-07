import numpy as np
from scipy import sparse
DATA_DIR = r"C:/Dev/Datasets/Movies/ml-100k/"

def load():
    data = np.array([[int(tok) for tok in line.split('\t')[:3]] for line in open(DATA_DIR + 'u.data')])
    ij = data[:,:2]
    ij -= 1 # original data is in 1-based system
    values = data[:,2]
    reviews = sparse.csc_matrix((values,ij.T)).astype(float)
    return reviews