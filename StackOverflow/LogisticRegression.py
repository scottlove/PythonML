
import CreateClassificationVectors as cc
import Measure
from sklearn.linear_model import LogisticRegression as lr

from sklearn.cross_validation import KFold
try:
    import ujson as json  # UltraJSON if available
except:
    import json



X,Y = cc.get_XY_vectors()

# precision, recall, thresholds = precision_recall_curve()
# thresholds = np.hstack([0],thresholds[medium])


for C in [0.1]: #[0.01, 0.1, 1.0, 10.0]:
    name = "LogReg C=%.2f" % C
    Measure.bias_variance_analysis(lr, {'penalty':'l2', 'C':C}, name,X,Y)
    Measure.measure(lr, {'penalty': 'l2', 'C': C},name,X,Y , plot=True)









