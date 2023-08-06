#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

"""
WinMLTools is a python package that supports the following:

    - Converts ML models into ONNX for use with Windows Machine Learning.
    - Quantize ONNX models

    For more information, go to https://docs.microsoft.com/en-us/windows/ai/convert-model-winmltools
"""

__version__ = "1.3.0"
__author__ = "Microsoft Corporation"
__producer__ = "WinMLTools"

from .convert import convert_coreml
from .convert import convert_keras
from .convert import convert_sklearn
from .convert import convert_libsvm
from .convert import convert_lightgbm
from .convert import convert_xgboost
from .convert import convert_tensorflow

from .utils import load_model
from .utils import save_model
from .utils import save_text

from .utils import quantize