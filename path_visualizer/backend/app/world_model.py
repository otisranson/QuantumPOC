# Copyright 2026 Otis Ranson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A small "learned world model": a network trained to predict the path-integral
field directly from (start, end, hbar), without ever running the simulator.

This is the same basic idea behind world models in AI more broadly: train a
fast network to mimic an expensive-to-query environment or simulator, so you
can sample it cheaply afterward. Here the "environment" is compute_field()
from path_integral.py, and the network is deliberately tiny and plain (an
MLP, no convolutions) -- an honestly-scoped toy of the idea, not a claim of
sophisticated learned physics. Expect its output to look visibly blurrier
than the live simulation: a small non-convolutional network regressing a
sparse, speckled Monte Carlo target naturally learns the gross shape, not
the fine texture. That blurriness is itself the point of the "computed vs.
learned" toggle -- it shows what got lost in amortizing the simulator away.
"""

import math
from pathlib import Path

import numpy as np
import torch
from torch import nn

from app.path_integral import GRID_SIZE, HBAR_MAX, HBAR_MIN

CHECKPOINT_PATH = Path(__file__).parent / "world_model.pt"

_LOG_HBAR_MIN = math.log10(HBAR_MIN)
_LOG_HBAR_MAX = math.log10(HBAR_MAX)


def featurize(start: list[float], end: list[float], hbar: float) -> np.ndarray:
    """[sx, sy, ex, ey, log10(hbar) rescaled to ~[-1, 1]] -- hbar's effect is multiplicative/log-scale."""
    log_hbar = math.log10(hbar)
    scaled = 2.0 * (log_hbar - _LOG_HBAR_MIN) / (_LOG_HBAR_MAX - _LOG_HBAR_MIN) - 1.0
    return np.array([start[0], start[1], end[0], end[1], scaled], dtype=np.float32)


class WorldModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(5, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, GRID_SIZE * GRID_SIZE),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).view(-1, GRID_SIZE, GRID_SIZE)


def predict(model: WorldModel, start: list[float], end: list[float], hbar: float) -> np.ndarray:
    """Run inference and renormalize by the output's own max, matching compute_field()'s convention."""
    model.eval()
    features = torch.from_numpy(featurize(start, end, hbar)).unsqueeze(0)
    with torch.no_grad():
        field = model(features).squeeze(0).numpy()
    peak = field.max()
    if peak > 0:
        field = field / peak
    return field


def load_model() -> WorldModel:
    model = WorldModel()
    state = torch.load(CHECKPOINT_PATH, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()
    return model
