import coremltools
import keras
import unittest
import onnxmltools
import winmltools
import os
import tensorflow as tf

data_path = "\\\\redmond\\1windows\\TestContent\\CORE\\SiGMa\\GRFX\\WinML\\models"

class OpsetTest(unittest.TestCase):
    def _verify_opset_version(self, input_model, convert_fn, required_opset, **kwarg):
        for opset_version in [1, 7, 8]:
            if opset_version < required_opset:
                self.assertRaises(RuntimeError, convert_fn, input_model, 'name', target_opset=opset_version, **kwarg)
            else:
                model = convert_fn(input_model, opset_version, 'name', **kwarg)
                filtered = list(filter(lambda op: op.domain == '' or op.domain == 'ai.onnx', model.opset_import))
                try:
                    opset = filtered[0]
                except IndexError:
                    self.fail('Could not find an ai.onnx domain opset from model {}'.format(model.model))
                # Actual opset version should be equal to the expected version.
                print('opset version: ' + str(opset.version))
                self.assertTrue(opset.version <= opset_version)


    def test_coreml(self):
        path = os.path.join(data_path, "coreml", "keras2coreml_MNIST.mlmodel")
        model = coremltools.models.MLModel(path)
        self._verify_opset_version(model, winmltools.convert_coreml, 1)


    def test_keras(self):
        path = os.path.join(data_path, "keras", "keras_Subtract_ImageNet.keras")
        model = keras.models.load_model(path)
        self._verify_opset_version(model, winmltools.convert_keras, 1)


    def test_insufficient_opset(self):
        path = os.path.join(data_path, "keras", "keras_elu_ImageNet.keras")
        model = keras.models.load_model(path)
        self._verify_opset_version(model, winmltools.convert_keras, 1)

if __name__ == '__main__':
    unittest.main()
