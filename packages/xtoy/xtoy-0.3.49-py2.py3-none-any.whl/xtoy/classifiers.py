# from sklearn.svm import SVC
import scipy
from sklearn import svm
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import Ridge, RidgeClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

from xtoy.utils import classification_or_regression


ridge_grid = {
    "clf__alpha": [
        0.00001,
        0.001,
        0.01,
        0.05,
        0.1,
        0.3,
        0.5,
        0.8,
        1.0,
        1.4,
        1.7,
        10,
        100,
        1000,
        10000,
        100000,
    ]
}
# normalize seems bugged at prediction time!

# ridge_grid = {'clf__alpha': [0.1, 1., 10.]}

ridge_classification = {"clf": RidgeClassifier, "grid": ridge_grid}
ridge_regression = {"clf": Ridge, "grid": ridge_grid}
# ridge_regression = {'clf': svm.SVR, 'grid': {
#     'clf__shrinking': [True, False],
#     'clf__C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
#     'clf__kernel': ['linear', 'poly', 'rbf', 'sigmoid']}}


rf_grid = {
    "clf__max_features": ["sqrt", "auto", "log2", 0.5, 0.8, 0.9],
    "clf__max_depth": [None, 5, 10, 20],
    "clf__min_samples_leaf": [1, 5, 10],
    "clf__min_samples_split": [2, 10, 20],
    "clf__n_estimators": [50],
}

knn_grid = {
    "clf__n_neighbors": [1, 2, 3, 5, 10, 20],
    "clf__leaf_size": [2, 3, 5, 10, 30, 50, 100],
    "clf__p": [1, 2, 5, 10],
    "clf__weights": ["uniform", "distance"],
}

rf_grid_classification = rf_grid.copy()
rf_grid_classification.update({"clf__class_weight": ["balanced"]})

rf_classification = {"clf": RandomForestClassifier, "grid": rf_grid_classification}
rf_regression = {"clf": RandomForestRegressor, "grid": rf_grid}

knn_classification = {"clf": KNeighborsClassifier, "grid": knn_grid}
knn_regression = {"clf": KNeighborsRegressor, "grid": knn_grid}

# ridge_classification = {'clf': KNeighborsClassifier, 'grid': {
#    "clf__n_neighbors": [4], "clf__weights": ["distance"]}}


options = {
    "regression": [ridge_regression, rf_regression, knn_regression],
    "classification": [ridge_classification, rf_classification, knn_classification],
}


def sparse_or_dense(X, RAM=None, magic=42):
    if scipy.sparse.issparse(X):
        return "sparse"
    else:
        # USING PAPER WE WILL GO TO DENSE ANYWAY
        return "dense"
    # size = np.prod(X.shape) if hasattr(X, 'shape') else len(X) * len(X[0])

    # # if N * num_feat * magic > RAM:
    # if size > 1000 ** 3:
    #     return 'sparse'
    # else:
    #     return 'dense'


def pick(X, y, cl_or_reg=None, opts=None):
    # i always choose first one now
    if opts is None:
        opts = options
    cl_or_reg = cl_or_reg if cl_or_reg else classification_or_regression(y)
    return opts[cl_or_reg]
