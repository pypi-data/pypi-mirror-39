# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from .common import tf2onnx_installed, utils

from .. import __version__, __producer__

import onnxmltools
onnxmltools.__producer__ = __producer__
onnxmltools.__producer_version__  = __version__ 

def convert_sklearn(model, target_opset, name=None, initial_types=None, doc_string='',
                    custom_conversion_functions=None, custom_shape_calculators=None):
    '''
    This function produces an equivalent ONNX model of the given scikit-learn model. The supported scikit-learn
    modules are listed below.

    * Preprocessings and transformations:
      1.  feature_extraction.DictVectorizer
      2.  preprocessing.Imputer
      3.  preprocessing.LabelEncoder
      4.  preprocessing.Normalizer
      5.  preprocessing.OneHotEncoder
      6.  preprocessing.RobustScale
      7.  preprocessing.StandardScaler
      8.  decomposition.TruncatedSVD
    * Linear classification and regression:
      9.  svm.LinearSVC
      10. linear_model.LogisticRegression,
      11. linear_model.SGDClassifier
      12. svm.LinearSVR
      13. linear_model.LinearRegression
      14. linear_model.Ridge
      15. linear_model.SGDRegressor
      16. linear_model.ElasticNet
    * Support vector machine for classification and regression
      17. svm.SVC
      18. svm.SVR
      19. svm.NuSVC
      20. svm.NuSVR
    * Tree-based models for classification and regression
      21. tree.DecisionTreeClassifier
      22. tree.DecisionTreeRegressor
      23. ensemble.GradientBoostingClassifier
      24. ensemble.GradientBoostingRegressor
      25. ensemble.RandomForestClassifier
      26. ensemble.RandomForestRegressor
      27. ensemble.ExtraTreesClassifier
      28. ensemble.ExtraTreesRegressor
    * pipeline
      29. pipeline.Pipeline

    For pipeline conversion, user needs to make sure each component is one of our supported items (1)-(24).

    This function converts the specified scikit-learn model into its ONNX counterpart. Notice that for all conversions,
    initial types are required.  ONNX model name can also be specified.

    :param model: A scikit-learn model
    :param target_opset: operator set version for default ai.onnx namespace. Use 7 for Windows 10 October 2018 (17763), and 8 for Windows Insider builds greater than 17763.
    :param name: The name of the graph (type: GraphProto) in the produced ONNX model (type: ModelProto)
    :param initial_types: a python list. Each element is a tuple of a variable name and a type defined in data_types.py
    :param custom_conversion_functions: a dictionary for specifying the user customized conversion function
    :param custom_shape_calculators: a dictionary for specifying the user customized shape calculator
    :return: An ONNX model (type: ModelProto) which is equivalent to the input scikit-learn model

    Example of initial_types:
    Assume that the specified scikit-learn model takes a heterogeneous list as its input. If the first 5 elements are
    floats and the last 10 elements are integers, we need to specify initial types as below. The [1] in [1, 5] indicates
    the batch size here is 1.
    >>> from winmltools.convert.common.data_types import FloatTensorType, Int64TensorType
    >>> initial_type = [('float_input', FloatTensorType([1, 5])), ('int64_input', Int64TensorType([1, 10]))]
    '''
    if not utils.sklearn_installed():
        raise RuntimeError(
            'scikit-learn is not installed. Please install sci-kit learn to use this feature.')

    # import from onnxmltools
    from onnxmltools.convert.sklearn.convert import convert as _convert_sklearn

    # import from local sklearn to allow for overrides
    from . import sklearn
    return _convert_sklearn(model, target_opset=target_opset, name=name, initial_types=initial_types, doc_string=doc_string,
                            custom_conversion_functions=custom_conversion_functions, custom_shape_calculators=custom_shape_calculators)


