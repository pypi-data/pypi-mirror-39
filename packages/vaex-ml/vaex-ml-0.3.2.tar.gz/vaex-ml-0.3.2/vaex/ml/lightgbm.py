import os
import ctypes
import math

import vaex
import lightgbm
import numpy as np
import tempfile
import base64
import vaex.serialize
from . import state
import traitlets

from . import generate

#libpath = os.path.join(os.path.dirname(__file__), "vaex_ml_lib.cpython-35m-x86_64-linux-gnu.so")
#print(libpath)
#lib = ctypes.cdll.LoadLibrary(libpath)
lib = lightgbm.basic._LIB

class EXPRESSION_RESULT(ctypes.Structure):
     _fields_ = [
         ("length", ctypes.c_longlong),
         ("data", ctypes.POINTER(ctypes.c_float))
     ]

EVALFUNC = ctypes.CFUNCTYPE(ctypes.c_int, (ctypes.c_char_p), ctypes.c_longlong, ctypes.c_longlong, ctypes.POINTER(EXPRESSION_RESULT))

@vaex.serialize.register
@generate.register
class LightGBMModel(state.HasState):
    '''The LightGBM algorithm.

    This class provides an interface to the LightGBM aloritham, with some optimizations
    for better memory efficiency when training large datasets. The algorithm itself is
    not modified at all.

    LightGBM is a fast gradient boosting algorithm based on decision trees and is
    mainly used for classification, regression and ranking tasks. It is under the
    umbrella of the Distributed Machine Learning Toolkit (DMTK) project of Microsoft.
    For more information, please visit https://github.com/Microsoft/LightGBM/.

    Example:
    --------

    import vaex.ml.
    >>> import vaex.ml.lightgbm
    >>> df = vaex.ml.datasets.load_iris()
    >>> features = ['sepal_width', 'petal_length', 'sepal_length', 'petal_width']
    >>> df_train, df_test = vaex.ml.train_test_split(df)
    >>> params = {
        'boosting': 'gbdt',
        'max_depth': 5,
        'learning_rate': 0.1,
        'application': 'multiclass',
        'num_class': 3,
        'subsample': 0.80,
        'colsample_bytree': 0.80}
    >>> booster = vaex.ml.lightgbm.LightGBMModel(features=features, num_rounds=100, param=params)
    >>> booster.fit(df_train, 'class_')
    >>> df_train = booster.transform(df_train)
    >>> df_test = booster.transform(df_test)
    '''

    features = traitlets.List(traitlets.Unicode(), help='List of features to use when fitting the LightGBMModel.')
    num_round = traitlets.CInt(help='Number of boosting iterations.')
    param = traitlets.Dict(help='parameters to be passed on the to the LightGBM model.')
    prediction_name = traitlets.Unicode(default_value='lightgbm_prediction', help='The name of the virtual column housing the predictions.')


    def __call__(self, *args):
        data2d = np.vstack([arg.astype(np.float64) for arg in args]).T.copy()
        #dmatrix = lightgbm.Dataset(data2d)
        return self.bst.predict(data2d)

    def transform(self, dataset):
        '''
        Transform the dataset such that it contains the predictions of the LightGBMModel
        in a form of a virtual columns.

        Parameters:
        -----------
        :param dataset: A vaex dataset.

        Returns:
        --------
        :return copy: A shallow copy of the dataset that includes the LightGBMModel predictions as virtual columns.
        '''

        copy = dataset.copy()
        lazy_function = copy.add_function('lightgbm_prediction_function', self)
        expression = lazy_function(*self.features)
        copy.add_virtual_column(self.prediction_name, expression, unique=False)
        return copy

    def fit(self, dataset, label, copy=False):
        '''
        Fit the LightGBMModel to the dataset.

        Parameters:
        -----------
        :param dataset: A vaex dataset.
        :param label: The name of the column containing the target variable.
        :param copy: bool, if True, make an in memory copy of the data before passing it to the LightGBMModel.

        Returns:
        --------
        self
        '''
        if copy:
            data = np.vstack([dataset.evaluate(k).astype(np.float64) for k in self.features]).T
            label_data = dataset.evaluate(label)
            dtrain = lightgbm.Dataset(data, label_data)
        else:
            dtrain = VaexDataset(dataset, label, features=self.features)
        param = dict(self.param)
        self.bst = lightgbm.train(param, dtrain, self.num_round)

    def predict(self, dataset, copy=False):
        '''Get an in-memory numpy array with the predictions of the LightGBMModel on
        a vaex dataset

        Parameters:
        -----------
        :param dataset: A vaex dataset.
        :param copy: bool, if True, make an in memory copy of the data before passing it to the LightGBMModel.

        Returns:
        --------
        A in-memory numpy array containing the LightGBMModel predictions.
        '''

        # TODO: we want to go multithreaded/parallel/chunks
        data = np.vstack([dataset.evaluate(k) for k in self.features]).T
        # if copy:
        #   data = np.vstack([dataset.evaluate(k) for k in self.features]).T
        #   dmatrix = lightgbm.Dataset(data)
        # else:
        #   dmatrix = VaexDMatrix(dataset, features=self.features)
        return self.bst.predict(data)

    def state_get(self):
        filename = tempfile.mktemp()
        self.bst.save_model(filename)
        with open(filename, 'rb') as f:
            data = f.read()
        return dict(tree_state=base64.encodebytes(data).decode('ascii'),
            substate=super(LightGBMModel, self).state_get())

    def state_set(self, state):
        super(LightGBMModel, self).state_set(state['substate'])
        data = base64.decodebytes(state['tree_state'].encode('ascii'))
        filename = tempfile.mktemp()
        with open(filename, 'wb') as f:
            f.write(data)
        self.bst = lightgbm.Booster(model_file=filename)

