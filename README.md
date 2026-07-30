# QuantumPOC

Small proof-of-concept scripts exploring quantum computing, mostly with
[Cirq](https://quantumai.google/cirq), Google's Python framework for building and simulating
quantum circuits.

## Contents

- [`quantum_encrypt.py`](#quantum_encryptpy) — quantum random number generator one-time pad
- [`quantum_morse/quantum_morse.py`](#quantum_morsequantum_morsepy) — Morse code over qubits
- [`quantum_gravity/`](#quantum_gravity) — emergent bulk geometry from a toy HaPPY code
- [`path_visualizer/`](#path_visualizer) — Feynman path-integral field with a learned world model

## Prerequisites

- **Python 3.10+** — for `quantum_encrypt.py`, `quantum_morse/`, and the backends of
  `quantum_gravity/` and `path_visualizer/`.
- **Node.js 18+ with npm** — only needed for the frontends of `quantum_gravity/` and
  `path_visualizer/`; the other two scripts don't touch it.

## Setup

This installs the dependencies for the two plain scripts below
(`quantum_encrypt.py`, `quantum_morse/`):

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

`quantum_gravity/` and `path_visualizer/` are self-contained and don't use this venv — each has
its own `run.sh` that creates its own backend venv and installs its own frontend dependencies on
first run, as described in their sections below.

## `quantum_encrypt.py`

Real encryption: a one-time pad keyed by a quantum random number generator. Hadamard-superposed
qubits are measured (in batches, to keep each simulated state vector small) to produce a key of
genuinely random bits, which is then XORed with the message's binary form.

```bash
./.venv/bin/python quantum_encrypt.py
```

It also decrypts the ciphertext with a second, different random key to show the result is
garbage — a one-time pad is only secure if the exact same key is reused for decryption, is truly
random, is the same length as the message, is never reused, and stays secret.

## `quantum_morse/quantum_morse.py`

A Morse code device simulated on qubits. A message is translated to Morse, then to an ITU-timed
pulse train (dot = 1 unit on, dash = 3, gaps of 1/3/7 units for symbol/letter/word boundaries).
Each pulse bit is "transmitted" by writing it onto a qubit with an `X` gate and reading it back
via measurement (batched, to keep each simulated state vector small), then decoded back through
Morse to text.

```bash
./.venv/bin/python quantum_morse/quantum_morse.py "your message here"
```

Run with no argument to instead run through a set of built-in example messages
(`SOS HELP`, `HELLO`, `CQ DE W1AW 73`, `A`).

## `quantum_gravity/`

A full-stack toy demo of emergent bulk geometry from boundary entanglement, loosely inspired by
the HaPPY code (a holographic quantum error-correcting code from the AdS/CFT correspondence).
Six "boundary" qubits sit in a ring; a [Qiskit](https://www.ibm.com/quantum/qiskit) circuit
entangles adjacent pairs by a tunable amount, and real von Neumann entanglement entropies
(computed via partial trace, not approximated) are used to derive a deformable interior "bulk"
geometry — more entanglement pushes the bulk outward toward the boundary, echoing the direction
the Ryu-Takayanagi formula relates entropy to minimal-surface area; weak entanglement leaves it
collapsed toward the center.
A FastAPI backend exposes the geometry (and a classical random-graph baseline for contrast) as
JSON; a React + D3 frontend renders it live, with sliders to tune entanglement strength per edge
and a toggle to compare the quantum-derived geometry against the classical baseline.

```bash
./quantum_gravity/run.sh
```

Then open the URL Vite prints (typically http://localhost:5173). This single command creates a
Python virtualenv and installs backend dependencies if needed, installs frontend dependencies if
needed, and starts both the FastAPI backend and the Vite dev server.

## `path_visualizer/`

A toy Feynman path-integral simulator, rendered as a live interference field between two
draggable points. Feynman's picture of quantum mechanics: a particle going from a start point to
an end point doesn't take one path — every possible path contributes an amplitude `e^(iS/hbar)`,
where `S` is the classical action along that path. Add up the amplitudes of many sampled paths
and square the result, and you get a real, observable interference pattern: where nearby paths
have similar action their phases agree and add up brightly, where action varies quickly between
nearby paths the phases scramble and cancel out to darkness. Shrinking `hbar` makes that phase
spin faster for the same amount of detour, so only paths that stay close to the classical
(least-action) trajectory keep interfering constructively — the field visibly narrows toward a
single clean path. Growing `hbar` widens that same window, letting a much broader spread of paths
interfere and produce rich fringe and lattice structure. This is the standard stationary-phase
argument for how classical mechanics emerges from quantum mechanics, made interactive.

The glowing field is not "the path" — it's the overlay of every sampled path at once. Brightness
at a point means many different routes reinforce each other passing through it; darkness means
they cancel out even though some path did go through that spot. What looks like a single clean
trajectory at the classical extreme is just what's left once only the near-straight-line paths
still agree with each other. (This is superposition over one particle's histories, not
entanglement — entanglement needs two or more separate quantum systems correlated with each
other, which is a different phenomenon demonstrated instead in `quantum_gravity/` above.)

A second endpoint serves a small PyTorch network trained to predict the same field directly from
`(start, end, hbar)`, without ever running the simulator — the same basic idea behind "world
models" in AI: instead of repeatedly querying an expensive environment or simulator, train a fast
network that mimics its output well enough to sample cheaply afterward. Toggling between
"computed" and "learned" shows the trade-off directly: the learned field is visibly blurrier, the
gross shape without the fine simulated texture, since a small non-convolutional network naturally
smooths over what it wasn't given enough capacity or data to memorize exactly.

```bash
./path_visualizer/run.sh
```

Same single-command setup as `quantum_gravity/` — this one also trains the world model on its
very first run (a few hundred quick examples generated from the real simulator, ~15-30 seconds on
CPU) before it starts serving; later runs just load the cached model and start immediately. Once
it's running, open http://localhost:5173 (the same URL Vite prints in the terminal) and try:

- **Drag the two dots** to move the start and end points — the field recomputes live.
- **The ħ slider** ("quantum ↔ classical") — slide toward classical to watch the field collapse
  into a single clean trajectory; slide toward quantum to watch it bloom into fringes.
- **The paths slider** — how many random paths get sampled per request; more paths, richer detail.
- **The computed/learned toggle** — compare the real simulation against the trained network's
  (visibly blurrier) guess at the same field.
