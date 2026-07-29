# QuantumPOC

Small proof-of-concept scripts exploring [Cirq](https://quantumai.google/cirq), Google's Python
framework for building and simulating quantum circuits.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

## `hello_hilbert.py`

A "hello world" for quantum circuits. It converts a message into binary, encodes the first 8
bits (one character) onto 8 qubits with `X` gates, puts every qubit into superposition with `H`,
then measures.

```bash
./.venv/bin/python hello_hilbert.py
```

This is an *encoding* demo, not encryption — the `X` gates just set qubit basis states to match
the message bits, and measuring right after `H` throws that information away, collapsing each
qubit to a random 0/1. Only 8 bits are encoded because simulating a full state vector scales as
2^n, and the message's full binary form (104 bits for "hello hilbert") would be infeasible to
simulate.

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

Reuses `string_to_binary` from `hello_hilbert.py`, so both files need to stay in the same
directory.
