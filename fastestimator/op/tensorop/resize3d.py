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
from typing import Any, Dict, Iterable, List, Sequence, TypeVar, Union

import tensorflow as tf
import torch

from fastestimator.backend._resize3d import resize_3d
from fastestimator.op.tensorop.tensorop import TensorOp
from fastestimator.util.traceability_util import traceable
from fastestimator.util.base_util import to_list

Tensor = TypeVar('Tensor', tf.Tensor, torch.Tensor)


@traceable()
class Resize3D(TensorOp):
    """Resize a 3D tensor.

        Args:
            inputs: Key of the input tensor.
            outputs: Key of the output tensor.
            output_shape: The desired output shape for the input tensor.
            resize_mode: The resize mode of the operation ('area' or 'nearest').
            mode: What mode(s) to execute this Op in. For example, "train", "eval", "test", or "infer". To execute
                regardless of mode, pass None. To execute in all modes except for a particular one, you can pass an argument
                like "!infer" or "!train".
            ds_id: What dataset id(s) to execute this Op in. To execute regardless of ds_id, pass None. To execute in all
                ds_ids except for a particular one, you can pass an argument like "!ds1".
    """
    def __init__(self,
                 inputs: Union[str, Iterable[str]],
                 outputs: Union[str, Iterable[str]],
                 output_shape: Sequence[int],
                 resize_mode: str = 'nearest',
                 mode: Union[None, str, Iterable[str]] = None,
                 ds_id: Union[None, str, Iterable[str]] = None):

        super().__init__(inputs=to_list(inputs), outputs=to_list(outputs), mode=mode)
        assert resize_mode in ['nearest', 'area'], "Only following resize modes are supported: 'nearest', 'area' "
        self.output_shape = output_shape
        self.reize_mode = resize_mode

    def forward(self, data: List[Tensor], state: Dict[str, Any]) -> Union[Tensor, List[Tensor]]:
        return [resize_3d(elem, self.output_shape, self.resize_mode) for elem in data]
