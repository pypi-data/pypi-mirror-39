

from ..vaex.ml.xgboost import *
import traitlets

def xgb_model(self, features, param, num_round=0, prediction_name='xgboost_prediction'):
    obj = vaex.ml.xgboost.XGBModel([])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(xgb_model=xgb_model)

def __init__(self, features=traitlets.Undefined, num_round=0, param=traitlets.Undefined, prediction_name='xgboost_prediction'):
    """
    

    """
    given_kwargs = {key:value for key, value in dict(features=features, num_round=num_round, param=param, prediction_name=prediction_name).items() if value is not traitlets.Undefined}

    super(vaex.ml.xgboost.XGBModel, self).__init__(**given_kwargs)

XGBModel.__init__ = __init__
XGBModel.__signature__ = __init__
del __init__
    