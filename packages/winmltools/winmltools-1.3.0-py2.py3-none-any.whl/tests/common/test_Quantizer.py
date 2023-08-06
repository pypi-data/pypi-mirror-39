import unittest
import winmltools
from onnxmltools.proto import onnx_proto
import onnx
import os
import subprocess
import random
from .._utils import *

share = '\\\\redmond\\1windows\\TestContent\\CORE\\SiGMa\\GRFX\\WinML\\RS5\\models\\onnx-1.3'

class QuantizerTest(unittest.TestCase):
    def _verify_smaller(self, model_path, quantized_model_path):
        '''
           verify that model is smaller than before
        '''
        model_size = os.path.getsize(model_path)
        quantized_size = os.path.getsize(quantized_model_path)
        print('{} size: {} bytes'.format(model_path, model_size))
        print('{} size: {} bytes'.format(quantized_model_path, quantized_size))
        self.assertTrue(model_size > quantized_size)

    def _verify_quantize_model(self, model, name):
        if not os.path.isdir(temp_model_path):
            os.makedirs(temp_model_path)
        model_path = os.path.join(temp_model_path, name + '.onnx')
        dq_path = os.path.join(temp_model_path, name + '-quantized.onnx')
        csm_path = os.path.join(temp_model_path, name + '-quantized-csm.onnx')

        onnx.save_model(model, model_path)
        quantized_dq = winmltools.utils.quantize(model, use_dequantize_linear=True)
        quantized_csm = winmltools.utils.quantize(model, use_dequantize_linear=False)
        onnx.save_model(quantized_dq, dq_path)
        onnx.save_model(quantized_csm, csm_path)

        self._verify_smaller(model_path, dq_path)
        self._verify_smaller(model_path, csm_path)
        self.assertEqual(run_model(dq_path), 0)
        self.assertEqual(run_model(csm_path), 0)


    def test_dequantize_linear(self):
        '''
            Testing DequantizeLinear operator weight packing
        '''
        resnet_model_path = share + '\\coreml_MNIST.onnx'
        quantized_result_path = os.path.join(temp_model_path, 'coreml_MNIST-dq.onnx')
        if not os.path.isdir(temp_model_path):
            os.makedirs(temp_model_path)
        model = onnx.load_model(resnet_model_path)
        quantized_model = winmltools.utils.quantize(model, per_channel=True, nbits=8, use_dequantize_linear=True)
        onnx.save(quantized_model, quantized_result_path)

        # verify that the model contains com.microsoft opset with version >= 1
        opset = next((opset for opset in quantized_model.opset_import if opset.domain == 'com.microsoft' and opset.version >= 1), None)
        self.assertFalse(opset is None)
        # verify that model is smaller than before
        self._verify_smaller(resnet_model_path, quantized_result_path)
        # verify that you can run the quantized model
        self.assertEqual(run_model(quantized_result_path), 0)

    def test_csm(self):
        '''
            Testing cast-sub-mul operator weight packing
        '''
        resnet_model_path = share + '\\coreml_MNIST.onnx'
        quantized_result_path = os.path.join(temp_model_path, 'coreml_MNIST-csm.onnx')
        if not os.path.isdir(temp_model_path):
            os.makedirs(temp_model_path)
        model = onnx.load_model(resnet_model_path)
        quantized_model = winmltools.utils.quantize(model, per_channel=True, nbits=8, use_dequantize_linear=False)
        onnx.save(quantized_model, quantized_result_path)
        # verify that model is smaller than before
        self._verify_smaller(resnet_model_path, quantized_result_path)
        # verify that you can run the quantized model
        self.assertEqual(run_model(quantized_result_path), 0)

    def test_gemm(self):
        # create a model with simple inputs and outputs for matmul
        M = 200
        K = 20
        N = 100
        data_type = onnx_proto.TensorProto.FLOAT
        # inputs and outputs
        A = onnx.helper.make_tensor_value_info('A', data_type, [M, K])
        B = onnx.helper.make_tensor_value_info('B', data_type, [K, N])
        C = onnx.helper.make_tensor_value_info('C', data_type, [M, N])
        Y = onnx.helper.make_tensor_value_info('Y', data_type, [M, N])
        # nodes
        gemm = onnx.helper.make_node('Gemm', ['A', 'B', 'C'], ['Y'])
        # initializer
        init = onnx.helper.make_tensor('B', data_type, [K, N], [float(i) for i in range(K * N)])
        # call quantize
        graph = onnx.helper.make_graph([gemm], 'test_graph', [A, B, C], [Y], initializer=[init])
        model = onnx.helper.make_model(graph)
        self._verify_quantize_model(model, 'Gemm')

    def test_matmul(self):
        # create a model with simple inputs and outputs for matmul
        dims = [20,20]
        data_type = onnx_proto.TensorProto.FLOAT
        # inputs and outputs
        A = onnx.helper.make_tensor_value_info('A', data_type, dims)
        B = onnx.helper.make_tensor_value_info('B', data_type, dims)
        Y = onnx.helper.make_tensor_value_info('Y', data_type, dims)
        # nodes
        matmul = onnx.helper.make_node('MatMul', ['A', 'B'], ['Y'])
        # initializer
        init = onnx.helper.make_tensor('B', data_type, dims, [float(i) for i in range(400)])
        # call quantize
        graph = onnx.helper.make_graph([matmul], 'test_graph', [A, B], [Y], initializer=[init])
        model = onnx.helper.make_model(graph)
        self._verify_quantize_model(model, 'MatMul')

    def _verify_rnn_like_ops(self, op_name, hidden_size_factor):
        data_type = onnx_proto.TensorProto.FLOAT
        seq_length = 50
        input_size = 100
        hidden_size = 10
        num_directions = 1
        W_dims = [num_directions, hidden_size_factor * hidden_size, input_size]
        R_dims = [num_directions, hidden_size_factor * hidden_size, hidden_size]
        # create a model with simple LSTM model
        node = onnx.helper.make_node(
            op_name,
            inputs=['X', 'W', 'R'],
            outputs=['Y'],
            hidden_size=hidden_size
        )

        # inputs and outputs
        X = onnx.helper.make_tensor_value_info('X', data_type, [seq_length, 1, input_size])
        W = onnx.helper.make_tensor_value_info('W', data_type, W_dims)
        R = onnx.helper.make_tensor_value_info('R', data_type, R_dims)
        Y = onnx.helper.make_tensor_value_info('Y', data_type, [seq_length, num_directions, 1, hidden_size])

        # initializer for W
        W_init = onnx.helper.make_tensor('W', data_type, W_dims,
            [random.random() for _ in range(num_directions * hidden_size_factor * hidden_size * input_size)])
        R_init = onnx.helper.make_tensor('R', data_type, R_dims,
            [random.random() for _ in range(num_directions * hidden_size_factor * hidden_size * hidden_size)])

        model = onnx.helper.make_model(onnx.helper.make_graph(
            [node], 'test_graph', [X,W,R], [Y], initializer=[W_init, R_init]))

        self._verify_quantize_model(model, op_name)

    def test_lstm(self):
        self._verify_rnn_like_ops('LSTM', 4)

    def test_rnn(self):
        self._verify_rnn_like_ops('RNN', 1)

    def test_gru(self):
        self._verify_rnn_like_ops('GRU', 3)

    def test_sanity(self):
        # Make sure input model does not change
        resnet_model_path = share + '\\coreml_MNIST.onnx'
        input_model = onnx.load_model(resnet_model_path) 
        input_model_cp = onnx_proto.ModelProto() 
        input_model_cp.CopyFrom(input_model)
        output_model = winmltools.utils.quantize(input_model)
        self.assertTrue(input_model == input_model_cp)
        # Verify quantize call twice with same parameter does not do anything
        output_model1 = winmltools.utils.quantize(output_model) 
        self.assertTrue(output_model == output_model1)


if __name__ == '__main__':
    unittest.main()
