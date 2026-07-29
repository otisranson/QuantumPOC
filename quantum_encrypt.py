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

"""Encrypt a string with a one-time pad keyed by a quantum random number generator.

A Hadamard on |0> puts a qubit into an equal superposition; measuring it in the
computational basis then collapses it to a genuinely random 0 or 1 (not a
pseudo-random one). Using that as a one-time-pad key is real, information-
theoretically secure encryption -- provided the key is truly random, as long
as the message, used only once, and never shared with anyone but the parties
who need it.
"""

import cirq

from hello_hilbert import string_to_binary


def binary_to_string(binary: str) -> str:
    """Inverse of string_to_binary: decode 8-bit chunks back into characters."""
    chars = (binary[i : i + 8] for i in range(0, len(binary), 8))
    return "".join(chr(int(byte, 2)) for byte in chars)


def xor_bits(a: str, b: str) -> str:
    return "".join("0" if x == y else "1" for x, y in zip(a, b))


def quantum_random_bits(n: int, batch_size: int = 16) -> str:
    """Generate n random bits by measuring Hadamard-superposed qubits, in small batches.

    Batching keeps each simulated state vector to at most 2**batch_size, since
    simulating all n qubits at once would need 2**n amplitudes.
    """
    simulator = cirq.Simulator()
    bits = []
    remaining = n

    while remaining > 0:
        chunk = min(batch_size, remaining)
        qubits = cirq.LineQubit.range(chunk)
        circuit = cirq.Circuit(cirq.H(q) for q in qubits)
        circuit.append(cirq.measure(*qubits, key="key"))

        result = simulator.run(circuit, repetitions=1)
        bits.append("".join(str(b) for b in result.measurements["key"][0]))
        remaining -= chunk

    return "".join(bits)


def encrypt(message: str) -> tuple[str, str]:
    """Return (ciphertext_bits, key) for `message`, encrypted with a quantum one-time pad."""
    plaintext_bits = string_to_binary(message)
    key = quantum_random_bits(len(plaintext_bits))
    ciphertext_bits = xor_bits(plaintext_bits, key)
    return ciphertext_bits, key


def decrypt(ciphertext_bits: str, key: str) -> str:
    plaintext_bits = xor_bits(ciphertext_bits, key)
    return binary_to_string(plaintext_bits)


def main() -> None:
    message = "hello hilbert"
    print(f"Message: {message!r}")

    ciphertext_bits, key = encrypt(message)
    ciphertext_bytes = int(ciphertext_bits, 2).to_bytes(len(ciphertext_bits) // 8, "big")

    print(f"\nQuantum-generated key: {key}")
    print(f"Ciphertext (bits):     {ciphertext_bits}")
    print(f"Ciphertext (hex):      {ciphertext_bytes.hex()}")

    recovered = decrypt(ciphertext_bits, key)
    print(f"\nDecrypted with correct key: {recovered!r}")

    wrong_key = quantum_random_bits(len(key))
    garbled = decrypt(ciphertext_bits, wrong_key)
    print(f"Decrypted with wrong key:   {garbled!r}")


if __name__ == "__main__":
    main()
