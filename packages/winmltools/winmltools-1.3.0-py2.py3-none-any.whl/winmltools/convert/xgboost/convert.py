#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

"""
Main file for ONNX converter for XGBoost models.
"""
from onnxmltools.convert.common.data_types import *
from ...proto import onnx_proto
from ..common import get_converter
from ..common import ModelBuilder
from ..common import model_util
from .XGBoostConvertContext import XGBoostConvertContext as ConvertContext

# These are not referenced directly but are imported
# to initialize the registration call.
from .XGBoostConverter import XGBRegressorConverter


def convert(model, name=None, initial_types=None):
    """
    Converts a :pkg:`XGBoost` model into ONNX.
    
    :param model: trained model (object, not filename)
    :param name: model name
    :param initial_types: specify input features
    :return: ONNX model.
    
    Example:
    
    ::
    
        from sklearn import datasets
        iris = datasets.load_iris()
        X = iris.data[:, :2]
        y = iris.target
        
        from xgboost import XGBClassifier
        clf = XGBClassifier()
        clf.fit(X, y)
        
        from winmltools.convert.xgboost import convert
        converted_model = convert(clf)
    """
    context = ConvertContext()

    nodes = []
    inputs = [model_util.make_tensor_value_info(context.get_unique_name('input'), onnx_proto.TensorProto.FLOAT)]
    if initial_types:
        inputs = []
        try:
            for input_name, input_type in initial_types:
                input_shape = input_type.shape
                if isinstance(input_type, (Int64TensorType, Int64Type)):
                    elem_type = model_util.tensorproto_typemap['int64']
                elif isinstance(input_type, (FloatTensorType, FloatType)):
                    elem_type = model_util.tensorproto_typemap['float']
                elif isinstance(input_type, (StringTensorType, StringType)):
                    elem_type = model_util.tensorproto_typemap['string']
                else:
                    raise RuntimeError('Unknown input type')
                inputs.append(model_util.make_tensor_value_info(context.get_unique_name(input_name),
                                                                elem_type, input_shape))
            if len(initial_types) > 1:
                nodes.append(_create_feature_vectorizer_node(context, inputs))
                inputs = nodes[-1].outputs
        except Exception as e:
            raise ValueError('Invalid initial_types argument.') from e
    else:
        raise ValueError('Specify model input names and  types when calling this convert(...) function')

    converter = get_converter(type(model))    

    nodes += converter.convert(context, model, inputs)
    mb = ModelBuilder(name)
    for node in nodes:
        mb.add_nodes([node.onnx_node])
        mb.add_initializers(node.initializers)
        mb.add_values(node.values)
        mb.add_domain_version_pair(node.domain_version_pair)

    mb.add_inputs(inputs)
    if len(context.outputs) > 0:
        mb.add_outputs(context.outputs)
    else:
        mb.add_outputs(nodes[-1].outputs)
    return mb.make_model()
