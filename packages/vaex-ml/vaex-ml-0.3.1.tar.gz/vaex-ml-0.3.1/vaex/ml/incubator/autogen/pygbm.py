

from vaex.ml.incubator.pygbm import *
import traitlets

def py_gbm_model(self, features, param, learning_rate=0.1, max_bins=255, max_iter=10, max_leaf_nodes=31, num_round=0, prediction_name='pygbm_prediction', random_state=0, verbose=1):
    obj = vaex.ml.incubator.pygbm.PyGBMModel([])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(py_gbm_model=py_gbm_model)

def __init__(self, features=traitlets.Undefined, learning_rate=0.1, max_bins=255, max_iter=10, max_leaf_nodes=31, num_round=0, param=traitlets.Undefined, prediction_name='pygbm_prediction', random_state=0, verbose=1):
    """
    

    """
    given_kwargs = {key:value for key, value in dict(features=features, learning_rate=learning_rate, max_bins=max_bins, max_iter=max_iter, max_leaf_nodes=max_leaf_nodes, num_round=num_round, param=param, prediction_name=prediction_name, random_state=random_state, verbose=verbose).items() if value is not traitlets.Undefined}

    super(vaex.ml.incubator.pygbm.PyGBMModel, self).__init__(**given_kwargs)

PyGBMModel.__init__ = __init__
PyGBMModel.__signature__ = __init__
del __init__
    