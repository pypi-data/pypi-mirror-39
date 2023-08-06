

from ..vaex.ml.lightgbm import *
import traitlets

def light_gbm_model(self, features, param, num_round=0, prediction_name='lightgbm_prediction'):
    obj = vaex.ml.lightgbm.LightGBMModel([{'name': 'features', 'help': 'List of features to use when fitting the LightGBMModel.'}, {'name': 'num_round', 'help': 'Number of boosting iterations.'}, {'name': 'param', 'help': 'parameters to be passed on the to the LightGBM model.'}, {'name': 'prediction_name', 'help': 'The name of the virtual column housing the predictions.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(light_gbm_model=light_gbm_model)

def __init__(self, features=traitlets.Undefined, num_round=0, param=traitlets.Undefined, prediction_name='lightgbm_prediction'):
    """
    

:param features: List of features to use when fitting the LightGBMModel.
:param num_round: Number of boosting iterations.
:param param: parameters to be passed on the to the LightGBM model.
:param prediction_name: The name of the virtual column housing the predictions.
    """
    given_kwargs = {key:value for key, value in dict(features=features, num_round=num_round, param=param, prediction_name=prediction_name).items() if value is not traitlets.Undefined}

    super(vaex.ml.lightgbm.LightGBMModel, self).__init__(**given_kwargs)

LightGBMModel.__init__ = __init__
LightGBMModel.__signature__ = __init__
del __init__
    


from ..vaex.ml.lightgbm import *
import traitlets

def light_gbm_classifier(self, features, param, num_round=0, prediction_name='lightgbm_prediction'):
    obj = vaex.ml.lightgbm.LightGBMClassifier([{'name': 'features', 'help': 'List of features to use when fitting the LightGBMModel.'}, {'name': 'num_round', 'help': 'Number of boosting iterations.'}, {'name': 'param', 'help': 'parameters to be passed on the to the LightGBM model.'}, {'name': 'prediction_name', 'help': 'The name of the virtual column housing the predictions.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(light_gbm_classifier=light_gbm_classifier)

def __init__(self, features=traitlets.Undefined, num_round=0, param=traitlets.Undefined, prediction_name='lightgbm_prediction'):
    """
    

:param features: List of features to use when fitting the LightGBMModel.
:param num_round: Number of boosting iterations.
:param param: parameters to be passed on the to the LightGBM model.
:param prediction_name: The name of the virtual column housing the predictions.
    """
    given_kwargs = {key:value for key, value in dict(features=features, num_round=num_round, param=param, prediction_name=prediction_name).items() if value is not traitlets.Undefined}

    super(vaex.ml.lightgbm.LightGBMClassifier, self).__init__(**given_kwargs)

LightGBMClassifier.__init__ = __init__
LightGBMClassifier.__signature__ = __init__
del __init__
    