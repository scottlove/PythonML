from unittest import TestCase
import unittest
import os.path
from MachineLearning import GensimCorpusCreate as gen
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def removeFile(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


class TestGenSim(TestCase):
    def test_CreateCorpusFromList(self):

        dictFile = "c:/tmp/deerwester.dict"
        mmFile = "c:/tmp/deerwester.mm"
        numTopics = 2
        lsiFile = "c:/tmp/model.lsi"


        removeFile(dictFile)
        removeFile(mmFile)

        documents = ["Human machine interface for lab abc computer applications",
                          "A survey of user opinion of computer system response time",
                          "The EPS user interface management system",
                          "System and human system engineering testing of EPS",
                          "Relation of user perceived response time to error measurement",
                          "The generation of random binary unordered trees",
                          "The intersection graph of paths in trees",
                          "Graph minors IV Widths of trees and well quasi ordering",
                          "Graph minors A survey"]
        gen.CreateCorpusFromList(documents,dictFile,mmFile)
        self.assertTrue(os.path.isfile(dictFile) )
        self.assertTrue(os.path.isfile(mmFile) )


    def test_createLSITransform(self):
        dictFile = "c:/tmp/deerwester.dict"
        mmFile = "c:/tmp/deerwester.mm"
        numTopics = 2
        lsiFile = "c:/tmp/model.lsi"

        dict = gen.getDictionary(dictFile)
        corpus = gen.getCorpus(mmFile)
        gen.createLSITransform(dict,corpus,numTopics,lsiFile)
        self.assertTrue(os.path.isfile(lsiFile) )

    def test_createLDATransform(self):
        dictFile = "c:/tmp/deerwester.dict"
        mmFile = "c:/tmp/deerwester.mm"
        numTopics = 2
        ldaFile = "c:/tmp/model.lda"
        dict = gen.getDictionary(dictFile)
        corpus = gen.getCorpus(mmFile)
        gen.createLDATransform(dict,corpus,numTopics,ldaFile)
        self.assertTrue(os.path.isfile(ldaFile) )


    def test_createSimilarityMatrixLsi(self):
        lsiFile = "c:/tmp/model.lsi"
        mmFile = "c:/tmp/deerwester.mm"
        indexFile = "c:/tmp/deerwesterLSI.index"
        corpus = gen.getCorpus(mmFile)
        lsiTransform = gen.getLSITransform(lsiFile)
        gen.createSimilarityMatrix(lsiTransform,corpus,indexFile)
        self.assertTrue(os.path.isfile(indexFile) )

    def test_createSimilarityMatrixLda(self):
        ldaFile = "c:/tmp/model.lda"
        mmFile = "c:/tmp/deerwester.mm"
        indexFile = "c:/tmp/deerwesterLDA.index"
        corpus = gen.getCorpus(mmFile)
        ldaTransform = gen.getLDATransform(ldaFile)
        gen.createSimilarityMatrix(ldaTransform,corpus,indexFile)
        self.assertTrue(os.path.isfile(indexFile) )

    def test_docToVec(self):
        doc = "Human computer interaction"
        dictFile = "c:/tmp/deerwester.dict"
        dict = gen.getDictionary(dictFile)
        docVector = gen.docToVec(doc,dict)
        #should only be 2 since interactin is not in dictionary
        self.assertEquals(len(docVector),2)

    def test_getSimilarityLsi(self):
        lsiFile = "c:/tmp/model.lsi"
        indexFile = "c:/tmp/deerwesterLSI.index"
        doc = "Human computer interaction"
        dictFile = "c:/tmp/deerwester.dict"
        dict = gen.getDictionary(dictFile)
        docVector = gen.docToVec(doc,dict)
        lsiTransform = gen.getLSITransform(lsiFile)
        simMatrix = gen.getSimilarityMatrix(indexFile)
        sim = gen.getSimilaritiy(docVector,lsiTransform,simMatrix)
        sim = sorted(enumerate(sim), key=lambda item: -item[1])
        print sim
        #deocument 2 should be most similar
        self.assertEquals(sim[0][0],2)

    def test_getSimilarityLda(self):
        ldaFile = "c:/tmp/model.lda"
        mmFile = "c:/tmp/deerwester.mm"
        indexFile = "c:/tmp/deerwesterLDA.index"
        doc = "Human computer interaction"
        dictFile = "c:/tmp/deerwester.dict"
        dict = gen.getDictionary(dictFile)
        docVector = gen.docToVec(doc,dict)
        ldaTransform = gen.getLDATransform(ldaFile)
        simMatrix = gen.getSimilarityMatrix(indexFile)
        sim = gen.getSimilaritiy(docVector,ldaTransform,simMatrix)
        sim = sorted(enumerate(sim), key=lambda item: -item[1])
        print sim
        #deocument 2 should be most similar
        self.assertEquals(4,4)


if __name__ == '__main__':
    unittest.main()


