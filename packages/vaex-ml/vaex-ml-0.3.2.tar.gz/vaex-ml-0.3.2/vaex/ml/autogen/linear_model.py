

from vaex.ml.linear_model import *
import traitlets

def logistic_regression(self, features, _sk_params=None, binned=True, fit_intercept=True, prediction_name='logit_prediction', shape=64):
    obj = vaex.ml.linear_model.LogisticRegression([])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(logistic_regression=logistic_regression)

def __init__(self, _sk_params=None, binned=True, features=traitlets.Undefined, fit_intercept=True, prediction_name='logit_prediction', shape=64):
    """
    

    """
    given_kwargs = {key:value for key, value in dict(_sk_params=_sk_params, binned=binned, features=features, fit_intercept=fit_intercept, prediction_name=prediction_name, shape=shape).items() if value is not traitlets.Undefined}

    super(vaex.ml.linear_model.LogisticRegression, self).__init__(**given_kwargs)

LogisticRegression.__init__ = __init__
LogisticRegression.__signature__ = __init__
del __init__
    


from vaex.ml.linear_model import *
import traitlets

def linear_regression(self, features, _sk_params=None, binned=True, fit_intercept=True, prediction_name='linear_prediction', shape=64):
    obj = vaex.ml.linear_model.LinearRegression([])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(linear_regression=linear_regression)

def __init__(self, _sk_params=None, binned=True, features=traitlets.Undefined, fit_intercept=True, prediction_name='linear_prediction', shape=64):
    """
    

    """
    given_kwargs = {key:value for key, value in dict(_sk_params=_sk_params, binned=binned, features=features, fit_intercept=fit_intercept, prediction_name=prediction_name, shape=shape).items() if value is not traitlets.Undefined}

    super(vaex.ml.linear_model.LinearRegression, self).__init__(**given_kwargs)

LinearRegression.__init__ = __init__
LinearRegression.__signature__ = __init__
del __init__
    