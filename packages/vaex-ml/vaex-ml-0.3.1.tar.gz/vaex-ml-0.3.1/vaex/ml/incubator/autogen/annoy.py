

from vaex.ml.incubator.annoy import *
import traitlets

def annoy_model(self, features, metric='euclidean', n_neighbours=10, n_trees=10, predcition_name='annoy_prediction', prediction_name='annoy_prediction', search_k=-1):
    obj = vaex.ml.incubator.annoy.ANNOYModel([{'name': 'features', 'help': 'List of features to use.'}, {'name': 'metric', 'help': 'Metric to use for distance calculations'}, {'name': 'n_neighbours', 'help': 'Now many neighbours'}, {'name': 'n_trees', 'help': 'Number of trees to build.'}, {'name': 'predcition_name', 'help': 'Output column name for the neighbours when transforming a dataset'}, {'name': 'prediction_name', 'help': 'Output column name for the neighbours when transforming a dataset'}, {'name': 'search_k', 'help': 'Jovan?'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(annoy_model=annoy_model)

def __init__(self, features=traitlets.Undefined, metric='euclidean', n_neighbours=10, n_trees=10, predcition_name='annoy_prediction', prediction_name='annoy_prediction', search_k=-1):
    """
    

:param features: List of features to use.
:param metric: Metric to use for distance calculations
:param n_neighbours: Now many neighbours
:param n_trees: Number of trees to build.
:param predcition_name: Output column name for the neighbours when transforming a dataset
:param prediction_name: Output column name for the neighbours when transforming a dataset
:param search_k: Jovan?
    """
    given_kwargs = {key:value for key, value in dict(features=features, metric=metric, n_neighbours=n_neighbours, n_trees=n_trees, predcition_name=predcition_name, prediction_name=prediction_name, search_k=search_k).items() if value is not traitlets.Undefined}

    super(vaex.ml.incubator.annoy.ANNOYModel, self).__init__(**given_kwargs)

ANNOYModel.__init__ = __init__
ANNOYModel.__signature__ = __init__
del __init__
    