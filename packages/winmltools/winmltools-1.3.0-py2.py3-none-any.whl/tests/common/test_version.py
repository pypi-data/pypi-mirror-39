import coremltools
import keras
import unittest
import onnxmltools
import winmltools
import os
import tensorflow as tf

data_path = "\\\\redmond\\1windows\\TestContent\\CORE\\SiGMa\\GRFX\\WinML\\models"

class VersionTest(unittest.TestCase):
    def test_producer_version(self):
        path = os.path.join(data_path, "coreml", "keras2coreml_MNIST.mlmodel")
        model = coremltools.models.MLModel(path)
        converted = winmltools.convert.convert_coreml(model, 8)
        self.assertEqual(converted.producer_name, winmltools.__producer__)
        self.assertEqual(converted.producer_version, winmltools.__version__)
    
if __name__ == '__main__':
    unittest.main()
