#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

def tf2onnx_installed():
    """
    Checks that *tf2onnx* is available.
    """
    try:
        import tf2onnx
        return True
    except ImportError:
        return False


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
