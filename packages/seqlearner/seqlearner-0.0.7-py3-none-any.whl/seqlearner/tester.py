import warnings

import numpy as np

from .MultiTaskLearner import MultiTaskLearner

warnings.filterwarnings("ignore")
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

np.seterr(divide='ignore', invalid='ignore')
mtl = MultiTaskLearner("../data/labeled.xlsx", "../data/unlabeled.xlsx")
# print(mtl.learner(3, 5, "load_embedding", "label_spreading", file="../data/protVec_100d_3grams.csv", func = "weighted_sum"))
# print(mtl.learner(3, 5, "load_embedding", "naive_bayes", file="../data/protVec_100d_3grams.csv", func="weighted_average"))
# print(mtl.learner(3, 5, "load_embedding", "label_propagation", file="../data/protVec_100d_3grams.csv", func="weighted_sum"))
# print(mtl.learner(3, 5, "load_embedding", "pseudo_labeling", file="../data/protVec_100d_3grams.csv", func="weighted_average", alg=svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
#     decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
#     max_iter=-1, probability=False, random_state=None, shrinking=True,
#     tol=0.001, verbose=False)))

# print(mtl.learner(3, 5, "load_embedding", "pseudo_labeling", file="../data/protVec_100d_3grams.csv", func="weighted_average", alg=svm.NuSVC(nu=0.8)))
# print(mtl.learner(3, 5, "load_embedding", "pseudo_labeling", file="../data/protVec_100d_3grams.csv", func="weighted_average", alg=AdaBoostClassifier()))
# print(mtl.learner(3, 5, "load_embedding", "pseudo_labeling", file="../data/protVec_100d_3grams.csv", func="weighted_average", alg=LinearDiscriminantAnalysis()))
print(
    mtl.learner(3, 5, "freq2vec", "label_spreading", func="sum", emb_dim=20,
                gamma=0.1, epochs=10))

### tested:
# label_spreading : passed
# label_propagation : passed with warning --> convergence warning
# naive_bayes : passed
# bayesian_classifier : failed --> blank!!!
# pseudo_labeing (SVM) : passed --> too slow
# pseudo_labeing (NuSVM) : failed --> specified nu is infeasible
# pseudo_labeing (KNN) : failed --> no score method!
# pseudo_labeling (AdaBoostClassifier) : passed
# pseudo_labeling (LinearDiscriminantAnalysis) : passed
#


# import pandas as pd
#
# from code.Embedding import Embedding
#
# sequence = pd.read_excel("../data/labeled.xlsx")['sequence']
# sequence += pd.read_excel("../data/unlabeled.xlsx")['sequence']
# test_embed = Embedding(sequences=sequence, word_length=3)
# skipgram = test_embed.sent2vec(lr=0.001)
