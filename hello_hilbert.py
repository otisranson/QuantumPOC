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

"""Hello Hilbert: encode a message's bits onto qubits and watch them superpose."""

import cirq


def string_to_binary(text: str) -> str:
    """Convert each character of `text` into an 8-bit binary string."""
    return "".join(format(ord(char), "08b") for char in text)


def hello_hilbert(qubits: list[cirq.Qid], binary: str) -> cirq.Circuit:
    """Build a circuit that encodes `binary` onto `qubits`, then superposes and measures them.

    Only min(len(qubits), len(binary)) bits are encoded; any extra qubits stay at |0>.
    """
    circuit = cirq.Circuit()

    for qubit, bit in zip(qubits, binary):
        if bit == "1":
            circuit.append(cirq.X(qubit))

    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(cirq.measure(*qubits, key="result"))
    return circuit


def main() -> None:
    message = "hello hilbert"
    binary = string_to_binary(message)
    print(f"Message: {message!r}")
    print(f"Binary:  {binary} ({len(binary)} bits)")

    # Simulating a full state vector scales as 2^n, so we only encode the
    # first character's worth of bits (8) to keep the demo instant.
    qubits = cirq.LineQubit.range(8)
    circuit = hello_hilbert(qubits, binary)

    print("\nCircuit:")
    print(circuit)

    result = cirq.Simulator().run(circuit, repetitions=5)
    print("\nMeasurements over 5 runs (randomized by the Hadamards):")
    print(result)


if __name__ == "__main__":
    main()
