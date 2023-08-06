import vaex.dataset
from vaex.serialize import register
import numpy as np
from . import generate
from .state import HasState
from traitlets import Dict, Unicode, List, Int, CFloat, CBool, Any, Tuple
from vaex.utils import _ensure_strings_from_expressions

help_features = 'List of features to transform.'
help_prefix = 'Prefix for the names of the transformed features.'


def dot_product(a, b):
    products = ['%s * %s' % (ai, bi) for ai, bi in zip(a, b)]
    return ' + '.join(products)


@register
class StateTransfer(HasState):
    state = Dict()

    def transform(self, dataset):
        copy = dataset.copy()
        self.state = dict(self.state, active_range=[copy._index_start, copy._index_end])
        copy.state_set(self.state)
        return copy


class Transformer(HasState):
    ''' Parent class for all of the transformers.
    Currently it implements only the fit_predict() method.
    '''

    def fit_transform(self, dataset):
        '''Fit and apply the transformer to the supplied dataset.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        :param copy: A shallow copy of the dataset that includes the transformations.
        '''

        self.fit(dataset=dataset)
        return self.transform(dataset=dataset)


@register
@generate.register
class PCA(Transformer):
    '''Transform a set of features using a Principal Component Analysis.

    Example
    -------

    >>> import vaex.ml
    >>> df = vaex.ml.datasets.load_iris()
    >>> features = ['sepal_width', 'petal_length', 'sepal_length', 'petal_width']
    >>> df_train, df_test = vaex.ml.train_test_split(df)
    >>> pca = vaex.ml.PCA(features=features, n_components=3)
    >>> df_train = pca.fit_transform(df_train)
    >>> df_test = pca.transform(df_test)
    '''

    # title = Unicode(default_value='PCA', read_only=True).tag(ui='HTML')
    features = List(Unicode(), help=help_features).tag(ui='SelectMultiple')
    n_components = Int(default_value=2, help='Number of components to retain.').tag(ui='IntText')
    prefix = Unicode(default_value="PCA_", help=help_prefix)
    eigen_vectors_ = List(List(CFloat()), help='The eigen vectors corresponding to each feature').tag(output=True)
    eigen_values_ = List(CFloat(), help='The eigen values that correspond to each feature.').tag(output=True)
    means_ = List(CFloat(), help='The mean of each feature').tag(output=True)

    def fit(self, dataset, column_names=None, progress=False):
        '''
        Fit the PCA model to the dataset.

        Parameters:
        -----------
        :param dataset: A vaex dataset.
        :param columns: Deprecated and should be removed.
        :param progress: bool, if True, display a progress bar of the fitting process.

        Returns:
        --------
        self
        '''

        assert self.n_components <= len(self.features), 'cannot have more components than features'
        C = dataset.cov(self.features, progress=progress)
        eigen_values, eigen_vectors = np.linalg.eigh(C)
        indices = np.argsort(eigen_values)[::-1]
        self.means_ = dataset.mean(self.features, progress=progress).tolist()
        self.eigen_vectors_ = eigen_vectors[:, indices].tolist()
        self.eigen_values_ = eigen_values[indices].tolist()

    def transform(self, dataset, n_components=None):
        '''
        Apply the PCA transformation to the dataset.

        Parameters:
        -----------
        :param dataset: A vaex dataset.
        :param n_components: The number of components to retain.

        Returns:
        --------
        :return copy: A shallow copy of the dataset that includes the PCA components.
        '''

        n_components = n_components or self.n_components
        copy = dataset.copy()
        name_prefix_offset = 0
        eigen_vectors = np.array(self.eigen_vectors_)
        while self.prefix + str(name_prefix_offset) in copy.get_column_names(virtual=True, strings=True):
            name_prefix_offset += 1

        expressions = [copy[feature]-mean for feature, mean in zip(self.features, self.means_)]
        for i in range(n_components):
            v = eigen_vectors[:, i]
            expr = dot_product(expressions, v)
            name = self.prefix + str(i + name_prefix_offset)
            copy[name] = expr
        return copy


