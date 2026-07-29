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

"""A classical random-graph baseline, for contrast with the quantum-derived geometry.

Same node/edge shape and the same layout_geometry() mapping as the quantum
path, but the "entropy" values driving it come from a seeded RNG instead of
a real quantum circuit -- so any structure visible in the quantum geometry
that's absent here is coming from actual entanglement, not from the layout
math itself.
"""

import numpy as np

from app.happy_code import NUM_QUBITS, S_EDGE_MAX, S_MAX, layout_geometry


def classical_geometry(seed: int) -> dict:
    rng = np.random.default_rng(seed)
    single = rng.uniform(0, S_MAX, size=NUM_QUBITS).tolist()
    edges = rng.uniform(0, S_EDGE_MAX, size=NUM_QUBITS).tolist()
    return layout_geometry(single, edges)
