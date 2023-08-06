

import vaex.ml.ui
import traitlets

def widgetize(self, _display_callbacks, _dom_classes, _msg_callbacks, _property_lock, _states_to_send, children, comm, keys, layout, log, _model_module='@jupyter-widgets/controls', _model_module_version='1.4.0', _model_name='VBoxModel', _view_count=None, _view_module='@jupyter-widgets/controls', _view_module_version='1.4.0', _view_name='VBoxView', box_style=''):
    obj = vaex.ml.ui.Widgetize([{'name': '_dom_classes', 'help': 'CSS classes applied to widget DOM element'}, {'name': '_view_count', 'help': 'EXPERIMENTAL: The number of views of the model displayed in the frontend. This attribute is experimental and may change or be removed in the future. None signifies that views will not be tracked. Set this to 0 to start tracking view creation/deletion.'}, {'name': 'box_style', 'help': 'Use a predefined styling for the box.'}, {'name': 'children', 'help': 'List of widget children'}, {'name': 'keys', 'help': 'The traits which are synced.'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(widgetize=widgetize)

def __init__(self, _display_callbacks=traitlets.Undefined, _dom_classes=traitlets.Undefined, _model_module='@jupyter-widgets/controls', _model_module_version='1.4.0', _model_name='VBoxModel', _msg_callbacks=traitlets.Undefined, _property_lock=traitlets.Undefined, _states_to_send=traitlets.Undefined, _view_count=None, _view_module='@jupyter-widgets/controls', _view_module_version='1.4.0', _view_name='VBoxView', box_style='', children=traitlets.Undefined, comm=traitlets.Undefined, keys=traitlets.Undefined, layout=traitlets.Undefined, log=traitlets.Undefined):
    """
    

:param _dom_classes: CSS classes applied to widget DOM element
:param _view_count: EXPERIMENTAL: The number of views of the model displayed in the frontend. This attribute is experimental and may change or be removed in the future. None signifies that views will not be tracked. Set this to 0 to start tracking view creation/deletion.
:param box_style: Use a predefined styling for the box.
:param children: List of widget children
:param keys: The traits which are synced.
    """
    super(vaex.ml.ui.Widgetize, self).__init__(_display_callbacks=_display_callbacks, _dom_classes=_dom_classes, _model_module=_model_module, _model_module_version=_model_module_version, _model_name=_model_name, _msg_callbacks=_msg_callbacks, _property_lock=_property_lock, _states_to_send=_states_to_send, _view_count=_view_count, _view_module=_view_module, _view_module_version=_view_module_version, _view_name=_view_name, box_style=box_style, children=children, comm=comm, keys=keys, layout=layout, log=log)

vaex.ml.ui.Widgetize.__init__ = __init__
vaex.ml.ui.Widgetize.__signature__ = __init__
del __init__
    


import vaex.ml.transformations
import traitlets

def pca(self, features, n_components=2, prefix='PCA_'):
    obj = vaex.ml.transformations.PCA([])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(pca=pca)

def __init__(self, features=traitlets.Undefined, n_components=2, prefix='PCA_'):
    """
    

    """
    super(vaex.ml.transformations.PCA, self).__init__(features=features, n_components=n_components, prefix=prefix)

vaex.ml.transformations.PCA.__init__ = __init__
vaex.ml.transformations.PCA.__signature__ = __init__
del __init__
    


import vaex.ml.transformations
import traitlets

def label_encoder(self, features, prefix='label_encoded_'):
    obj = vaex.ml.transformations.LabelEncoder([])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(label_encoder=label_encoder)

def __init__(self, features=traitlets.Undefined, prefix='label_encoded_'):
    """
    

    """
    super(vaex.ml.transformations.LabelEncoder, self).__init__(features=features, prefix=prefix)

vaex.ml.transformations.LabelEncoder.__init__ = __init__
vaex.ml.transformations.LabelEncoder.__signature__ = __init__
del __init__
    


import vaex.ml.transformations
import traitlets

def one_hot_encoder(self, features, one=1, prefix='', zero=0):
    obj = vaex.ml.transformations.OneHotEncoder([{'name': 'features', 'help': 'List of features to one hot encode'}, {'name': 'one', 'help': 'Value to use for existing values'}, {'name': 'prefix', 'help': 'Prefix to add to the columns'}, {'name': 'zero', 'help': 'Value to use for missing values'}])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(one_hot_encoder=one_hot_encoder)

def __init__(self, features=traitlets.Undefined, one=1, prefix='', zero=0):
    """
    

:param features: List of features to one hot encode
:param one: Value to use for existing values
:param prefix: Prefix to add to the columns
:param zero: Value to use for missing values
    """
    super(vaex.ml.transformations.OneHotEncoder, self).__init__(features=features, one=one, prefix=prefix, zero=zero)

vaex.ml.transformations.OneHotEncoder.__init__ = __init__
vaex.ml.transformations.OneHotEncoder.__signature__ = __init__
del __init__
    


import vaex.ml.transformations
import traitlets

def standard_scaler(self, features, prefix='standard_scaled_', with_mean=True, with_std=True):
    obj = vaex.ml.transformations.StandardScaler([])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(standard_scaler=standard_scaler)

def __init__(self, features=traitlets.Undefined, prefix='standard_scaled_', with_mean=True, with_std=True):
    """
    

    """
    super(vaex.ml.transformations.StandardScaler, self).__init__(features=features, prefix=prefix, with_mean=with_mean, with_std=with_std)

vaex.ml.transformations.StandardScaler.__init__ = __init__
vaex.ml.transformations.StandardScaler.__signature__ = __init__
del __init__
    


import vaex.ml.transformations
import traitlets

def min_max_scaler(self, feature_range, features, prefix='minmax_scaled_'):
    obj = vaex.ml.transformations.MinMaxScaler([])
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(min_max_scaler=min_max_scaler)

def __init__(self, feature_range=traitlets.Undefined, features=traitlets.Undefined, prefix='minmax_scaled_'):
    """
    

    """
    super(vaex.ml.transformations.MinMaxScaler, self).__init__(feature_range=feature_range, features=features, prefix=prefix)

vaex.ml.transformations.MinMaxScaler.__init__ = __init__
vaex.ml.transformations.MinMaxScaler.__signature__ = __init__
del __init__
    