@register
@generate.register
class LabelEncoder(Transformer):
    '''Encode categorical columns with integer values between 0 and num_classes-1.

    Example
    -------

    >>> import vaex.ml
    >>> df = vaex.ml.datasets.load_titanic()
    >>> df_train, df_test = vaex.ml.train_test_split(df)
    >>> encoder = vaex.ml.LabelEncoder(features=['sex', 'embarked'])
    >>> df_train = encoder.fit_transform(df_train)
    >>> df_test = encoder.transform(df_test)
    '''

    # title = Unicode(default_value='Label Encoder', read_only=True).tag(ui='HTML')
    features = List(Unicode(), help=help_features).tag(ui='SelectMultiple')
    prefix = Unicode(default_value=help_prefix, help="").tag(ui='Text')
    labels_ = List(List(), help='The encoded labels of each feature.').tag(output=True)

    def fit(self, dataset):
        '''
        Fit LabelEncoder to the dataset.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        self
        '''

        labels = []
        for i in self.features:
            labels.append(np.unique(dataset.evaluate(i)).tolist())
        self.labels_ = labels

    def transform(self, dataset):
        '''
        Transform a dataset with a fitted LabelEncoder.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        :return copy: A shallow copy of the dataset that includes the encodings.
        '''

        copy = dataset.copy()
        for i, v in enumerate(self.features):
            name = self.prefix + v
            labels = np.unique(dataset.evaluate(v))
            if len(np.intersect1d(labels, self.labels_[i])) < len(labels):
                diff = np.setdiff1d(labels, self.labels_[i])
                raise ValueError("%s contains previously unseen labels: %s" % (v, str(diff)))
            # copy[name] = np.searchsorted(self.labels[i], v)
            copy.add_virtual_column(name, 'searchsorted({x}, {v})'.format(x=self.labels_[i], v=v))
        return copy


@register
@generate.register
class OneHotEncoder(Transformer):
    '''Encode categorical columns according ot the One-Hot scheme.

    Example
    -------

    >>> import vaex.ml
    >>> df = vaex.from_arrays(color=['red', 'green', 'green', 'blue', 'red'])
    >>> df
     #  color
     0  red
     1  green
     2  green
     3  blue
     4  red
    >>> encoder = vaex.ml.OneHotEncoder(features=['color'])
    >>> encoder.fit_transform(df)
     #  color      color_blue    color_green    color_red
     0  red                 0              0            1
     1  green               0              1            0
     2  green               0              1            0
     3  blue                1              0            0
     4  red                 0              0            1

    '''

    # title = Unicode(default_value='One-Hot Encoder', read_only=True).tag(ui='HTML')
    features = List(Unicode(), help=help_features).tag(ui='SelectMultiple')
    prefix = Unicode(default_value='', help=help_prefix).tag(ui='Text')
    one = Any(1, help='Value to encode when a category is present.')
    zero = Any(0, help='Value to encode when category is absent.')
    uniques_ = List(List(), help='The unique elements found in each feature.').tag(output=True)

    def fit(self, dataset):
        '''Fit OneHotEncoder to the dataset.

        :param dataset: A vaex dataset.
        '''

        uniques = []
        for i in self.features:
            expression = _ensure_strings_from_expressions(i)
            unique = dataset.unique(expression)
            unique = np.sort(unique)  # this can/should be optimized with @delay
            uniques.append(unique.tolist())
        self.uniques_ = uniques

    def transform(self, dataset):
        '''Transform a dataset with a fitted OneHotEncoder.

        :param dataset: A vaex dataset.
        :return: A shallow copy of the dataset that includes the encodings.
        '''

        copy = dataset.copy()
        # for each feature, add a virtual column for each unique entry
        for i, feature in enumerate(self.features):
            for j, value in enumerate(self.uniques_[i]):
                column_name = self.prefix + feature + '_' + str(value)
                copy.add_virtual_column(column_name, 'where({feature} == {value}, {one}, {zero})'.format(
                                        feature=feature, value=repr(value), one=self.one, zero=self.zero))
        return copy


