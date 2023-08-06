"""
Tests scilit-learn's tree-based methods' converters.
"""
import pickle
import onnx
import os
import unittest
from sklearn.datasets import load_iris
from xgboost import XGBRegressor, XGBClassifier
from winmltools.convert import convert_xgboost

from winmltools.convert.common.data_types import FloatTensorType
from .._utils import convert_model, run_model, temp_model_path

class TestXGBoostModels(unittest.TestCase):
    
    def test_xgb_regressor(self):
        iris = load_iris()
        X = iris.data[:, :2]
        y = iris.target

        xgb = XGBRegressor()
        xgb.fit(X, y)
        conv_model, _ = convert_model(xgb, input_types=[('input', FloatTensorType(shape=[1, 'None']))])
        model_path = os.path.join(temp_model_path, 'XGBRegressor.onnx')
        onnx.save_model(conv_model, model_path)
        self.assertEqual(run_model(model_path), 0)
        
        
    def test_xgb_classifier(self):
        iris = load_iris()
        X = iris.data[:, :2]
        y = iris.target
        y[y == 2] = 0

        xgb = XGBClassifier()
        xgb.fit(X, y)
        conv_model, _ = convert_model(xgb, input_types=[('input', FloatTensorType(shape=[1, 'None']))])
        model_path = os.path.join(temp_model_path, 'XGBClassifier.onnx')
        onnx.save_model(conv_model, model_path)
        self.assertEqual(run_model(model_path), 0)
 
    def test_xgb_classifier_multi(self):
        iris = load_iris()
        X = iris.data[:, :2]
        y = iris.target

        xgb = XGBClassifier()
        xgb.fit(X, y)
        conv_model, _ = convert_model(xgb, input_types=[('input', FloatTensorType(shape=[1, 'None']))])
        model_path = os.path.join(temp_model_path, 'XGBClassifier-multi.onnx')
        onnx.save_model(conv_model, model_path)
        self.assertEqual(run_model(model_path), 0)


    def test_xgboost_unpickle_06(self):
        # Unpickle a model trained with an old version of xgboost.
        this = os.path.dirname(__file__)
        with open(os.path.join(this, "xgboost10day.pickle.dat"), "rb") as f:
            xgb = pickle.load(f)
        
        conv_model, _ = convert_model(xgb, input_types=[('features', FloatTensorType([1, 10000]))])
        model_path = os.path.join(temp_model_path, 'XGBClassifier-multi.onnx')
        onnx.save_model(conv_model, model_path)
        self.assertEqual(run_model(model_path), 0)

if __name__ == '__main__':
    unittest.main()
                