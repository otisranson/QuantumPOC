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

"""Generates training data from the real simulator and trains the learned world model.

Called once, synchronously, from main.py's startup lifespan if no checkpoint
exists yet -- see world_model.py for what the model is and why it looks
blurrier than the live simulation.
"""

import math

import numpy as np
import torch
from torch import nn

from app.path_integral import GRID_SIZE, HBAR_MAX, HBAR_MIN, compute_field
from app.world_model import CHECKPOINT_PATH, WorldModel, featurize

N_SAMPLES = 300
NUM_PATHS_FOR_TRAINING = 80
EPOCHS = 200
BATCH_SIZE = 32
LEARNING_RATE = 1e-3
SEED = 0


def _random_endpoints(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Uniform random start/end within the domain, resampled until they're not degenerately close."""
    while True:
        start = rng.uniform(-0.9, 0.9, size=2)
        end = rng.uniform(-0.9, 0.9, size=2)
        if np.linalg.norm(end - start) > 0.3:
            return start, end


def generate_dataset(n_samples: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    features = np.zeros((n_samples, 5), dtype=np.float32)
    fields = np.zeros((n_samples, GRID_SIZE, GRID_SIZE), dtype=np.float32)

    log_hbar_min, log_hbar_max = math.log10(HBAR_MIN), math.log10(HBAR_MAX)
    for i in range(n_samples):
        start, end = _random_endpoints(rng)
        hbar = 10 ** rng.uniform(log_hbar_min, log_hbar_max)
        fields[i] = compute_field(start.tolist(), end.tolist(), NUM_PATHS_FOR_TRAINING, hbar, rng)
        features[i] = featurize(start.tolist(), end.tolist(), hbar)

    return features, fields


def train() -> WorldModel:
    rng = np.random.default_rng(SEED)
    torch.manual_seed(SEED)

    print(f"[world_model] generating {N_SAMPLES} training samples...")
    features, fields = generate_dataset(N_SAMPLES, rng)
    x = torch.from_numpy(features)
    y = torch.from_numpy(fields).view(N_SAMPLES, -1)

    model = WorldModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    loss_fn = nn.MSELoss()

    print(f"[world_model] training for {EPOCHS} epochs...")
    for epoch in range(EPOCHS):
        perm = torch.randperm(N_SAMPLES)
        epoch_loss = 0.0
        for start_idx in range(0, N_SAMPLES, BATCH_SIZE):
            idx = perm[start_idx : start_idx + BATCH_SIZE]
            batch_x, batch_y = x[idx], y[idx]

            optimizer.zero_grad()
            pred = model(batch_x).view(batch_x.size(0), -1)
            loss = loss_fn(pred, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * len(idx)

        if epoch % 50 == 0 or epoch == EPOCHS - 1:
            print(f"[world_model] epoch {epoch:4d}  loss={epoch_loss / N_SAMPLES:.5f}")

    model.eval()
    torch.save(model.state_dict(), CHECKPOINT_PATH)
    print(f"[world_model] saved checkpoint to {CHECKPOINT_PATH}")
    return model


if __name__ == "__main__":
    train()
