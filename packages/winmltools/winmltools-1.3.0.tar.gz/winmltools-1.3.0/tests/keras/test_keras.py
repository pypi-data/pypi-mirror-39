import unittest
import keras
import onnx
import os

from .._utils import *

models_dir = os.path.dirname(os.path.abspath(__file__)) + '/../models'

class TestKeras(unittest.TestCase):
    def test_LSTM(self):
        model = keras.models.load_model(os.path.join(models_dir, 'keras', 'LSTM.keras'))
        result, _ = convert_model(model, 'keras-lstm')
        result_path = os.path.join(temp_model_path, 'keras-lstm.onnx')
        onnx.save_model(result, result_path)
        self.assertEqual(run_model(result_path), 0)

    def test_Conv2D(self):
        model = keras.models.load_model(os.path.join(models_dir, 'keras', 'Conv2D.keras'))
        result, _ = convert_model(model, 'keras-conv2d')
        result_path = os.path.join(temp_model_path, 'keras-conv2d.onnx')
        onnx.save_model(result, result_path)
        # TODO: Bug (7819) Failed to run this model with WinMLRunner
        #self.assertEqual(run_model(result_path), 0)

    def test_tanh(self):
        model = keras.models.load_model(os.path.join(models_dir, 'keras', 'tanh.keras'))
        result, _ = convert_model(model, 'keras-tanh')
        result_path = os.path.join(temp_model_path, 'keras-tanh.onnx')
        onnx.save_model(result, result_path)
        # TODO: Bug (7820) Failed to run this model with WinMLRunner
        #self.assertEqual(run_model(result_path), 0)
