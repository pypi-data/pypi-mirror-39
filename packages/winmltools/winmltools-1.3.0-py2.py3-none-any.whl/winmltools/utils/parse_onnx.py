#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------
import os
import argparse
import onnx
import struct

import numpy as np

parser = argparse.ArgumentParser()
options = parser.add_mutually_exclusive_group()

options.add_argument("--print", help="print a model")
options.add_argument("--quantize", help="quantize a model")


def print_onnx(model):
    '''
    modelProto = pb.ModelProto()
    with open(model_path, 'rb') as f:
        data = f.read()
    modelProto.ParseFromString(data)
    '''
    print(model.model_version)
    print(model.domain)
    print(model.opset_import)
    print_nodes(model)
    print_inputs(model)
    print_outputs(model)
    print_initializers(model)
    print_bad_data(model)


def print_nodes(model):
    for node in model.graph.node:
        print("---node begin---")
        print(repr(node))
        print("---node end-----")


def print_inputs(model):
    for inp in model.graph.input:
        print("---input begin---")
        print(inp)
        print("---input end---")


def print_outputs(model):
    for outp in model.graph.output:
        print("---output begin---")
        print(outp)
        print("---output end---")

def print_initializers(model):
    for initializer in model.graph.initializer:
        if initializer.name.endswith('quantized'):
            print("---initializer begin---")
            print(initializer.int32_data)
            print("---initializer end---")

def print_bad_data(model):
    for initializer in model.graph.initializer:
        print("---initializer begin---")
        print('name {}'.format(initializer.name))
        print(initializer.float_data)
        print("---initializer end---")

# DataType enum defined in onnx-ml
floatType = 1
uint8Type = 2
int8Type = 3
uint16Type = 4

class Weight:
    '''
        Represents a single weight input from ONNX operators
    '''
    def __init__(self, name, initializer, rmin, rmax, scale, zero_point, data=[], quantized_data=[]):
        self.name = name
        self.initializer = initializer  # TensorProto initializer in ONNX graph
        self.rmin = rmin
        self.rmax = rmax
        self.scale = scale
        self.zero_point = zero_point
        self.data = data
        self.quantized_data = quantized_data