@vaex.serialize.register
@generate.register
class LightGBMClassifier(LightGBMModel):
    def __call__(self, *args):
        return np.argmax(super(LightGBMClassifier, self).__call__(*args), axis=1)
    def predict(self, dataset, copy=False):
        return np.argmax(super(LightGBMClassifier, self).predict(dataset, copy=copy), axis=1)


class VaexDataset(lightgbm.Dataset):
    def __init__(self, ds, label=None, features=None, blocksize=100*1000, sample_count=10*100, params={}):
        super(VaexDataset, self).__init__(None)
        self.ds = ds
        self.features = features or self.ds.get_column_names(virtual=True)
        assert len(set(self.features)) == len(self.features), "using duplicate features"
        self.blocksize = blocksize

        self.data_references = {}

        self.c_features = (ctypes.c_char_p * len(self.features))()
        self.c_features[:] = [k.encode() for k in self.features]

        self.c_evaluate = EVALFUNC(self.evaluate)

        self.handle = ctypes.c_void_p()

        row_count = len(self.ds)
        ncol = len(self.features)
        num_sample_row = min(sample_count, row_count)

        data_list = [self.ds.evaluate(k, i1=0, i2=num_sample_row).astype(np.float64) for k in self.features]
        data_pointers = [k.ctypes.data_as(ctypes.POINTER(ctypes.c_double)) for k in data_list]
        sample_data = (ctypes.POINTER(ctypes.c_double) * ncol)(*data_pointers)

        indices = np.arange(num_sample_row, dtype=np.int32)
        indices_pointers = [indices.ctypes.data_as(ctypes.POINTER(ctypes.c_int)) for k in range(ncol)]
        sample_indices = (ctypes.POINTER(ctypes.c_int) * ncol)(*indices_pointers)
        num_per_col = (ctypes.c_int * ncol)(*((num_sample_row,) * ncol))
        parameters = ctypes.c_char_p(lightgbm.basic.param_dict_to_str(params).encode())

        lightgbm.basic._safe_call(lib.LGBM_DatasetCreateFromSampledColumn(sample_data,
                                                sample_indices,
                                                ctypes.c_uint(ncol),
                                                num_per_col,
                                                ctypes.c_uint(num_sample_row),
                                                ctypes.c_uint(row_count),
                                                parameters,
                                                ctypes.byref(self.handle)))
        #self._push_rows()
        #print(">>>", self.num_data())
        blocks = int(math.ceil(row_count / blocksize))
        #print(blocks)
        dtype = np.float64
        for i in range(blocks):
            i1 = i * blocksize
            i2 = min(row_count, (i+1) * blocksize)
            data = np.array([ds.evaluate(k, i1=i1, i2=i2).astype(dtype) for k in features]).T.copy()
            #print(data.shape)
            ctypemap = {np.float64: ctypes.c_double, np.float32: ctypes.c_float}
            capi_typemap = {np.float64: lightgbm.basic.C_API_DTYPE_FLOAT64, np.float32:lightgbm.basic.C_API_DTYPE_FLOAT32}
            lightgbm.basic._safe_call(lib.LGBM_DatasetPushRows(self.handle,
                                     data.ctypes.data_as(ctypes.POINTER(ctypemap[dtype])),
                                     ctypes.c_uint(capi_typemap[dtype]),
                                     ctypes.c_uint32(i2-i1),
                                     ctypes.c_uint32(ncol),
                                     ctypes.c_uint32(i1),
                                     ))

        #return_code = lib.create_dmatrix(self.c_features, len(self.features), rows, batch_size, self.c_evaluate, self.blocksize, ctypes.byref(self.handle))
        #print(return_code)
        ##lib.test_dmatrix(self.handle, 0)
        if label is not None:
            self.label_data = self.ds.evaluate(label)
            #$self.set_label_npy2d(label)
            self.set_label(self.label_data)


    def set_label_npy2d(self, label):
        """Set label of dmatrix

        Parameters
        ----------
        label: array like
            The label information to be set into DMatrix
            from numpy 2D array
        """
        self.set_float_info_npy2d('label', label)

    def set_float_info_npy2d(self, field, data):
        """Set float type property into the DMatrix
           for numpy 2d array input

        Parameters
        ----------
        field: str
            The field name of the information

        data: numpy array
            The array of data to be set
        """
        data = np.array(data, copy=False, dtype=np.float32)
        c_data = data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        lightgbm.core._check_call(lightgbm.core._LIB.XGDMatrixSetFloatInfo(self.handle,
                                               lightgbm.core.c_str(field),
                                               c_data,
                                               ctypes.c_uint64(len(data))))

    def evaluate(self, expression, i1, i2, result):
        try:
            expression = expression.decode()
            #print(expression, i1, i2)
            #print(result[0])
            data = self.ds.evaluate(expression, i1, i2) # TODO, support selections
            # keep a reference, since otherwise the memory is freed
            # and we overwrite the last reference, so that will be freed
            self.data_references[expression] = data = data.astype(np.float32) # TODO: think about masking, nan?
            #print(data, type(data), data.dtype)
            ptr = data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            #print(ptr, ptr)
            result[0].length = len(data)
            result[0].data = ptr
            #print(result.data, result.length)
            #print(result)
            return 0 #EXPRESSION_RESULT(len(data), ptr)
        except (Exception, e):
            print('error', e)
try:
    from .autogen import lightgbm as _
    del _
except ImportError:
    pass

if __name__ == "__main__":
    ds = vaex.ml.iris()
    features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    #lds = VaexDataset(ds, 'class_', features=features)
    lds = lightgbm.Dataset(np.array(ds[features]), ds.data.class_)
    param = {'num_leaves':31, 'num_trees':100, 'objective':'softmax', 'num_class': 3}
    num_round=30
    bst = lightgbm.train(param, lds, num_round)
    print(bst.predict(np.array(ds[features])))

