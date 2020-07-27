# Copyright 2019 The FastEstimator Authors. All Rights Reserved.
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
from typing import Any, Dict, Iterable, List, TypeVar, Union

from fastestimator.op.tensorop.tensorop import TensorOp


class LossOp(TensorOp):
    """Abstract base LossOp class.

    A base class for loss operations. It can be used directly to perform value pass-through (see the adversarial
    training showcase for an example of when this is useful).
    """
    def __init__(self,
                 inputs: Union[str, List[str]] = None,
                 outputs: List[str] = None,
                 mode: Union[None, str, Iterable[str]] = None,
                 average_loss: bool = True):
        assert len(inputs) > 1, "We need at least two inputs to calculate loss"
        assert len(outputs) > 0, "We need at least one output to store the loss"

        super().__init__(inputs=inputs, outputs=outputs, mode=mode)
        self.average_loss = average_loss

    @property
    def true_key(self) -> str:
        return self.inputs[self.true_key_idx]

    @property
    def pred_key(self) -> str:
        return self.inputs[self.pred_key_idx]

    @property
    def true_key_idx(self) -> int:
        return 1

    @property
    def pred_key_idx(self) -> int:
        return 0
