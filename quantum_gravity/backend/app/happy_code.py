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

"""A toy HaPPY-code-inspired model of emergent bulk geometry.

Six qubits sit on a boundary circle. Adjacent boundary qubits are entangled
by a tunable RY-then-CX gate pair, so the "entanglement strength" of each
ring edge is a real, continuous circuit parameter. From the resulting
6-qubit state we compute genuine von Neumann entanglement entropies (via
partial trace, not an approximation), and use a simplified
Ryu-Takayanagi-style rule -- more boundary entanglement pushes the
corresponding bulk point outward, toward the boundary, echoing the RT area
law's own direction (more entropy, a larger minimal surface); weak
entanglement leaves that point pulled inward toward the center -- to derive
a deformable bulk geometry.

This is an explicit toy model: a real quantum circuit and real entropies,
but a simplified geometric mapping, not an exact minimal-surface
computation or a rigorous HaPPY perfect-tensor code.

Note on a real, verified quirk of this circuit: because CX(i, i+1) fires on
every ring edge regardless of that edge's own strength, and boundary qubits
are shared between adjacent edges, entanglement can propagate all the way
around the ring from a single slider. That's not a bug -- it's a genuine
consequence of the shared-qubit ring topology, and a fitting echo of
AdS/CFT non-locality.
"""

import math

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, entropy, partial_trace

NUM_QUBITS = 6

S_MAX = 1.0
"""Max single-qubit von Neumann entropy, in bits. Normalizes bulk radius.

Radius scales with S_i / S_MAX, so more entanglement pushes the bulk node
outward (toward the boundary) and weak entanglement leaves it near the
center -- the same direction the RT area law relates entropy to surface
area, not a literal area computation.
"""

S_EDGE_MAX = 2.0
"""Max two-qubit block entropy, in bits (verified numerically, not 1.0). Used only for edge visual scaling."""

R_MAX = 200.0
"""Boundary circle radius in px; also the max bulk node radius."""

R_MIN = 40.0
"""Min bulk node radius in px, so the bulk polygon never collapses to a point."""

ANGLE_OFFSET = -math.pi / 2
"""Rotate the layout so boundary qubit 0 sits at 12 o'clock."""


def _clean(value: float) -> float:
    """Normalize signed -0.0 (a real artifact of entropy()'s floating-point sum) to 0.0."""
    return 0.0 if value == 0 else float(value)


def build_circuit(strengths: list[float]) -> QuantumCircuit:
    """Build the 6-qubit boundary ring circuit for the given per-edge strengths in [0, 1]."""
    qc = QuantumCircuit(NUM_QUBITS)
    for i, strength in enumerate(strengths):
        theta = strength * (math.pi / 2)
        qc.ry(theta, i)
        qc.cx(i, (i + 1) % NUM_QUBITS)
    return qc


def compute_entropies(qc: QuantumCircuit) -> tuple[list[float], list[float]]:
    """Return (S_i x6, S_edge_i x6): single-qubit and adjacent-pair entanglement entropies."""
    state = Statevector.from_instruction(qc)

    single = []
    for i in range(NUM_QUBITS):
        trace_out = [q for q in range(NUM_QUBITS) if q != i]
        reduced = partial_trace(state, trace_out)
        single.append(_clean(entropy(reduced, base=2)))

    edges = []
    for i in range(NUM_QUBITS):
        j = (i + 1) % NUM_QUBITS
        trace_out = [q for q in range(NUM_QUBITS) if q not in (i, j)]
        reduced = partial_trace(state, trace_out)
        edges.append(_clean(entropy(reduced, base=2)))

    return single, edges


def layout_geometry(single_entropies: list[float], edge_entropies: list[float]) -> dict:
    """Turn per-qubit and per-edge entropies into boundary/bulk node and edge coordinates.

    Pure function (no Qiskit dependency) so both the quantum path and the
    classical random-graph baseline can share the exact same geometric mapping.
    """
    boundary_nodes = []
    bulk_nodes = []

    for i in range(NUM_QUBITS):
        angle = ANGLE_OFFSET + (2 * math.pi * i / NUM_QUBITS)
        bx = R_MAX * math.cos(angle)
        by = R_MAX * math.sin(angle)
        boundary_nodes.append(
            {"index": i, "angle": angle, "x": bx, "y": by, "entropy": single_entropies[i]}
        )

        radius = R_MAX * (single_entropies[i] / S_MAX)
        radius = max(R_MIN, min(R_MAX, radius))
        ix = radius * math.cos(angle)
        iy = radius * math.sin(angle)
        bulk_nodes.append({"index": i, "angle": angle, "x": ix, "y": iy, "radius": radius})

    boundary_edges = [
        {"index": i, "source": i, "target": (i + 1) % NUM_QUBITS, "entropy": edge_entropies[i]}
        for i in range(NUM_QUBITS)
    ]
    bulk_edges = [
        {"source": i, "target": (i + 1) % NUM_QUBITS} for i in range(NUM_QUBITS)
    ]

    return {
        "boundary_nodes": boundary_nodes,
        "boundary_edges": boundary_edges,
        "bulk_nodes": bulk_nodes,
        "bulk_edges": bulk_edges,
    }


def quantum_geometry(strengths: list[float]) -> dict:
    """Build the ring circuit, compute real entanglement entropies, and derive bulk geometry."""
    qc = build_circuit(strengths)
    single, edges = compute_entropies(qc)
    return layout_geometry(single, edges)
