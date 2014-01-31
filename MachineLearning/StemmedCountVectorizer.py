import sklearn.feature_extraction.text as sk
import nltk.stem

english_stemmer = nltk.stem.SnowballStemmer('english')

#Stemmer reduces words to basic stem
class StemmedCountVectorizer(sk.TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))


