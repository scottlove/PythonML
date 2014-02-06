from unittest import TestCase
import unittest
import os.path
from MachineLearning import GensimCorpusCreate as gen
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARN)

def removeFile(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


class TestGenSim_Integration(TestCase):
    dictFile = "c:/tmp/deerwester.dict"
    mmFile = "c:/tmp/deerwester.mm"
    numTopics = 10
    lsiFile = "c:/tmp/model.lsi"
    ldaFile = "c:/tmp/model.lda"
    indexFileLSI = "c:/tmp/deerwesterLSI.index"
    indexFileLDA = "c:/tmp/deerwesterLDA.index"
    dictFile = "c:/tmp/deerwester.dict"

    documents = ["Human machine interface for lab abc computer applications",
                      "A survey of user opinion of computer system response time",
                      "The EPS user interface management system",
                      "System and human system engineering testing of EPS",
                      "Relation of user perceived response time to error measurement",
                      "The generation of random binary unordered trees",
                      "The intersection graph of paths in trees",
                      "Graph minors IV Widths of trees and well quasi ordering",
                      "Graph minors A survey"]
    testDoc = "Human computer interaction"

    def setUp(self):
        removeFile(self.dictFile)
        removeFile(self.mmFile)
        removeFile(self.lsiFile)
        removeFile(self.ldaFile)
        removeFile(self.indexFileLSI)
        removeFile(self.indexFileLDA)
        removeFile(self.dictFile)
        gen.CreateCorpusFromList(self.documents,self.dictFile,self.mmFile)

    def test_GenSimLSIIntegration(self):

        #Create and LSI transform
        corpus = gen.getCorpus(self.mmFile)
        dict = gen.getDictionary(self.dictFile)
        gen.createLSITransform(dict,corpus,self.numTopics,self.lsiFile)

        #Create the similarity matrix between all the docs using an LSITransform
        lsiTransform = gen.getLSITransform(self.lsiFile)
        gen.createSimilarityMatrix(lsiTransform,corpus,self.indexFileLSI)

        #Check for similarity of doc to corpus
        #first change doc into vector
        dict = gen.getDictionary(self.dictFile)
        docVector = gen.docToVec(self.testDoc,dict)

        #Check similarity using LSI generated indexFile
        simMatrix = gen.getSimilarityMatrix(self.indexFileLSI)
        sim = gen.getSimilaritiy(docVector,lsiTransform,simMatrix)
        sim = sorted(enumerate(sim), key=lambda item: -item[1])
        self.assertEquals(sim[0][0],0)
        print("similarity to docs using LSI")
        print list(enumerate(sim))





    def test_GenSimLDAIntegration(self):

        #Create and LSI and LDA transform
        corpus = gen.getCorpus(self.mmFile)
        dict = gen.getDictionary(self.dictFile)
        gen.createLDATransform(dict,corpus,self.numTopics,self.ldaFile)

        #Create the similarity matrix between all the docs using an LDATransform
        ldaTransform = gen.getLDATransform(self.ldaFile)
        gen.createSimilarityMatrix(ldaTransform,corpus,self.indexFileLDA)

        #Check for similarity of doc
        #first change doc into vector
        dict = gen.getDictionary(self.dictFile)
        docVector = gen.docToVec(self.testDoc,dict)

        #Check similarity using LDA generated indexFile
        simMatrix = gen.getSimilarityMatrix(self.indexFileLDA)
        sim = gen.getSimilaritiy(docVector,ldaTransform,simMatrix)
        sim = sorted(enumerate(sim), key=lambda item: -item[1])
        self.assertEquals(sim[0][0],0)
        print("similarity to docs using LDA")
        print list(enumerate(sim))



if __name__ == '__main__':
    unittest.main()


__author__ = 'scotlov'
