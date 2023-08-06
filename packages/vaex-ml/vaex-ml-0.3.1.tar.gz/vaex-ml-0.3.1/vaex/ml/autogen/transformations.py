

from vaex.ml.transformations import *
import traitlets

def pca(self, features, n_components=2, prefix='PCA_'):
    obj = vaex.ml.transformations.PCA([{'name': 'features', 'help': 'List of features to transform.'}, {'name': 'n_components', 'help': 'Number of components to retain.'}, {'name': 'prefix', 'help': 'Prefix for the names of the transformed features.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(pca=pca)

def __init__(self, features=traitlets.Undefined, n_components=2, prefix='PCA_'):
    """
    

:param features: List of features to transform.
:param n_components: Number of components to retain.
:param prefix: Prefix for the names of the transformed features.
    """
    given_kwargs = {key:value for key, value in dict(features=features, n_components=n_components, prefix=prefix).items() if value is not traitlets.Undefined}

    super(vaex.ml.transformations.PCA, self).__init__(**given_kwargs)

PCA.__init__ = __init__
PCA.__signature__ = __init__
del __init__
    


from vaex.ml.transformations import *
import traitlets

def label_encoder(self, features, prefix='Prefix for the names of the transformed features.'):
    obj = vaex.ml.transformations.LabelEncoder([{'name': 'features', 'help': 'List of features to transform.'}, {'name': 'prefix', 'help': ''}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(label_encoder=label_encoder)

def __init__(self, features=traitlets.Undefined, prefix='Prefix for the names of the transformed features.'):
    """
    

:param features: List of features to transform.
:param prefix: 
    """
    given_kwargs = {key:value for key, value in dict(features=features, prefix=prefix).items() if value is not traitlets.Undefined}

    super(vaex.ml.transformations.LabelEncoder, self).__init__(**given_kwargs)

LabelEncoder.__init__ = __init__
LabelEncoder.__signature__ = __init__
del __init__
    


from vaex.ml.transformations import *
import traitlets

def one_hot_encoder(self, features, one=1, prefix='', zero=0):
    obj = vaex.ml.transformations.OneHotEncoder([{'name': 'features', 'help': 'List of features to transform.'}, {'name': 'one', 'help': 'Value to encode when a category is present.'}, {'name': 'prefix', 'help': 'Prefix for the names of the transformed features.'}, {'name': 'zero', 'help': 'Value to encode when category is absent.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(one_hot_encoder=one_hot_encoder)

def __init__(self, features=traitlets.Undefined, one=1, prefix='', zero=0):
    """
    

:param features: List of features to transform.
:param one: Value to encode when a category is present.
:param prefix: Prefix for the names of the transformed features.
:param zero: Value to encode when category is absent.
    """
    given_kwargs = {key:value for key, value in dict(features=features, one=one, prefix=prefix, zero=zero).items() if value is not traitlets.Undefined}

    super(vaex.ml.transformations.OneHotEncoder, self).__init__(**given_kwargs)

OneHotEncoder.__init__ = __init__
OneHotEncoder.__signature__ = __init__
del __init__
    


from vaex.ml.transformations import *
import traitlets

def standard_scaler(self, features, prefix='standard_scaled_', with_mean=True, with_std=True):
    obj = vaex.ml.transformations.StandardScaler([{'name': 'features', 'help': 'List of features to transform.'}, {'name': 'prefix', 'help': 'Prefix for the names of the transformed features.'}, {'name': 'with_mean', 'help': 'If True, remove the mean from each feature.'}, {'name': 'with_std', 'help': 'If True, scale each feature to unit variance.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(standard_scaler=standard_scaler)

def __init__(self, features=traitlets.Undefined, prefix='standard_scaled_', with_mean=True, with_std=True):
    """
    

:param features: List of features to transform.
:param prefix: Prefix for the names of the transformed features.
:param with_mean: If True, remove the mean from each feature.
:param with_std: If True, scale each feature to unit variance.
    """
    given_kwargs = {key:value for key, value in dict(features=features, prefix=prefix, with_mean=with_mean, with_std=with_std).items() if value is not traitlets.Undefined}

    super(vaex.ml.transformations.StandardScaler, self).__init__(**given_kwargs)

StandardScaler.__init__ = __init__
StandardScaler.__signature__ = __init__
del __init__
    


from vaex.ml.transformations import *
import traitlets

def min_max_scaler(self, feature_range, features, prefix='minmax_scaled_'):
    obj = vaex.ml.transformations.MinMaxScaler([{'name': 'feature_range', 'help': 'The range the features are scaled to.'}, {'name': 'features', 'help': 'List of features to transform.'}, {'name': 'prefix', 'help': 'Prefix for the names of the transformed features.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(min_max_scaler=min_max_scaler)

def __init__(self, feature_range=traitlets.Undefined, features=traitlets.Undefined, prefix='minmax_scaled_'):
    """
    

:param feature_range: The range the features are scaled to.
:param features: List of features to transform.
:param prefix: Prefix for the names of the transformed features.
    """
    given_kwargs = {key:value for key, value in dict(feature_range=feature_range, features=features, prefix=prefix).items() if value is not traitlets.Undefined}

    super(vaex.ml.transformations.MinMaxScaler, self).__init__(**given_kwargs)

MinMaxScaler.__init__ = __init__
MinMaxScaler.__signature__ = __init__
del __init__
    


from vaex.ml.transformations import *
import traitlets

def max_abs_scaler(self, features, prefix='absmax_scaled_'):
    obj = vaex.ml.transformations.MaxAbsScaler([{'name': 'features', 'help': 'List of features to transform.'}, {'name': 'prefix', 'help': 'Prefix for the names of the transformed features.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(max_abs_scaler=max_abs_scaler)

def __init__(self, features=traitlets.Undefined, prefix='absmax_scaled_'):
    """
    

:param features: List of features to transform.
:param prefix: Prefix for the names of the transformed features.
    """
    given_kwargs = {key:value for key, value in dict(features=features, prefix=prefix).items() if value is not traitlets.Undefined}

    super(vaex.ml.transformations.MaxAbsScaler, self).__init__(**given_kwargs)

MaxAbsScaler.__init__ = __init__
MaxAbsScaler.__signature__ = __init__
del __init__
    


from vaex.ml.transformations import *
import traitlets

def robust_scaler(self, features, percentile_range, prefix='robust_scaled_', with_centering=True, with_scaling=True):
    obj = vaex.ml.transformations.RobustScaler([{'name': 'features', 'help': 'List of features to transform.'}, {'name': 'percentile_range', 'help': 'The percentile range to which to scale each feature to.'}, {'name': 'prefix', 'help': 'Prefix for the names of the transformed features.'}, {'name': 'with_centering', 'help': 'If True, remove the median.'}, {'name': 'with_scaling', 'help': 'If True, scale each feature between the specified percentile range.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(robust_scaler=robust_scaler)

def __init__(self, features=traitlets.Undefined, percentile_range=traitlets.Undefined, prefix='robust_scaled_', with_centering=True, with_scaling=True):
    """
    

:param features: List of features to transform.
:param percentile_range: The percentile range to which to scale each feature to.
:param prefix: Prefix for the names of the transformed features.
:param with_centering: If True, remove the median.
:param with_scaling: If True, scale each feature between the specified percentile range.
    """
    given_kwargs = {key:value for key, value in dict(features=features, percentile_range=percentile_range, prefix=prefix, with_centering=with_centering, with_scaling=with_scaling).items() if value is not traitlets.Undefined}

    super(vaex.ml.transformations.RobustScaler, self).__init__(**given_kwargs)

RobustScaler.__init__ = __init__
RobustScaler.__signature__ = __init__
del __init__
    