

from ..vaex.ml.cluster import *
import traitlets

def k_means(self, cluster_centers, features, inertia=None, init='random', max_iter=300, n_clusters=2, n_init=1, prediction_label='prediction_kmeans', random_state=None, verbose=False):
    obj = vaex.ml.cluster.KMeans([{'name': 'cluster_centers', 'help': 'Coordinates of cluster centers.'}, {'name': 'features', 'help': 'List of features to cluster.'}, {'name': 'inertia', 'help': 'Sum of squared distances of samples to their closest cluster center.'}, {'name': 'init', 'help': 'Method for initializing the centroids.'}, {'name': 'max_iter', 'help': 'Maximum number of iterations of the KMeans algorithm for a single run.'}, {'name': 'n_clusters', 'help': 'Number of clusters to form.'}, {'name': 'n_init', 'help': 'Number of centroid initializations.                                                    The KMeans algorithm will be run for each initialization,                                                    and the final results will be the best output of the n_init                                                    consecutive runs in terms of inertia.'}, {'name': 'prediction_label', 'help': 'The name of the virtual column that houses the cluster labels for each point.'}, {'name': 'random_state', 'help': 'Random number generation for centroid initialization.                                                                              If an int is specified, the randomness becomes deterministic.'}, {'name': 'verbose', 'help': 'If True, enable verbosity mode.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(k_means=k_means)

def __init__(self, cluster_centers=traitlets.Undefined, features=traitlets.Undefined, inertia=None, init='random', max_iter=300, n_clusters=2, n_init=1, prediction_label='prediction_kmeans', random_state=None, verbose=False):
    """
    

:param cluster_centers: Coordinates of cluster centers.
:param features: List of features to cluster.
:param inertia: Sum of squared distances of samples to their closest cluster center.
:param init: Method for initializing the centroids.
:param max_iter: Maximum number of iterations of the KMeans algorithm for a single run.
:param n_clusters: Number of clusters to form.
:param n_init: Number of centroid initializations.                                                    The KMeans algorithm will be run for each initialization,                                                    and the final results will be the best output of the n_init                                                    consecutive runs in terms of inertia.
:param prediction_label: The name of the virtual column that houses the cluster labels for each point.
:param random_state: Random number generation for centroid initialization.                                                                              If an int is specified, the randomness becomes deterministic.
:param verbose: If True, enable verbosity mode.
    """
    given_kwargs = {key:value for key, value in dict(cluster_centers=cluster_centers, features=features, inertia=inertia, init=init, max_iter=max_iter, n_clusters=n_clusters, n_init=n_init, prediction_label=prediction_label, random_state=random_state, verbose=verbose).items() if value is not traitlets.Undefined}

    super(vaex.ml.cluster.KMeans, self).__init__(**given_kwargs)

KMeans.__init__ = __init__
KMeans.__signature__ = __init__
del __init__
    