def convert_coreml(model, target_opset, name=None, initial_types=None, doc_string='',
                   custom_conversion_functions=None, custom_shape_calculators=None):
    '''
    This function converts the specified CoreML model into its ONNX counterpart. Some information such as the produced
    ONNX model name can be specified.
    :param model: A CoreML model (https://apple.github.io/coremltools/coremlspecification/sections/Model.html#model) or
    a CoreML MLModel object
    :param target_opset: operator set version for default ai.onnx namespace. Use 7 for Windows 10 October 2018 (17763), and 8 for Windows Insider builds greater than 17763.
    :param name: The name of the graph (type: GraphProto) in the produced ONNX model (type: ModelProto)
    produced model. If ONNXMLTools cannot find a compatible ONNX python package, an error may be thrown.
    :param initial_types: A list providing some types for some root variables. Each element is a tuple of a variable
    name and a type defined in data_types.py.
    :param doc_string: A string attached onto the produced ONNX model
    :param custom_conversion_functions: a dictionary for specifying the user customized conversion function
    :param custom_shape_calculators: a dictionary for specifying the user customized shape calculator
    :return: An ONNX model (type: ModelProto) which is equivalent to the input CoreML model

    Example of initial types:
    Assume that 'A' and 'B' are two root variable names used in the CoreML model you want to convert. We can specify
    their types via
    >>> from winmltools.convert.common.data_types import FloatTensorType
    >>> initial_type = [('A', FloatTensorType([40, 12, 1, 1])), ('B', FloatTensorType([1, 32, 1, 1]))]
    '''
    if not utils.coreml_installed():
        raise RuntimeError(
            'coremltools is not installed. Please install coremltools to use this feature.')

    # import from onnxmltools
    from onnxmltools.convert.coreml.convert import convert as _convert_coreml

    # import from local coreml to allow for overrides
    from . import coreml
    return _convert_coreml(model, name=name, initial_types=initial_types, target_opset=target_opset, doc_string=doc_string,
                           custom_conversion_functions=custom_conversion_functions, custom_shape_calculators=custom_shape_calculators)


def convert_keras(model, target_opset, name=None, initial_types=None, doc_string='', default_batch_size=1,
                   channel_first_inputs=None, custom_conversion_functions=None, custom_shape_calculators=None):
    '''
    Convert Keras-Tensorflow Model and Sequence objects into Topology.
    :param model: A Keras model (Model or Sequence object)
    :param target_opset: operator set version for default ai.onnx namespace. Use 7 for Windows 10 October 2018 (17763), and 8 for Windows Insider builds greater than 17763.
    :param name: Optional graph name of the produced ONNX model
    :param initial_types: A list providing types for some input variables. Each element is a tuple of a variable name
    and a type defined in data_types.py.
    :param doc_string: A string attached onto the produced ONNX model
    :param default_batch_size: default batch size of produced ONNX model. If not set, it will be 1
    :param channel_first_inputs: specifies names of 4-D inputs which are forced to be in channel-first format
     (i.e., NCHW) in the converted model. It's a list of string; for example, ['input1', 'input2'].
    :param custom_conversion_functions: a dictionary for specifying the user customized conversion function
    :param custom_shape_calculators: a dictionary for specifying the user customized shape calculator
    :return: An ONNX model (type: ModelProto) which is equivalent to the input Keras model
    '''
    if not utils.keras_installed():
        raise RuntimeError(
            'Keras is not installed. Please install Keras (>=2.0.0) to use this feature.')

    # import from onnxmltools
    from onnxmltools.convert.keras.convert import convert as _convert_keras

    # import from local keras to allow for overrides
    from . import keras
    return _convert_keras(model, name=name, target_opset=target_opset, initial_types=initial_types, doc_string=doc_string,
                          default_batch_size=default_batch_size, channel_first_inputs=channel_first_inputs,
                          custom_conversion_functions=custom_conversion_functions, custom_shape_calculators=custom_shape_calculators)


