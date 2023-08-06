# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
import onnx
import onnx.numpy_helper
import struct

import numpy as np
from onnx import onnx_pb as onnx_proto

type_to_name = {
    1: "FLOAT",
    2: "UINT8",
    3: "INT8",
    4: "UINT16",
    5: "INT16",
    6: "INT32",
    7: "INT64",
    8: "STRING",
    9: "BOOL",
    10: "FLOAT16",
    11: "DOUBLE",
    12: "UINT32",
    13: "UINT64",
    14: "COMPLEX64",
    15: "COMPLEX128",
}

# Quantization mode
# DQ_Linear: Packing initialized inputs with DequantizeLinear operator. They are supported in com.microsoft namespace version 1.
# CAST_SUB_MUL: Packing initialized inputs with 'Cast', 'Sub', and 'Mul' operators. 
#               Since this requires general broadcasting, they are supported in opset >= 7.
class QuantizationMode():
    DequantizeLinear = 0
    CAST_SUB_MUL = 1

quantization_modes = [getattr(QuantizationMode, attr) for attr in dir(QuantizationMode) if not callable(getattr(QuantizationMode, attr)) and not attr.startswith("__")]

# OperatorSet version for custom operator for quantization
ms_domain = 'com.microsoft'
ms_version = 1

class Weight:
    '''
        Represents a linearly quantized weight input from ONNX operators
    '''
    def __init__(self, name, initializer, rmins, rmaxs, zero_points, scales, data=[], quantized_data=[], axis=1):
        self.name = name
        self.initializer = initializer  # TensorProto initializer in ONNX graph
        self.rmins = rmins  # List of minimum range for each axis
        self.rmaxs = rmaxs  # List of maximum range for each axis
        self.zero_points = zero_points  # 1D tensor of zero points computed for each axis. scalar if axis is empty
        self.scales = scales  # 1D tensor of scales computed for each axis. scalar if axis is empty
        self.data = data  # original data from initializer TensorProto
        self.quantized_data = quantized_data  # weight-packed data from data
        self.axis = axis  # Scalar to specify which dimension in the initializer to weight pack.
                          # If empty, single zero point and scales computed from a single rmin and rmax


def quantize_data(data, quantize_range, mode='linear'):
    '''
        :parameter quantize_range: list of data to weight pack.
        :parameter mode: mode to quantize data. Currently only supporting linear
        :return: minimum, maximum, zero point, scale, and quantized weights

        To pack weights, we compute a linear transformation from [rmin, rmax] -> [0, 2^{b-1}],
        and add necessary intermediate nodes to trasnform quantized weight to full weight using the equation
        r = S(q-z), where
            r: real original value
            q: quantized value
            S: scale
            z: zero point
    '''
    rmin = min(data)
    rmax = max(data)

    scale = (float(rmax) - rmin) / quantize_range if rmin != rmax else 1
    zero_point = round((0 - rmin) / scale) # round to nearest integer
    quantized_data = (np.asarray(data) / scale + zero_point).astype('B') # unsigned byte type
    return rmin, rmax, zero_point, scale, quantized_data


# Currently ONNX 1.3 make_node on helper.py does not assign domain correctly.
# TODO: remove this when newer onnx pypi package with commit
# https://github.com/onnx/onnx/commit/f86e951d6957517af59a0b845f0e449794a371b2 is available.
def make_node_domain(
        op_type,  # type: Text
        inputs,  # type: Sequence[Text]
        outputs,  # type: Sequence[Text]
        name=None,  # type: Optional[Text]
        doc_string=None,  # type: Optional[Text]
        domain=None,  # type: Optional[Text]
        **kwargs  # type: Any
):  # type: (...) -> NodeProto
    """Construct a NodeProto.

    Arguments:
        op_type (string): The name of the operator to construct
        inputs (list of string): list of input names
        outputs (list of string): list of output names
        name (string, default None): optional unique identifier for NodeProto
        doc_string (string, default None): optional documentation string for NodeProto
        domain (string, default None): optional domain for NodeProto.
            If it's None, we will just use default domain (which is empty)
        **kwargs (dict): the attributes of the node.  The acceptable values
            are documented in :func:`make_attribute`.
    """

    node = onnx.NodeProto()
    node.op_type = op_type
    node.input.extend(inputs)
    node.output.extend(outputs)
    if name:
        node.name = name
    if doc_string:
        node.doc_string = doc_string
    if domain is not None:
        node.domain = domain
    if kwargs:
        node.attribute.extend(
            onnx.helper.make_attribute(key, value)
            for key, value in sorted(kwargs.items()))
    return node

onnx.helper.make_node = make_node_domain


