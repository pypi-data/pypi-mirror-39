import unittest
import sklearn
from sklearn import datasets
from sklearn import linear_model
import winmltools
from .._utils import run_model, temp_model_path
import numpy as np
import onnx
from lightgbm import LGBMClassifier, LGBMRegressor
from onnxmltools.utils.tests_helper import dump_binary_classification, dump_multiple_classification, dump_single_regression

from winmltools.convert.common.data_types import FloatTensorType, Int64TensorType

import os

class TestLightGbm(unittest.TestCase):
    def test_classifier(self):
        model = LGBMClassifier(n_estimators=3, min_child_samples=1)
        dump_binary_classification(model, folder=temp_model_path)
        dump_multiple_classification(model, folder=temp_model_path)
        run_model(os.path.join(temp_model_path, 'lgbmBinLGBMClassifier.model.onnx'))
        run_model(os.path.join(temp_model_path, 'lgbmMclLGBMClassifier.model.onnx'))

    def test_regressor(self):
        model = LGBMRegressor(n_estimators=3, min_child_samples=1)
        dump_single_regression(model, folder=temp_model_path)
        run_model(os.path.join(temp_model_path, 'lgbmRegLGBMRegressor.model.onnx'))
