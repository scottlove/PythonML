import sklearn.datasets
import StemmedCountVectorizer as sc
import sklearn.cluster as skc
import scipy as sp

def dist_norm(v1,v2):
    #normalized vector is a unit vector
    v1_normalized = v1/sp.linalg.norm(v1.toarray())
    v2_normalized = v2/sp.linalg.norm(v2.toarray())
    delta = v1_normalized -v2_normalized
    return sp.linalg.norm(delta.toarray())


MLCOMP_DIR = "C:/Dev/Datasets/dataset-379-20news-18828_GWNMC"
groups = [
    'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
    'comp.sys.ma c.hardware', 'comp.windows.x', 'sci.space']
dataset = sklearn.datasets.load_mlcomp("20news-18828", "train",
                                       mlcomp_root=MLCOMP_DIR,
                                       categories=groups)
test_data = sklearn.datasets.load_mlcomp("20news-18828", "test",
                                       mlcomp_root=MLCOMP_DIR,
                                       categories=groups)

#dataset.data list of posts
#print(dataset.data[0])
#print(dataset.data[1])
#print(dataset.data[2])

#create a vectorizor that ignores errors from bad data
#use our stemming vectorizor
vectorizor = sc.StemmedCountVectorizer(min_df=10, stop_words='english',charset_error='ignore')


vectorized = vectorizor.fit_transform(dataset.data)
num_samples, num_features = vectorized.shape
print("#sampes:%d, #features: %d" %(num_samples, num_features))

num_clusters = 50

km = skc.KMeans(n_clusters=num_clusters,init='random',n_init=1, verbose=0)


clustered = km.fit(vectorized)


new_post = \
    """Disk drive problems. Hi, I have a problem with my hard disk.
After 1 year it is working only sporadically now.
I tried to format it, but now it doesn't boot any more.
Any ideas? Thanks.
"""

print(new_post)
new_post_vec = vectorizor.transform([new_post])
new_post_label = km.predict(new_post_vec)[0]
similar_indices = (km.labels_==new_post_label).nonzero()[0]
#print (similar_indices)
similar = []
for i in similar_indices:
    dist = dist_norm(new_post_vec,vectorized[i])
    similar.append((dist,dataset.data[i]))

similar = sorted(similar)
print(len(similar))
print(similar[0])
print(similar[-1])