@register
@generate.register
class StandardScaler(Transformer):
    '''Standardize features by removing thir mean and scaling them to unit variance.

    Example:
    --------

    >>> import vaex.ml
    >>> df = vaex.ml.datasets.load_iris()
    >>> features = ['sepal_width', 'petal_length', 'sepal_length', 'petal_width']
    >>> df_train, df_test = vaex.ml.train_test_split(df)
    >>> scaler = vaex.ml.StandardScaler(features=features, with_mean=True, with_std=True)
    >>> df_train = scaler.fit_transform(df_train)
    >>> df_test = scaler.transform(df_test)
    '''

    # title = Unicode(default_value='Standard Scaler', read_only=True).tag(ui='HTML')
    features = List(Unicode(), help=help_features).tag(ui='SelectMultiple')
    prefix = Unicode(default_value="standard_scaled_", help=help_prefix).tag(ui='Text')
    with_mean = CBool(default_value=True, help='If True, remove the mean from each feature.').tag(ui='Checkbox')
    with_std = CBool(default_value=True, help='If True, scale each feature to unit variance.').tag(ui='Checkbox')
    mean_ = List(CFloat(), help='The mean of each feature').tag(output=True)
    std_ = List(CFloat(), help='The standard deviation of each feature.').tag(output=True)

    def fit(self, dataset):
        '''
        Fit StandardScaler to the dataset.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        self
        '''

        mean = dataset.mean(self.features, delay=True)
        std = dataset.std(self.features, delay=True)

        @vaex.delayed
        def assign(mean, std):
            self.mean_ = mean.tolist()
            self.std_ = std.tolist()

        assign(mean, std)
        dataset.executor.execute()

    def transform(self, dataset):
        '''
        Transform a dataset with a fitted StandardScaler.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        :return copy: a shallow copy of the dataset that includes the scaled features.
        '''

        copy = dataset.copy()
        for i in range(len(self.features)):
            name = self.prefix+self.features[i]
            expression = copy[self.features[i]]
            if self.with_mean:
                expression = expression - self.mean_[i]
            if self.with_std:
                expression = expression / self.std_[i]
            copy[name] = expression
        return copy


@register
@generate.register
class MinMaxScaler(Transformer):
    '''Will scale a set of features to a given range.

    Example:
    --------

    >>> import vaex.ml
    >>> df = vaex.ml.datasets.load_iris()
    >>> features = ['sepal_width', 'petal_length', 'sepal_length', 'petal_width']
    >>> df_train, df_test = vaex.ml.train_test_split(df)
    >>> scaler = vaex.ml.MinMaxScaler(features=features, feature_range=(0, 1))
    >>> df_train = scaler.fit_transform(df_train)
    >>> df_test = scaler.transform(df_test)
    '''

    # title = Unicode(default_value='MinMax Scaler', read_only=True).tag(ui='HTML')
    features = List(Unicode(), help=help_features).tag(ui='SelectMultiple')
    feature_range = Tuple(default_value=(0, 1), help='The range the features are scaled to.').tag().tag(ui='FloatRangeSlider')
    prefix = Unicode(default_value="minmax_scaled_", help=help_prefix).tag(ui='Text')
    fmax_ = List(CFloat(), help='The minimum value of a feature.').tag(output=True)
    fmin_ = List(CFloat(), help='The maximum value of a feature.').tag(output=True)

    def fit(self, dataset):
        '''
        Fit MinMaxScaler to the dataset.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        self
        '''

        assert len(self.feature_range) == 2, 'feature_range must have 2 elements only'
        minmax = dataset.minmax(self.features)
        self.fmin_ = minmax[:, 0].tolist()
        self.fmax_ = minmax[:, 1].tolist()

    def transform(self, dataset):
        '''
        Transform a dataset with a fitted MinMaxScaler.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        :return copy: a shallow copy of the dataset that includes the scaled features.
        '''

        copy = dataset.copy()

        for i in range(len(self.features)):
            name = self.prefix + self.features[i]
            a = self.feature_range[0]
            b = self.feature_range[1]
            expr = copy[self.features[i]]
            expr = (b-a)*(expr-self.fmin_[i])/(self.fmax_[i]-self.fmin_[i]) + a
            copy[name] = expr
        return copy


