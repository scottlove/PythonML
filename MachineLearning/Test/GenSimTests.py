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
    indexFile = "c:/tmp/deerwesterLSI.index"
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

    def setUp(self):
        removeFile(self.dictFile)
        removeFile(self.mmFile)
        removeFile(self.lsiFile)
        removeFile(self.ldaFile)
        removeFile(self.indexFile)
        removeFile(self.dictFile)
        gen.CreateCorpusFromList(self.documents,self.dictFile,self.mmFile)
        self.createLSITransform()
        self.createLDATransform()
        self.createSimilarityMatrixLsi()
        self.createSimilarityMatrixLda()


    def createLSITransform(self):

        dict = gen.getDictionary(self.dictFile)
        corpus = gen.getCorpus(self.mmFile)
        print corpus
        gen.createLSITransform(dict,corpus,self.numTopics,self.lsiFile)
        self.assertTrue(os.path.isfile(self.lsiFile) )

    def createLDATransform(self):

        dict = gen.getDictionary(self.dictFile)
        corpus = gen.getCorpus(self.mmFile)
        gen.createLDATransform(dict,corpus,self.numTopics,self.ldaFile)
        self.assertTrue(os.path.isfile(self.ldaFile) )


    def createSimilarityMatrixLsi(self):

        corpus = gen.getCorpus(self.mmFile)
        lsiTransform = gen.getLSITransform(self.lsiFile)
        gen.createSimilarityMatrix(lsiTransform,corpus,self.indexFile)
        self.assertTrue(os.path.isfile(self.indexFile) )

    def createSimilarityMatrixLda(self):

        corpus = gen.getCorpus(self.mmFile)
        ldaTransform = gen.getLDATransform(self.ldaFile)
        gen.createSimilarityMatrix(ldaTransform,corpus,self.indexFile)
        self.assertTrue(os.path.isfile(self.indexFile) )

    def test_docToVec(self):
        doc = "Human computer interaction"

        dict = gen.getDictionary(self.dictFile)
        docVector = gen.docToVec(doc,dict)
        #should only be 2 since interactin is not in dictionary
        self.assertEquals(len(docVector),2)

    def test_getSimilarityLsi(self):

        doc = "Human computer interaction"

        dict = gen.getDictionary(self.dictFile)
        docVector = gen.docToVec(doc,dict)
        lsiTransform = gen.getLSITransform(self.lsiFile)
        simMatrix = gen.getSimilarityMatrix(self.indexFile)
        sim = gen.getSimilaritiy(docVector,lsiTransform,simMatrix)
        sim = sorted(enumerate(sim), key=lambda item: -item[1])
        #deocument 2 should be most similar
#        self.assertEquals(sim[0][0],0)
        print("similarity to docs using LSI")
        print list(enumerate(sim))

    def test_getSimilarityLda(self):

        doc = "Human computer interaction"

        dict = gen.getDictionary(self.dictFile)
        docVector = gen.docToVec(doc,dict)
        ldaTransform = gen.getLDATransform(self.ldaFile)
        simMatrix = gen.getSimilarityMatrix(self.indexFile)
        sim = gen.getSimilaritiy(docVector,ldaTransform,simMatrix)
        sim = sorted(enumerate(sim), key=lambda item: -item[1])
        #deocument 2 should be most similar
#        self.assertEquals(4,4)
        print("similarity to docs using LDA")
        print list(enumerate(sim))


if __name__ == '__main__':
    unittest.main()


__author__ = 'scotlov'
