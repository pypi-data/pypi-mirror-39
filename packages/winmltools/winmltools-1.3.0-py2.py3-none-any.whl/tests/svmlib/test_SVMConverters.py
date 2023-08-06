"""
Tests scikit-linear converter.
"""
import svm
import numpy as np
import unittest
from sklearn.datasets import load_iris
from svm import PRINT_STRING_FUN, print_null, C_SVC as SVC, EPSILON_SVR as SVR, NU_SVC as NuSVC, NU_SVR as NuSVR
import svmutil
from winmltools.convert.common.data_types import FloatTensorType
import os
import onnx

from .._utils import *


noprint = PRINT_STRING_FUN(print_null)


class TestSvmLibSVM(unittest.TestCase):
    def test_convert_svmc_linear(self):
        iris = load_iris()

        X = iris.data[:, :2]
        y = iris.target
        y[y == 2] = 1
        
        prob = svmutil.svm_problem(y, X.tolist())        

        param = svmutil.svm_parameter()
        param.svm_type = SVC
        param.kernel_type = svmutil.LINEAR
        param.eps = 1
        param.probability = 1
        param.print_func = noprint
        
        libsvm_model = svmutil.svm_train(prob, param)

        node, _ = convert_model(libsvm_model, input_types=[('input', FloatTensorType(shape=[1, 'None']))])
        model_path = os.path.join(temp_model_path, 'smvc-linear.onnx')
        onnx.save_model(node, model_path)
        self.assertEqual(run_model(model_path), 0)

    def test_convert_svmc(self):
        iris = load_iris()

        X = iris.data[:, :2]
        y = iris.target
        y[y == 2] = 1
        
        prob = svmutil.svm_problem(y, X.tolist())        

        param = svmutil.svm_parameter()
        param.svm_type = SVC
        param.kernel_type = svmutil.RBF
        param.eps = 1
        param.probability = 1
        param.print_func = noprint
        
        libsvm_model = svmutil.svm_train(prob, param)

        node, _ = convert_model(libsvm_model, input_types=[('input', FloatTensorType(shape=[1, 'None']))])
        model_path = os.path.join(temp_model_path, 'smvc.onnx')
        onnx.save_model(node, model_path)
        self.assertEqual(run_model(model_path), 0)

    def test_convert_svmr_linear(self):
        iris = load_iris()

        X = iris.data[:, :2]
        y = iris.target
        prob = svmutil.svm_problem(y, X.tolist())        
                
        param = svmutil.svm_parameter()
        param.svm_type = SVR
        param.kernel_type = svmutil.LINEAR
        param.eps = 1
        param.print_func = noprint

        libsvm_model = svmutil.svm_train(prob, param)

        node, _ = convert_model(libsvm_model, input_types=[('input', FloatTensorType(shape=[1, 'None']))])
        model_path = os.path.join(temp_model_path, 'svmr-linear.onnx')
        onnx.save_model(node, model_path)
        self.assertEqual(run_model(model_path), 0)

    def test_convert_svmr(self):
        iris = load_iris()

        X = iris.data[:, :2]
        y = iris.target
        prob = svmutil.svm_problem(y, X.tolist())        
                
        param = svmutil.svm_parameter()
        param.svm_type = SVR
        param.kernel_type = svmutil.RBF
        param.probability = 1
        param.eps = 1
        param.print_func = noprint

        libsvm_model = svmutil.svm_train(prob, param)

        node, _ = convert_model(libsvm_model, input_types=[('input', FloatTensorType(shape=[1, 'None']))])
        model_path = os.path.join(temp_model_path, 'svmr.onnx')
        onnx.save_model(node, model_path)
        self.assertEqual(run_model(model_path), 0)

    def test_convert_nusvmr(self):
        iris = load_iris()

        X = iris.data[:, :2]
        y = iris.target
        y[y == 2] = 1
        prob = svmutil.svm_problem(y, X.tolist())        
                
        param = svmutil.svm_parameter()
        param.svm_type = NuSVR
        param.kernel_type = svmutil.RBF
        param.eps = 1
        param.print_func = noprint

        libsvm_model = svmutil.svm_train(prob, param)

        node, _ = convert_model(libsvm_model, input_types=[('input', FloatTensorType(shape=[1, 'None']))])
        model_path = os.path.join(temp_model_path, 'nusvmr.onnx')
        onnx.save_model(node, model_path)
        self.assertEqual(run_model(model_path), 0)

    def test_convert_nusvmc(self):
        iris = load_iris()

        X = iris.data[:, :2]
        y = iris.target
        y[y == 2] = 1
        
        prob = svmutil.svm_problem(y, X.tolist())        

        param = svmutil.svm_parameter()
        param.svm_type = NuSVC
        param.kernel_type = svmutil.RBF
        param.eps = 1
        param.probability = 1
        param.print_func = noprint
        param.print_func = noprint
        
        libsvm_model = svmutil.svm_train(prob, param)

        node, _ = convert_model(libsvm_model, input_types=[('input', FloatTensorType(shape=[1, 'None']))])
        model_path = os.path.join(temp_model_path, 'nusvmc.onnx')
        onnx.save_model(node, model_path)
        self.assertEqual(run_model(model_path), 0)

if __name__ == '__main__':
    unittest.main()
