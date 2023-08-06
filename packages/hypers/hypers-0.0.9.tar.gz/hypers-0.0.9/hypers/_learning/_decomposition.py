import numpy as np 
from sklearn.decomposition import (
    PCA, FastICA, IncrementalPCA, TruncatedSVD, DictionaryLearning, MiniBatchDictionaryLearning,
    FactorAnalysis, NMF, LatentDirichletAllocation
)

DECOMPOSE_TYPES = (
    PCA,
    FastICA,
    #KernelPCA,
    IncrementalPCA,
    TruncatedSVD,
    DictionaryLearning,
    MiniBatchDictionaryLearning,
    FactorAnalysis,
    NMF,
    LatentDirichletAllocation
)


def _data_decomposition(X, mdl):
    if type(mdl) not in DECOMPOSE_TYPES:
        raise TypeError('Must pass a sklearn decomposition class. Refer to documentation.')

    X.mdl_decompose = mdl
    n_components = X.mdl_decompose.get_params()['n_components']
    images = X.mdl_decompose.fit_transform(X.flatten()).reshape(X.data.shape[:-1] + (n_components,))
    specs = X.mdl_decompose.components_.transpose()

    return images, specs


def _data_scree(X):
    """Returns the array for the scree plot

    Returns the scree plot from `PCA` as an array.

    Returns
    -------
    scree : array, shape (n_features,)

    """
    mdl = PCA()
    mdl.fit_transform(X.flatten())
    scree = mdl.explained_variance_ratio_

    return scree
