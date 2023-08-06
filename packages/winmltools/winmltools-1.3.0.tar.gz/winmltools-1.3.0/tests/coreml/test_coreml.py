import unittest
import coremltools
import onnx
import os

from .._utils import *

models_dir = os.path.dirname(os.path.abspath(__file__)) + '/../models'

class TestKeras(unittest.TestCase):
    def test_LSTM(self):
        model = coremltools.models.MLModel(os.path.join(models_dir, 'coreml', 'LSTM.mlmodel'))
        result, _ = convert_model(model, 'coreml-lstm')
        result_path = os.path.join(temp_model_path, 'coreml-lstm.onnx')
        onnx.save_model(result, result_path)
        self.assertEqual(run_model(result_path), 0)

    def test_mnist(self):
        model = coremltools.models.MLModel(os.path.join(models_dir, 'coreml', 'mnist.mlmodel'))
        result, _ = convert_model(model, 'coreml-mnist')
        result_path = os.path.join(temp_model_path, 'coreml-mnist.onnx')
        onnx.save_model(result, result_path)
        # TODO: Bug (7819) Failed to run this model with WinMLRunner
        self.assertEqual(run_model(result_path), 0)

    def test_simple_RNN(self):
        model = coremltools.models.MLModel(os.path.join(models_dir, 'coreml', 'SimpleRNN.mlmodel'))
        result, _ = convert_model(model, 'coreml-rnn')
        result_path = os.path.join(temp_model_path, 'coreml-rnn.onnx')
        onnx.save_model(result, result_path)
        # TODO: Bug (7820) Failed to run this model with WinMLRunner
        self.assertEqual(run_model(result_path), 0)