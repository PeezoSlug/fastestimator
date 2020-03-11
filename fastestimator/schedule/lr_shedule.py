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
import math


def cosine_decay(epoch_or_step: int, cycle_length: int, init_lr: float, min_lr: float = 1e-6, start: int = 0):
    """ learning rate cosine decay function (using half of cosine curve)

    Args:
        epoch_or_step: current step or epoch during training.
        cycle_length: the decay cycle length.
        init_lr: initial learning rate to decay from.
        min_lr: minimum learning rate.
        start_step: the step or epoch to start the decay schedule.
    Return:
        lr: learning rate given current step or epoch.
    """
    if epoch_or_step < start:
        lr = init_lr
    else:
        step_in_cycle = (epoch_or_step - start) % cycle_length / cycle_length
        lr = (init_lr - min_lr) / 2 * math.cos(step_in_cycle * math.pi) + (init_lr + min_lr) / 2
    return lr