@register
@generate.register
class MaxAbsScaler(Transformer):
    ''' Scale features by their maximum absolute value.

    Example:
    --------

    >>> import vaex.ml
    >>> df = vaex.ml.datasets.load_iris()
    >>> features = ['sepal_width', 'petal_length', 'sepal_length', 'petal_width']
    >>> df_train, df_test = vaex.ml.train_test_split(df)
    >>> scaler = vaex.ml.MaxAbsScaler(features=features)
    >>> df_train = scaler.fit_transform(df_train)
    >>> df_test = scaler.transform(df_test)
    '''

    features = List(Unicode(), help=help_features).tag(ui='SelectMultiple')
    prefix = Unicode(default_value="absmax_scaled_", help=help_prefix).tag(ui='Text')
    absmax_ = List(CFloat(), help='Tha maximum absolute value of a feature.').tag(output=True)

    def fit(self, dataset):
        '''
        Fit MinMaxScaler to the dataset.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        self
        '''

        absmax = dataset.max(['abs(%s)' % k for k in self.features]).tolist()
        # Check if the absmax_ value is 0, in which case replace with 1
        self.absmax_ = [value if value != 0 else 1 for value in absmax]

    def transform(self, dataset):
        '''
        Transform a dataset with a fitted MaxAbsScaler.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        :return copy: a shallow copy of the dataset that includes the scaled features.
        '''

        copy = dataset.copy()
        for i in range(len(self.features)):
            name = self.prefix + self.features[i]
            expr = copy[self.features[i]]
            expr = expr / self.absmax_[i]
            copy[name] = expr
        return copy


@register
@generate.register
class RobustScaler(Transformer):
    ''' The RobustScaler removes the median and scales the data according to a
    given percentile range. By default, the scaling is done between the 25th and
    the 75th percentile. Centering and scaling happens independently for each
    feature (column).

    Example:
    --------

    >>> import vaex.ml
    >>> df = vaex.ml.datasets.load_iris()
    >>> features = ['sepal_width', 'petal_length', 'sepal_length', 'petal_width']
    >>> df_train, df_test = vaex.ml.train_test_split(df)
    >>> scaler = vaex.ml.RobustScaler(features=features, percentile_range=(25, 75))
    >>> df_train = scaler.fit_transform(df_train)
    >>> df_test = scaler.transform(df_test)
    '''

    features = List(Unicode(), help=help_features).tag(ui='SelectMultiple')
    with_centering = CBool(default_value=True, help='If True, remove the median.').tag(ui='Checkbox')
    with_scaling = CBool(default_value=True, help='If True, scale each feature between the specified percentile range.').tag(ui='Checkbox')
    percentile_range = Tuple(default_value=(25, 75), help='The percentile range to which to scale each feature to.').tag().tag(ui='FloatRangeSlider')
    prefix = Unicode(default_value="robust_scaled_", help=help_prefix).tag(ui='Text')
    center_ = List(CFloat(), default_value=None, help='The median of each feature.').tag(output=True)
    scale_ = List(CFloat(), default_value=None, help='The percentile range for each feature.').tag(output=True)

    def fit(self, dataset):
        '''
        Fit RobustScaler to the dataset.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        self
        '''

        # check the quantile range
        q_min, q_max = self.percentile_range
        if not 0 <= q_min <= q_max <= 100:
            raise ValueError('Invalid percentile range: %s' % (str(self.percentile_range)))

        if self.with_centering:
            self.center_ = dataset.percentile_approx(expression=self.features, percentage=50).tolist()

        if self.with_scaling:
            self.scale_ = (dataset.percentile_approx(expression=self.features, percentage=q_max) - dataset.percentile_approx(expression=self.features, percentage=q_min)).tolist()

    def transform(self, dataset):
        '''
        Transform a dataset with a fitted RobustScaler.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        :return copy: a shallow copy of the dataset that includes the scaled features.
        '''

        copy = dataset.copy()
        for i in range(len(self.features)):
            name = self.prefix+self.features[i]
            expr = copy[self.features[i]]
            if self.with_centering:
                expr = expr - self.center_[i]
            if self.with_scaling:
                expr = expr / self.scale_[i]
            copy[name] = expr
        return copy
try:
    from .autogen import transformations as _
    del _
except ImportError:
    pass
