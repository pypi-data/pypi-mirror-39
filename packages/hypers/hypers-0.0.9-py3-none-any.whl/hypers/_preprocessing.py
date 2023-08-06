import numpy as np
from sklearn.preprocessing import (
    MaxAbsScaler, MinMaxScaler, PowerTransformer, QuantileTransformer, RobustScaler,
    StandardScaler
)

PREPROCESSING_TYPES = (
    MaxAbsScaler,
    MinMaxScaler,
    PowerTransformer,
    QuantileTransformer,
    RobustScaler,
    StandardScaler
)


# TODO This is scaling samples. Perhaphs amend to give option to scale features as well.
def _data_preprocessing(X, mdl):
    if type(mdl) not in PREPROCESSING_TYPES:
        raise TypeError('Must pass a sklearn preprocessing class. Refer to documentation.')
    
    X.mdl_preprocess = mdl
    
    X_newdata = X.mdl_preprocess.fit_transform(X.flatten().transpose()).transpose().reshape(X.shape)
    X.data = X_newdata
    X.update()
