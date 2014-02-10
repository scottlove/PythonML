import gensim.corpora as corpora
import gensim.models as models
import gensim.similarities as sim

MLCOMP_DIR = "C:/Dev/Datasets/ap/"



corpus = corpora.BleiCorpus(MLCOMP_DIR +'ap.dat',MLCOMP_DIR +'vocab.txt')
#build a tiopic model
model = models.ldamodel.LdaModel(corpus,num_topics=100,id2word=corpus.id2word)

topics = [model[c] for c in corpus]
print (topics[0])