class ONNXQuantizer:
    def __init__(self, model, dqtype=uint8Type):
        self.model = model
        self.dqtype = dqtype  # dequantize data type
        self.weights = {}  # dictionary of TensorProto initializer name to weights in the graph

    def process_initializer(self, initializer):
        '''
            compute scale and ranges from all values in initializer weights
            input: TensorProto initializer
            dqtype: dequantize type
                0: 8 bit unsigned integer
                1: 16 bit unsigned integer
        '''
        dtype = initializer.data_type
        if dtype != 1:  # float
            raise ValueError("only to float quantization supported for now.")
        if self.dqtype not in [uint8Type]:
            raise ValueError("unsupported dequantization type.")

        qrange = 255 if self.dqtype == uint8Type or self.dqtype == int8Type else 65535  # 2^b - 1
        if len(initializer.float_data) != 0:
            rmin = min(initializer.float_data)
            rmax = max(initializer.float_data)
            weights = initializer.float_data
        elif len(initializer.double_data) != 0:
            rmin = min(initializer.double_data)
            rmax = max(initializer.double_data)
            weights = initializer.double_data
        elif len(initializer.raw_data) != "":
            raw_data = initializer.raw_data
            floats = []
            # Raw data stored as little endian float in IEE 754 format
            # need to unpack for each 4 bytes in raw data
            for i in range(0, len(raw_data), 4):
                floats.append(struct.unpack('<f', raw_data[i:i + 4])[0])
            rmin = min(floats)
            rmax = max(floats)
            weights = floats
        else:
            print(initializer)
            raise ValueError("could not find initializer value for {}".format(initializer.name))
        scale = (rmax - rmin) / qrange
        zero_point = (0 - rmin) / scale  # for uint8 conversion
        qweights = (np.asarray(weights) / scale + zero_point).astype(int)
        weight = Weight(initializer.name, initializer, rmin, rmax, scale, zero_point, weights, qweights)
        self.weights[initializer.name] = weight
        self.update_initializer(weight)
        return weight

    def get_tensor_dim(self, tensorProto):
        dims = []
        for dim in tensorProto.dims:
            dims.append(dim)
        return dims

    def update_initializer(self, weight):
        '''
            using Weight class remove old initializer and update with new quantized initializer in the graph
        '''
        self.model.graph.initializer.remove(weight.initializer)
        new_initializer = onnx.helper.make_tensor(weight.name + '_quantized', self.dqtype,
                                                  self.get_tensor_dim(weight.initializer), weight.quantized_data)
        self.model.graph.initializer.extend([new_initializer])

    def get_shape(self, tensorShapeProto):
        '''
        :param tensorShapeProto:
        :return: a list representing the shape of a tensorShapeProto
        '''
        shape = []
        for dim in tensorShapeProto.dim:
            shape.append(dim.dim_value)
        return shape

    def quantize_convolution(self, node):
        '''
            -given a node, find a weight and its initializer.
            - find rmin and rmax
            - Compute scale
            - compute zero point (-scale * rmin)
            - update initializer with quantized weights q = r / S + Z
            - update(add new and remove old) name of initializer and value info proto (_quantized prefix name)
            - create cast node sub node and mul node, update input and output of each intermediate nodes
            :return: a list of nodes that should be representing convolution in topological order
                (e.g cast -> sub -> mul -> conv)
        '''
        dqType = uint8Type
        node_list = []
        assert (node.op_type == "Conv")
        # Updating Initializer
        weight_name = node.input[1]
        for initializer in self.model.graph.initializer:
            if initializer.name == weight_name:
                self.process_initializer(initializer)

        # Removing input weight to a convolution
        shape = []
        for input in self.model.graph.input:
            if input.name == weight_name:
                shape = self.get_shape(input.type.tensor_type.shape)
                break
        self.model.graph.input.remove(input)

        # Create inputs and initializer for zero and scale
        scale_name = weight_name + '_scale'
        zero_point_name = weight_name + '_zero_point'
        scale_initializer = onnx.helper.make_tensor(scale_name, floatType, [1], [self.weights[weight_name].scale])
        zero_initializer = onnx.helper.make_tensor(zero_point_name, floatType, [1], [self.weights[weight_name].zero_point])
        self.model.graph.initializer.extend([scale_initializer, zero_initializer])

        # Create input for initialized scale and zeros
        for name in [scale_name, zero_point_name]:
            value_info = onnx.helper.make_tensor_value_info(name, floatType, [1])
            self.model.graph.input.extend([value_info])

        # Create operators and connect them. Add nodes in topological order
        cast_output_name = weight_name + '_cast_output'
        cast_node = onnx.helper.make_node('Cast', [weight_name + '_quantized'], [cast_output_name],
                                          weight_name + '_cast', to=floatType)
        node_list.append(cast_node)
        sub_output_name = weight_name + "_sub_output"
        node_list.append(
            onnx.helper.make_node('Sub', [cast_output_name, zero_point_name], [sub_output_name], weight_name + '_sub'))
        mul_output_name = weight_name + "_dequantized"
        node_list.append(
            onnx.helper.make_node('Mul', [sub_output_name, scale_name], [mul_output_name], weight_name + '_mul'))
        # update node and value info (input) and node
        node.input[1] = mul_output_name  # node input name

        # Create inputs for all the intermediate inputs/outputs
        for name in [cast_output_name, sub_output_name, mul_output_name]:
            value_info = onnx.helper.make_tensor_value_info(name, floatType, self.get_shape(input.type.tensor_type.shape))

        # appending convolution at the very end for topological sorting
        node_list.append(node)

        return node_list

    def quantize_model(self):
        # Create a new topologically sorted list for quantizing a model
        new_list = []
        for node in self.model.graph.node:
            if node.op_type == 'Conv':
                new_list += self.quantize_convolution(node)
            else:
                new_list.append(node)
        self.model.graph.ClearField('node')
        self.model.graph.node.extend(new_list)
        return self.model

def quantize(model_path, output_path, nbits):
    if nbits == 8:
        qType = uint8Type
        quantizer = ONNXQuantizer(onnx.load_model(model_path), qType)
        quantizer.quantize_model()
        with open(output_path, 'wb') as f:
            f.write(quantizer.model.SerializeToString())
    else:
        raise ValueError('only 8 bit quantization is currently supported')
'''
if __name__ == "__main__":
    args = parser.parse_args()
    if args.print is not None:
        model = onnx.load_model(args.print)
        print_onnx(model)
    elif args.quantize is not None:
        if os.path.isdir(args.quantize):
            for file in os.listdir(args.quantize):
                if os.path.splitext(file)[-1] == '.onnx':
                    print('quantizing {}'.format(file))
                    quantizer = ONNXQuantizer(onnx.load_model('{}\\{}'.format(args.quantize, file)), uint8Type)
                    quantizer.quantize_model()
                    with open('{}\\{}-quantized.onnx'.format(args.quantize, os.path.splitext(file)[0]), 'wb') as f:
                        f.write(quantizer.model.SerializeToString())
        elif os.path.exists(args.quantize):
            quantizer = ONNXQuantizer(onnx.load_model(args.quantize), uint8Type)
            quantizer.quantize_model()
            with open('{}-quantized.onnx'.format(os.path.splitext(args.quantize)[0]), 'wb') as f:
                f.write(quantizer.model.SerializeToString())
        else:
            raise ValueError('wrong argument for quantizing a model')
'''