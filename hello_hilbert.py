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