def convert_lightgbm(model, target_opset, name=None, initial_types=None, doc_string='',
            custom_conversion_functions=None, custom_shape_calculators=None):
    '''
    This function produces an equivalent ONNX model of the given lightgbm model.
    The supported lightgbm modules are listed below.

    * LightGBM Python module
      1. LGBMClassifiers (http://lightgbm.readthedocs.io/en/latest/Python-API.html#lightgbm.LGBMClassifier)
      2. LGBMRegressor (http://lightgbm.readthedocs.io/en/latest/Python-API.html#lightgbm.LGBMRegressor)

    :param model: A lightgbm model
    :param target_opset: operator set version for default ai.onnx namespace. Use 7 for Windows 10 October 2018 (17763), and 8 for Windows Insider builds greater than 17763.
    :param initial_types: a python list. Each element is a tuple of a variable name and a type defined in data_types.py
    :param name: The name of the graph (type: GraphProto) in the produced ONNX model (type: ModelProto)
    :param doc_string: A string attached onto the produced ONNX model
    :param targeted_onnx: A string (for example, '1.1.2' and '1.2') used to specify the targeted ONNX version of the
    produced model. If ONNXMLTools cannot find a compatible ONNX python package, an error may be thrown.
    :param custom_conversion_functions: a dictionary for specifying the user customized conversion function
    :param custom_shape_calculators: a dictionary for specifying the user customized shape calculator
    :return: An ONNX model (type: ModelProto) which is equivalent to the input lightgbm model
    '''

    if not utils.lightgbm_installed():
        raise RuntimeError('lightgbm not installed. Please install lightgbm to use this feature.')
    from onnxmltools.convert.lightgbm import convert as _convert_lightgbm

    # import from local lightgbm to allow for overrides
    from . import lightgbm
    return _convert_lightgbm(model, target_opset=target_opset, name=name, initial_types=initial_types, doc_string=doc_string,
                             custom_conversion_functions=custom_conversion_functions, custom_shape_calculators=custom_shape_calculators)


def convert_libsvm(model, target_opset=8, name=None, initial_types=None, **kwarg):
    if not utils.libsvm_installed():
        raise RuntimeError(
            'libsvm is not installed. Please install libsvm to use this feature.')
    from .libsvm.convert import convert
    # not using target_opset for libsvm convert since the converter is only generating operators in ai.onnx.ml domain
    # but just passing in target_opset for consistency
    return convert(model, name=name, initial_types=initial_types, **kwarg)


def convert_xgboost(model, target_opset=8, name=None, initial_types=None, **kwarg):
    if not utils.xgboost_installed():
        raise RuntimeError(
            'xgboost not installed or not recent enough. Please install xgboost from github to use this feature.')
    from .xgboost.convert import convert
    # not using target_opset for libsvm convert since the converter is only generating operators in ai.onnx.ml domain
    # but just passing in target_opset for consistency
    return convert(model, name=name, initial_types=initial_types, **kwarg)


def convert_tensorflow(graph, target_opset, name=None, continue_on_error=False, verbose=False, target=None,
                       custom_op_handlers=None, custom_rewriter=None, extra_opset=None, shape_override=None,
                       inputs_as_nchw=None, output_names=None):
    """Convert tensorflow graph to onnx graph.
        Args:
            :param tf_graph: tensorflow graph
            :param target_opset: operator set version for default ai.onnx namespace. Use 7 for Windows 10 October 2018 (17763), and 8 for Windows Insider builds greater than 17763.
            :param continue_on_error: if an op can't be processed (aka there is no mapping), continue
            :param verbose: print summary stats
            :param target: list of workarounds applied to help certain platforms
            :param custom_op_handlers: dictionary of custom ops handlers
            :param custom_rewriter: list of custom graph rewriters
            :param extra_opset: list of extra opset's, for example the opset's used by custom ops
            :param shape_override: dict with inputs that override the shapes given by tensorflow
            :param inputs_as_nchw: transpose inputs in list from nchw to nchw
            :param output_names: name of output nodes in graph
    """
    try:
        import tensorflow
    except ImportError:
        raise RuntimeError(
            'Need Tensorflow python packages installed to enable its converter.'
        )

    if not tf2onnx_installed():
        raise RuntimeError(
            'tf2onnx not installed. Please install tf2onnx to use this feature.')

    import tf2onnx
    g = tf2onnx.tfonnx.process_tf_graph(graph, continue_on_error=continue_on_error, verbose=verbose, target=target,
                                        opset=target_opset, custom_op_handlers=custom_op_handlers, custom_rewriter=custom_rewriter,
                                        extra_opset=extra_opset, shape_override=shape_override, inputs_as_nchw=inputs_as_nchw, output_names=output_names)
    doc = 'converted_from {}'.format(name) if name is not None else ''
    model_proto = g.make_model(doc)
    model_proto.producer_version = __version__
    model_proto.producer_name = __producer__

    return model_proto