class ONNXQuantizer:
    def __init__(self, model, per_channel, dqtype, mode):
        self.model = model
        self.per_channel = per_channel # weight-pack per channel
        self.dqtype = dqtype  # dequantize data type
        self.mode = mode # QuantizationMode.Value
        if not self.mode in quantization_modes:
            raise ValueError('unsupported quantization mode {}'.format(self.mode))
        if self.dqtype == onnx_proto.TensorProto.UINT8:
            self.qrange = 255  # 2^b - 1
        else:
            raise ValueError('unsupported quantization data type')

        # Quantization is supported for opset 7 and higher. This is because operators support boradcasting starting in opset 7
        opset_info = next((opset for opset in self.model.opset_import if opset.domain == '' or opset.domain == 'ai.onnx'), None)
        if opset_info is None or opset_info.version < 7:
            raise ValueError('the model does not have the required ai.onnx operator set (7 or higher) for quantization support.')

    def quantize_model(self):
        # Create a new topologically sorted list for quantizing a model
        new_list = []
        for node in self.model.graph.node:
            if node.op_type == 'Conv':
                new_list += self._quantize_convolution(node)
            elif node.op_type == 'MatMul':
                new_list += self._quantize_matmul(node)
            elif node.op_type == 'Gemm':
                new_list += self._quantize_gemm(node)
            elif node.op_type == 'LSTM':
                new_list += self._quantize_lstm(node)
            elif node.op_type == 'RNN':
                new_list += self._quantize_rnn(node)
            elif node.op_type == 'GRU':
                new_list += self._quantize_gru(node)
            else:
                new_list.append(node)

        # extend is used to append to the list for a protobuf fields
        # https://developers.google.com/protocol-buffers/docs/reference/python-generated?csw=1#fields
        self.model.graph.ClearField('node')
        self.model.graph.node.extend(new_list)
        # update custom 'ms' opset for dequant mode
        if self.mode == QuantizationMode.DequantizeLinear:
            ms_opset = next(
                (opset for opset in self.model.opset_import if opset.domain == ms_domain and opset.version >= ms_version), None)
            if ms_opset is None:
                self.model.opset_import.extend([onnx.helper.make_opsetid(ms_domain, ms_version)])
        return self.model

    def find_weight_data(self, initializer):
        '''
            :param initializer: TensorProto initializer object from a graph
            :return: a list of initialized data in a given initializer object
        '''
        if initializer.data_type == onnx_proto.TensorProto.FLOAT:
            weights = onnx.numpy_helper.to_array(initializer)
        else:
            raise ValueError('Model contains conv operator weights in {}. Only float type quantization is supported.'.format(
                type_to_name[initializer.data_type]))
        return weights

    def _update_graph(self, weight):
        '''
            Given a weight object, update the graph by doing the following:
             - remove old initializer, update new initializers for quantized weight, zero point, and scale
             - remove old weight input, update with new inputs for quantized weight, zero point, and scale
            This function does NOT update the nodes in the graph, just initializers and inputs
        '''
        packed_weight_name = weight.name + '_quantized'
        scale_name = weight.name + '_scale'
        zero_point_name = weight.name + '_zero_point'

        # Remove existing weight initializer
        self.model.graph.initializer.remove(weight.initializer)
        # Update packed weight, zero point, and scale initializers
        packed_weight_initializer = onnx.helper.make_tensor(packed_weight_name, self.dqtype,
                                                  weight.initializer.dims, weight.quantized_data)
        if self.mode == QuantizationMode.CAST_SUB_MUL:
            zero_scale_shape = [1 for _ in weight.initializer.dims]
            zero_scale_shape[weight.axis] = weight.initializer.dims[weight.axis]
        elif self.mode == QuantizationMode.DequantizeLinear:
            zero_scale_shape = [weight.initializer.dims[weight.axis]] if self.per_channel else None # Empty dimension implies scalar
        zero_point_type = onnx_proto.TensorProto.UINT8 if self.mode == QuantizationMode.DequantizeLinear else onnx_proto.TensorProto.FLOAT
        scale_initializer = onnx.helper.make_tensor(scale_name, onnx_proto.TensorProto.FLOAT, zero_scale_shape, weight.scales)
        zero_initializer = onnx.helper.make_tensor(zero_point_name, zero_point_type, zero_scale_shape, weight.zero_points)

        self.model.graph.initializer.extend([packed_weight_initializer, scale_initializer, zero_initializer])

        # Removing input weight to a convolution
        try:
            weight_input = next(val for val in self.model.graph.input if val.name == weight.name)
        except StopIteration:
            raise ValueError('invalid weight name {} found in the graph '.format(weight.name))
        self.model.graph.input.remove(weight_input)

        # Create input for initialized scale and zeros
        packed_weight_value_info = onnx.helper.make_tensor_value_info(packed_weight_name, self.dqtype, weight.initializer.dims)
        scale_value_info = onnx.helper.make_tensor_value_info(scale_name, onnx_proto.TensorProto.FLOAT, zero_scale_shape)
        zero_point_value_info = onnx.helper.make_tensor_value_info(zero_point_name,
            zero_point_type, zero_scale_shape) # zero_point is int for dequantize operator

        self.model.graph.input.extend([packed_weight_value_info, scale_value_info, zero_point_value_info])

    def _get_weight_packing_nodes(self, weight, node, weight_index):
        '''
            Given a weight object, prepend the dequantization nodes to the list of nodes.
            If mode is 'weight_pack' mode, this function will add Cast, Sub, and Mul operators to
            simulate r = S(q-z) equation.
            For 'weight_pack_dequantize' mode, this function will add a DequantizeLinear operator
            to the graph

            :param weight: weight object for weight-packing
            :param node: node containing the input to be weight packed
            :param weight_index: index of node input to be weight packed
            :return: topologically sorted list of nodes to represent weight-packed input node
        '''
        assert(self.mode in quantization_modes)
        new_weight_name = weight.name + '_quantized'
        scale_name = weight.name + '_scale'
        zero_point_name = weight.name + '_zero_point'
        output_name = weight.name + '_dequantized'
        node_list = []
        if self.mode == QuantizationMode.CAST_SUB_MUL:
            # Create Cast -> Sub -> Mul operators. This version is supported for >= RS5
            cast_output_name = weight.name + '_cast_output'
            cast_node = onnx.helper.make_node('Cast', [new_weight_name], [cast_output_name],
                                            weight.name + '_cast', to=onnx_proto.TensorProto.FLOAT)
            node_list.append(cast_node)
            sub_output_name = weight.name + '_sub_output'
            node_list.append(
                onnx.helper.make_node('Sub', [cast_output_name, zero_point_name], [sub_output_name], weight.name + '_sub'))
            node_list.append(
                onnx.helper.make_node('Mul', [sub_output_name, scale_name], [output_name], weight.name + '_mul'))
        elif self.mode == QuantizationMode.DequantizeLinear:
            # Create DequantizeLinear operator. This version is supported for >= 19H1
            if self.per_channel:
                node_list.append(onnx.helper.make_node('DequantizeLinear', [new_weight_name, scale_name, zero_point_name],
                    [output_name], weight.name + '_DequantizeLinear', domain=ms_domain, axis=weight.axis))
            else:
                node_list.append(onnx.helper.make_node('DequantizeLinear', [new_weight_name, scale_name, zero_point_name],
                    [output_name], weight.name + '_DequantizeLinear', domain=ms_domain))

        # updating input of the node to be the output of dequantize operator(s)
        node.input[weight_index] = output_name
        return node_list

    def _get_quantized_weight(self, initializer):
        '''
            :param initializer: TensorProto initializer
            :return: Weight class with quantization information
        '''
        weights_data = self.find_weight_data(initializer)
        rmin, rmax, zero_point, scale, quantized_weights_data = quantize_data(weights_data.flatten().tolist(), self.qrange)
        weight = Weight(initializer.name, initializer, [rmin], [rmax], [zero_point], [scale], weights_data, quantized_weights_data)
        return weight

    def _get_quantized_weight_convolution(self, initializer):
        '''
            :param initializer: initializer TypeProto to quantize
            :return: Weight class object with quantization information for a given initializer
        '''
        if not self.per_channel:
            return self._get_quantized_weight(initializer)

        weights = self.find_weight_data(initializer)
        # Assuming nchw, compute per-channel quantization
        # https://arxiv.org/pdf/1806.08342.pdf
        channel_count = initializer.dims[1]
        np_data = np.reshape(weights, initializer.dims)
        rmin_list = []
        rmax_list = []
        zero_point_list = []
        scale_list = []
        quantized_per_channel_data_list = []
        for i in range(channel_count):
            # for each channel, compute quantization data
            per_channel_data = np_data[:,i,:,:].flatten()
            rmin, rmax, zero_point, scale, quantized_per_channel_data = quantize_data(per_channel_data.flatten().tolist(), self.qrange)
            rmin_list.append(rmin)
            rmax_list.append(rmax)
            zero_point_list.append(zero_point)
            scale_list.append(scale)
            quantized_per_channel_data_list.append(quantized_per_channel_data)
        channel_index = 1 # nchw
        # combine per_channel_data into one
        reshape_dims = list(initializer.dims)  # deep copy
        reshape_dims[channel_index] = 1  # only one per channel for reshape
        quantized_weights = np.asarray(quantized_per_channel_data_list[0]).reshape(reshape_dims)
        for i in range(1, len(quantized_per_channel_data_list)):
            channel_weights = np.asarray(quantized_per_channel_data_list[i]).reshape(reshape_dims)
            quantized_weights = np.concatenate((quantized_weights, channel_weights), axis=1)

        weight = Weight(initializer.name, initializer, rmin_list, rmax_list,
                        zero_point_list, scale_list, weights, quantized_weights.flatten().tolist(), channel_index)
        return weight

    def _quantize_with_inputs(self, node, indices):
        '''
            Given a node and indices of inputs, return a quantized node.
        '''
        nodes_list = []
        for i in indices: # weight packing w,r weights
            node_input = node.input[i]
            # weight pack w as a whole for now.
            try:
                initializer = next(iter([init for init in self.model.graph.initializer if init.name == node_input]))
                # print('quantizing input {} for node {}'.format(initializer.name, node.name))
            except:
                # no initializer for convolution weight input, just return the node as it is
                continue
            weight = self._get_quantized_weight(initializer)
            self._update_graph(weight)
            nodes_list += self._get_weight_packing_nodes(weight, node, i)
        return nodes_list + [node]

    def _quantize_convolution(self, node):
        '''
            https://github.com/onnx/onnx/blob/master/docs/Operators.md#Conv
            :param node: Conv node
            :return: a list of nodes in topological order that represents quantized Conv node
        '''
        assert (node.op_type == "Conv")
        # Try to update weight input initializers
        weight_index = 1  # weight input is at index 1 for convolution op
        try:
            initializer = next(iter([init for init in self.model.graph.initializer if init.name == node.input[weight_index]]))
        except:
            # no initializer for convolution weight input, just return the node as it is
            return [node]
        weight = self._get_quantized_weight_convolution(initializer)
        self._update_graph(weight)
        return self._get_weight_packing_nodes(weight, node, weight_index) + [node]

    def _quantize_matmul(self, node):
        '''
            https://github.com/onnx/onnx/blob/master/docs/Operators.md#MatMul
            :param node: MatMul node
            :return: a list of nodes in topological order that represents quantized MatMul node
        '''
        assert(node.op_type == 'MatMul')
        return self._quantize_with_inputs(node, [0,1])

    def _quantize_gemm(self, node):
        '''
            https://github.com/onnx/onnx/blob/master/docs/Operators.md#Gemm
            :param node: Gemm node
            :return: a list of nodes in topological order that represents quantized Gemm node
        '''
        assert(node.op_type == 'Gemm')
        return self._quantize_with_inputs(node, [0,1])

    def _quantize_lstm(self, node):
        '''
            https://github.com/onnx/onnx/blob/master/docs/Operators.md#LSTM
            :param node: LSTM node
            :return: a list of nodes in a topological order that represents a quantized LSTM node
        '''
        assert(node.op_type == 'LSTM')
        input_indices = [1,2] # quantizing w and r inputs
        return self._quantize_with_inputs(node, input_indices)

    def _quantize_rnn(self, node):
        '''
            https://github.com/onnx/onnx/blob/master/docs/Operators.md#RNN
            :return: a list of nodes in a topological order that represents a quantized RNN node
        '''
        assert(node.op_type == 'RNN')
        input_indices = [1,2] # quantizing w and r
        return self._quantize_with_inputs(node, input_indices)

    def _quantize_gru(self, node):
        '''
            https://github.com/onnx/onnx/blob/master/docs/Operators.md#GRU
            :return: a list of nodes in a topological order that represents a quantized GRU node
        '''
        assert(node.op_type == 'GRU')
        input_indices = [1,2] # quantizing w and r
        return self._quantize_with_inputs(node, input_indices)


def quantize(model_path, output_path, per_channel=True, nbits=8, use_dequantize_linear=True):
    '''
        Given an onnx model, create a quantized onnx model and save it into a file

    :param model_path: input onnx model path
    :param output_path: output onnx model path
    :param nbits: number of bits to represent quantized data. Currently only supporting 8-bit types
    :param per_channel: quantize weights per channel
    :param use_dequantize_linear: If True, the function will use DequantizeLinear operator for weight packing.
        If False, the function will use Cast, Sub, and Mul operator of opset 7 for dequantizing a graph.
    '''
    if nbits == 8:
        qType = onnx_proto.TensorProto.UINT8
        mode = QuantizationMode.DequantizeLinear if use_dequantize_linear else QuantizationMode.CAST_SUB_MUL
        quantizer = ONNXQuantizer(onnx.load_model(model_path), per_channel, qType, mode)
        quantizer.quantize_model()
        with open(output_path, 'wb') as outfile:
            outfile.write(quantizer.model.SerializeToString())
    else:
        raise ValueError('Unknown value for nbits. only 8 bit quantization is currently supported')