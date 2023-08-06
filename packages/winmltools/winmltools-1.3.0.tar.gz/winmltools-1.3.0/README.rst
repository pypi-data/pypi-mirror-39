WinMLTools provide following tools for Windows ML:

Model Conversion
################

WinMLTools enables you to convert models from different machine 
learning toolkits into `ONNX <https://onnx.ai>`_ for use with Windows ML. 
Currently the following toolkits are supported:

* apple CoreML
* keras
* scikit-learn
* lightgbm
* xgboost
* libSVM
* tensorflow (experimental)

Here is a simple example to convert a Core ML model:

::

    from coremltools.models.utils import load_spec
    from winmltools import convert_coreml
    model_coreml = load_spec('example.mlmodel')
    model_onnx = convert_coreml(model_coreml, 7, name='ExampleModel')

Quantization
############

WinMLTools provides quantization tool to reduce the memory footprint of the model.

Here is an example to convert an ONNX model to a quantized ONNX model:

::

    import winmltools

    model = winmltools.load_model('model.onnx')
    quantized_model = winmltools.quantize(model, per_channel=True, nbits=8, use_dequantize_linear=True)
    winmltools.save_model(quantized_model, 'quantized.onnx')


Dependencies
============

In order to convert from different toolkits, you may have to install the following packages for different converters: 

+--------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| Toolkit      | Source                                                                                                                                             |
+==============+====================================================================================================================================================+
| keras        | https://pypi.org/project/Keras                                                                                                                     |
+--------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| tensorflow   | https://pypi.org/project/tensorflow                                                                                                                |
+--------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| scikit-learn | https://pypi.org/project/scikit-learn                                                                                                              |
+--------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| lightgbm     | https://pypi.org/project/lightgbm                                                                                                                  |
+--------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| xgboost      | https://pypi.org/project/xgboost                                                                                                                   |
+--------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| libsvm       | You can download libsvm wheel from various web sources. One example can be found here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#libsvm          |
+--------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| coremltools  | Currenlty coreml does not distribute coreml packaging on windows. You can install from source: pip install git+https://github.com/apple/coremltools|
+--------------+----------------------------------------------------------------------------------------------------------------------------------------------------+


For more information on WinMLTools, you can go to `Convert ML models to ONNX with WinMLTools
<https://docs.microsoft.com/en-us/windows/ai/convert-model-winmltools>`_

License
=======

MIT License
