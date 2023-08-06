import winmltools
import tensorflow
import tf2onnx
import unittest

from tensorflow.core.framework import graph_pb2
from tensorflow.python.tools import freeze_graph
import tensorflow as tf
import os
import onnx

from .._utils import temp_model_path

models_dir = os.path.dirname(os.path.abspath(__file__)) + '/../models'


def convert_tensorflow_file(filename, output_names, test_name="", debug=True, opset=8):
    graph_def = graph_pb2.GraphDef()
    with open(filename, 'rb') as file:
        graph_def.ParseFromString(file.read())
    g = tf.import_graph_def(graph_def, name='')
    with tf.Session(graph=g) as sess:
        converted_model = winmltools.convert_tensorflow(sess.graph, opset, continue_on_error=True, verbose=True, output_names=output_names)
        onnx.checker.check_model(converted_model)
    if debug:
        with open(os.path.join(temp_model_path, test_name + '-' + os.path.basename(filename) +'.onnx'), 'wb') as file:
            file.write(converted_model.SerializeToString())
    tf.reset_default_graph()

class TestTensorFlowConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isdir(temp_model_path):
            os.makedirs(temp_model_path)

    def test_conv(self):
        convert_tensorflow_file(models_dir + '/tensorflow/conv-layers/frozen.pb', ['output:0'], test_name='conv')

    def test_fc(self):
        convert_tensorflow_file(models_dir + '/tensorflow/fc-layers/frozen.pb', ['output:0'], test_name='fc')

    def test_ae0(self):
        convert_tensorflow_file(models_dir + '/tensorflow/ae0/frozen.pb', ['output:0'], test_name='ae0')

    def test_add(self):
        x = tf.placeholder(tf.float32, shape=[1], name='x')
        y = tf.placeholder(tf.float32, shape=[1], name='y')
        add = tf.add(x, y, 'addition')
        graph_path = temp_model_path + '/tf-add.pb'
        with tf.Session() as sess:
            sess.run(add, feed_dict={x:[1], y:[2]})
            graph_def = sess.graph.as_graph_def()
        with open(graph_path, 'wb') as file:
            file.write(graph_def.SerializeToString())
        convert_tensorflow_file(graph_path, ['addition:0'])

if __name__ == "__main__":
    unittest.main()