# QuantumPOC

Small proof-of-concept scripts exploring quantum computing, mostly with
[Cirq](https://quantumai.google/cirq), Google's Python framework for building and simulating
quantum circuits.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

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
