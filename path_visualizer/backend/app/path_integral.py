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

"""A 2D Feynman path-integral Monte Carlo simulation.

Feynman's idea: a particle going from a start point to an end point doesn't
take one path -- every possible path contributes an amplitude e^(iS/hbar),
where S is the classical action along that path. Summing the amplitudes of
many paths and squaring the result gives the real, observable interference
pattern. Where nearby paths have similar action, their phases agree and add
constructively (bright); where action varies quickly between nearby paths,
phases scramble and cancel (dark).

At small hbar, S/hbar changes very fast as a path deviates from the
classical (least-action) trajectory, so almost everything cancels except a
narrow bundle of near-classical paths -- the field collapses to a single
trajectory. At large hbar, that phase changes slowly, so a wide spread of
different paths still interfere constructively, producing rich fringe and
lattice structure. This is the textbook stationary-phase argument for how
classical mechanics emerges from quantum mechanics, made visible.
"""

import numpy as np

GRID_SIZE = 64
NUM_SEGMENTS = 48
"""Points per sampled path minus one. Changing this requires re-deriving SPREAD (see below)."""

DOMAIN_MIN = -1.0
DOMAIN_MAX = 1.0

HBAR_MIN = 0.02
HBAR_MAX = 2.5
HBAR_DEFAULT = float(np.sqrt(HBAR_MIN * HBAR_MAX))

NUM_PATHS_MIN = 1
NUM_PATHS_MAX = 500
NUM_PATHS_DEFAULT = 150

SPREAD_BASE = 0.08
"""Per-axis stddev (domain units) of detour noise at HBAR_REF. Not a free aesthetic knob.

Two things had to be true for the quantum<->classical slider to visibly do
anything, and neither holds if the sampling width is a flat constant:

1. Each of the NUM_SEGMENTS+1 path points gets *independent* Gaussian noise
   (not a correlated random walk), so its magnitude doesn't shrink with dt
   the way a literal Wiener path would -- a typical detour path's action
   scales as E[S] ~= (NUM_SEGMENTS**2 / 3) * spread**2, not tied to hbar.
2. With a *fixed* sampling width, "collapse to the classical path" would
   have to come entirely from destructive phase cancellation among
   otherwise-identically-distributed paths -- which needs far more samples
   per grid cell than a responsive UI slider (num_paths <= 500) can afford;
   below that, finite-sample phase noise ("speckle") swamps the real
   cancellation and the field looks like undifferentiated noise at every
   hbar.

Fix: make the *sampling width itself* scale as sqrt(hbar/HBAR_REF), which is
exactly the semiclassical/WKB result -- expanding the action to quadratic
order around the classical path, the phase stays of order 1 radian out to a
detour size of order sqrt(hbar). So small hbar narrows the physical corridor
paths are drawn from (a real, visible "collapse"), while the *phase*
computation (still using the same hbar in e^(iS/hbar)) independently adds
genuine interference texture inside whatever corridor width results. Verified
numerically (see path_visualizer physics sanity checks) that this produces a
visibly narrow, high-contrast band at HBAR_MIN and a visibly wide, richly
textured field at HBAR_MAX with realistic num_paths values.
"""

HBAR_REF = HBAR_DEFAULT


def _bridge_spread(hbar: float) -> float:
    return SPREAD_BASE * np.sqrt(hbar / HBAR_REF)


def _sample_paths(
    start: np.ndarray, end: np.ndarray, num_paths: int, hbar: float, rng: np.random.Generator
) -> np.ndarray:
    """Brownian-bridge-perturbed straight lines from start to end. Shape (num_paths, NUM_SEGMENTS+1, 2)."""
    t = np.linspace(0.0, 1.0, NUM_SEGMENTS + 1)
    straight = start[None, :] + t[:, None] * (end - start)[None, :]

    spread = _bridge_spread(hbar)
    noise = rng.normal(0.0, spread, size=(num_paths, NUM_SEGMENTS + 1, 2))
    noise[:, 0, :] = 0.0
    noise[:, -1, :] = 0.0

    bridge_scale = np.sqrt(t * (1.0 - t))[None, :, None]
    return straight[None, :, :] + noise * bridge_scale


def _path_actions(paths: np.ndarray, dt: float) -> np.ndarray:
    """Discretized free-particle action S = sum 0.5*|dp|^2/dt per path. Shape (num_paths,)."""
    diffs = np.diff(paths, axis=1)
    segment_action = 0.5 * np.sum(diffs**2, axis=2) / dt
    return segment_action.sum(axis=1)


def _to_grid_indices(paths: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Map path points from [DOMAIN_MIN, DOMAIN_MAX] to grid row/col indices, clipped to bounds."""
    frac = (paths - DOMAIN_MIN) / (DOMAIN_MAX - DOMAIN_MIN)
    idx = np.clip((frac * GRID_SIZE).astype(int), 0, GRID_SIZE - 1)
    col = idx[..., 0]  # x -> column
    row = idx[..., 1]  # y -> row; row 0 corresponds to y = DOMAIN_MIN
    return row, col


def compute_field(
    start: list[float],
    end: list[float],
    num_paths: int,
    hbar: float,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Sample num_paths random paths, sum their complex phases onto a grid, return normalized intensity."""
    rng = rng if rng is not None else np.random.default_rng()
    start_arr = np.asarray(start, dtype=float)
    end_arr = np.asarray(end, dtype=float)
    dt = 1.0 / NUM_SEGMENTS

    paths = _sample_paths(start_arr, end_arr, num_paths, hbar, rng)
    actions = _path_actions(paths, dt)
    weights = np.exp(1j * actions / hbar)

    rows, cols = _to_grid_indices(paths)
    point_weights = np.repeat(weights[:, None], NUM_SEGMENTS + 1, axis=1)

    field = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.complex128)
    np.add.at(field, (rows.ravel(), cols.ravel()), point_weights.ravel())

    intensity = np.abs(field) ** 2
    peak = intensity.max()
    if peak > 0:
        intensity = intensity / peak
    return intensity
