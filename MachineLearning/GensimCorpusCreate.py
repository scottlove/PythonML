
import gensim.corpora as co
import gensim.models as mo
import gensim.similarities as si

def getDictionary(DictFilename):
    return co.Dictionary.load(DictFilename)


def getCorpus(CorpusFilename):
    return co.MmCorpus(CorpusFilename)

def getLSITransform(lsiFilename):
    return mo.LsiModel.load(lsiFilename)

def getLDATransform(ldaFilename):
    return mo.LdaModel.load(ldaFilename)

def getSimilarityMatrix(matrixFilename):
    return si.MatrixSimilarity.load(matrixFilename)

def docToVec(doc,dictionary):
    #cnvert single document to vector
    stoplist = set('for a of the and to in'.split())
    text = [word for word in doc.lower().split() if word not in stoplist]
    return dictionary.doc2bow(doc.lower().split())


def CreateCorpusFromList(documents,DictFilename,CorpusFilename):
    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]
    # remove words that appear only once
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
             for text in texts]
    dictionary = co.Dictionary(texts)
    dictionary.save(DictFilename) # store the dictionary, for future reference
    corpus = [dictionary.doc2bow(text) for text in texts]
    co.MmCorpus.serialize(CorpusFilename, corpus) # store to disk, for later use

def createLSITransform(dictionary,corpus,numTopics,outFile):
     tfidf = mo.TfidfModel(corpus)
     #do the actual transform
     corpus_tfidf = tfidf[corpus]
     #create lsi transform ojbect
     lsi = mo.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=numTopics)
     lsi.save(outFile)

def createLDATransform(dictionary,bow_corpus,numTopics,outFile):
     #create lsi transform ojbect
     lda = mo.LdaModel(bow_corpus, id2word=dictionary,num_topics=numTopics)
     lda.save(outFile)

def createSimilarityMatrix(transform,corpus,outfile):
    #in memory creation of similarity Matrix
    index = si.MatrixSimilarity(transform[corpus])
    index.save(outfile)


def getSimilaritiy(docVector,lsi,similarityMatrix):
    vec_lsi = lsi[docVector] # convert the query to LSI space
    return similarityMatrix[vec_lsi] # perform a similarity query against the corpus







