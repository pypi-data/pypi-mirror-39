import os 
import subprocess

from onnxmltools.utils.tests_helper import dump_binary_classification, dump_multiple_classification
import onnxmltools.utils


def convert_model(model, name=None, input_types=None, opset=8):
    """
    This function is to override onnxmltool's test helper to convert a model

    :param model: model, *scikit-learn*, *keras*, or *coremltools* object
    :return: *onnx* model
    """
    
    from sklearn.base import BaseEstimator
    from xgboost import XGBRegressor, XGBClassifier
    from svm import svm_model
    if model.__class__.__name__.startswith("LGBM"):
        from winmltools.convert import convert_lightgbm
        model = convert_lightgbm(model, opset, name=name, initial_types=input_types), 'lgbm'
    elif isinstance(model, XGBRegressor) or isinstance(model, XGBClassifier):
        from winmltools.convert import convert_xgboost
        model = convert_xgboost(model, opset, name=name, initial_types=input_types), 'xgboost'
    elif isinstance(model, svm_model):
        from winmltools.convert import convert_libsvm
        model = convert_libsvm(model, opset, name=name, initial_types=input_types), 'libsvm'
    elif isinstance(model, BaseEstimator):
        from winmltools.convert import convert_sklearn
        model = convert_sklearn(model, opset, name=name, initial_types=input_types), 'sklearn'
    else:
        from keras.models import Model
        if isinstance(model, Model):
            from winmltools.convert import convert_keras
            model = convert_keras(model, opset, name=name, initial_types=input_types), 'keras'
        else:
            from winmltools.convert import convert_coreml
            model = convert_coreml(model, opset, name=name, initial_types=input_types), 'coreml'
    if model is None:
        raise RuntimeError("Unable to convert model of type '{0}'.".format(type(model)))
    return model


def run_model(model_path):
    '''
        This function is to run onnx model from the given path using WinMLRunner.
        TODO: Implement onnx backend for WinML
    '''
    if os.environ.get('WINML_RUNNER_PATH') is None:
        raise RuntimeError('WINML_RUNNER_PATH is missing')
    winml_runner_path = os.environ['WINML_RUNNER_PATH']
    return subprocess.call([winml_runner_path, '-model', model_path])


temp_model_path = os.path.join(os.path.abspath('.'), 'temp', 'models')

if not os.path.isdir(temp_model_path):
    os.makedirs(temp_model_path)

onnxmltools.utils.tests_helper.convert_model = convert_model

