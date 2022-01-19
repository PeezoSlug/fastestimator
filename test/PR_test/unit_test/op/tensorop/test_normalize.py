# Copyright 2022 The FastEstimator Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import unittest

import tensorflow as tf
import torch
from numpy import arange, array, float32, testing

from fastestimator.backend import to_tensor
from fastestimator.op.tensorop.normalize import Normalize


class TestNormalize(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.numpy_array = arange(0.0, 27.0, 1.0, dtype=float32).reshape((1, 3, 3, 3))
        self.expected_result = array(
            [[[[-1.6688062, -1.5404365, -1.4120668], [-1.283697, -1.1553273, -1.0269576], [
                -0.89858794, -0.77021825, -0.6418485
            ]], [[-0.5134788, -0.38510913, -0.2567394], [-0.1283697, 0., 0.1283697], [0.2567394, 0.38510913, 0.5134788]
                 ], [[0.6418485, 0.77021825, 0.89858794], [1.0269576, 1.1553273, 1.283697],
                     [1.4120668, 1.5404365, 1.6688062]]]],
            dtype=float32)
        self.expected_result_multi = array(
            [[[[-1.5331011, -1.543425, -1.5537487], [-1.1459544, -1.1562783, -1.166602],
               [-0.7588076, -0.7691315, -0.7794553]],
              [[-0.37166086, -0.38198477, -0.39230856], [0.01548585, 0.00516195, -0.00516183], [
                  0.4026326, 0.39230868, 0.3819849
              ]], [[0.7897793, 0.7794554, 0.7691316], [1.176926, 1.1666021, 1.1562784],
                   [1.5640727, 1.5537488, 1.5434251]]]],
            dtype=float32)

    def test_normalize_tf(self):
        op = Normalize(inputs="image", outputs="image", mean=0.482, std=0.289, max_pixel_value=27)
        op.build("tf")
        data = op.forward(data=tf.convert_to_tensor(self.numpy_array), state={})
        testing.assert_array_almost_equal(data.numpy(), self.expected_result, 2)

    def test_normalize_tf_multi(self):
        op = Normalize(inputs="image",
                       outputs="image",
                       mean=(0.44, 0.48, 0.52),
                       std=(0.287, 0.287, 0.287),
                       max_pixel_value=27)
        op.build("tf")
        data = op.forward(data=tf.convert_to_tensor(self.numpy_array), state={})
        testing.assert_array_almost_equal(data.numpy(), self.expected_result_multi, 2)

    def test_normalize_torch(self):
        op = Normalize(inputs="image", outputs="image", mean=0.482, std=0.289, max_pixel_value=27.0)
        op.build("torch", "cuda:0" if torch.cuda.is_available() else "cpu")
        data = op.forward(data=to_tensor(self.numpy_array, "torch"), state={})
        testing.assert_array_almost_equal(data.numpy(), self.expected_result, 2)

    def test_normalize_torch_multi(self):
        op = Normalize(inputs="image",
                       outputs="image",
                       mean=(0.44, 0.48, 0.52),
                       std=(0.287, 0.287, 0.287),
                       max_pixel_value=27)
        op.build("torch", "cuda:0" if torch.cuda.is_available() else "cpu")
        data = op.forward(data=to_tensor(self.numpy_array, "torch"), state={})
        testing.assert_array_almost_equal(data.numpy(), self.expected_result_multi, 2)

    def test_normalize_numpy(self):
        op = Normalize(inputs="image", outputs="image", mean=0.482, std=0.289, max_pixel_value=27.0)
        data = op.forward(data=self.numpy_array, state={})
        testing.assert_array_almost_equal(data, self.expected_result, 2)

    def test_normalize_numpy_multi(self):
        op = Normalize(inputs="image",
                       outputs="image",
                       mean=(0.44, 0.48, 0.52),
                       std=(0.287, 0.287, 0.287),
                       max_pixel_value=27)
        data = op.forward(data=self.numpy_array, state={})
        testing.assert_array_almost_equal(data, self.expected_result_multi, 2)