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

"""A Morse code device simulated on qubits.

A message is translated into Morse code, then into an ITU-timed pulse train
(dot = 1 unit on, dash = 3 units on, intra-character gap = 1 unit off,
inter-character gap = 3 units off, inter-word gap = 7 units off). That pulse
train is "transmitted" by writing each bit onto a qubit with an X gate and
reading it back with a measurement, then decoded back into text.
"""

import argparse
from itertools import groupby

import cirq

MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
}
REVERSE_MORSE_CODE = {code: letter for letter, code in MORSE_CODE.items()}


def text_to_morse(text: str) -> str:
    """Convert `text` to Morse, letters space-separated, words separated by ' / '."""
    words = text.upper().split(" ")
    morse_words = []
    for word in words:
        letters = [MORSE_CODE[ch] for ch in word if ch in MORSE_CODE]
        morse_words.append(" ".join(letters))
    return " / ".join(morse_words)


def morse_to_text(morse: str) -> str:
    words = morse.split(" / ")
    decoded_words = []
    for word in words:
        letters = word.split(" ")
        decoded_words.append("".join(REVERSE_MORSE_CODE.get(letter, "") for letter in letters))
    return " ".join(decoded_words)


def morse_to_pulse_train(morse: str) -> str:
    """Encode Morse text as an ITU-timed bit string of dots, dashes, and gaps."""
    word_pulses = []
    for word in morse.split(" / "):
        letter_pulses = []
        for letter in word.split(" "):
            symbol_pulses = ["1" if symbol == "." else "111" for symbol in letter]
            letter_pulses.append("0".join(symbol_pulses))
        word_pulses.append("000".join(letter_pulses))
    return "0000000".join(word_pulses)


def pulse_train_to_morse(pulse_train: str) -> str:
    """Inverse of morse_to_pulse_train: read run lengths back into Morse text."""
    morse = []
    for bit, group in groupby(pulse_train):
        length = sum(1 for _ in group)
        if bit == "1":
            morse.append("." if length == 1 else "-")
        elif length >= 7:
            morse.append(" / ")
        elif length >= 3:
            morse.append(" ")
        # length 1 zero-run is the intra-character gap: no separator needed.
    return "".join(morse)


def transmit_via_qubits(pulse_train: str, batch_size: int = 16) -> str:
    """Write `pulse_train` onto qubits with X gates and read it back via measurement.

    Batched to keep each simulated state vector to at most 2**batch_size, since
    simulating the whole pulse train's worth of qubits at once would need
    2**len(pulse_train) amplitudes.
    """
    simulator = cirq.Simulator()
    received = []

    for start in range(0, len(pulse_train), batch_size):
        chunk = pulse_train[start : start + batch_size]
        qubits = cirq.LineQubit.range(len(chunk))
        circuit = cirq.Circuit(cirq.X(q) for q, bit in zip(qubits, chunk) if bit == "1")
        circuit.append(cirq.measure(*qubits, key="pulses"))

        result = simulator.run(circuit, repetitions=1)
        received.append("".join(str(b) for b in result.measurements["pulses"][0]))

    return "".join(received)


EXAMPLE_MESSAGES = ["SOS HELP", "HELLO", "CQ DE W1AW 73", "A"]


def run_message(message: str) -> str:
    """Encode `message`, send it through the simulated qubits, decode it, and print each stage.

    Returns the decoded text so callers (or a script) can check it against the input.
    """
    print(f"Message: {message!r}")

    # Text -> Morse: standard dot/dash notation, letters space-separated, words separated by '/'.
    morse = text_to_morse(message)
    print(f"\nMorse:       {morse}")

    # Morse -> pulse train: ITU timing as a bit string (dot=1 unit on, dash=3, gaps of 1/3/7).
    pulse_train = morse_to_pulse_train(morse)
    print(f"Pulse train: {pulse_train}")

    # The "device": each pulse bit is written onto a qubit with X and read back by measuring it.
    received = transmit_via_qubits(pulse_train)
    print(f"\nRead back from qubits: {received}")
    # True as long as the qubits round-trip the bits faithfully (no noise is simulated here).
    print(f"Matches sent pulses:   {received == pulse_train}")

    # Pulse train -> Morse -> text: the inverse of the two encoding steps above.
    decoded_morse = pulse_train_to_morse(received)
    decoded_text = morse_to_text(decoded_morse)
    print(f"\nDecoded Morse: {decoded_morse}")
    print(f"Decoded text:  {decoded_text!r}")

    return decoded_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Encode a message as Morse, transmit it through simulated qubits, decode it back."
    )
    parser.add_argument(
        "message",
        nargs="?",
        default=None,
        help="Text to send (letters, digits, spaces). Omit to run the built-in example messages instead.",
    )
    args = parser.parse_args()

    if args.message is not None:
        run_message(args.message)
        return

    print("No message given, running the built-in examples instead.\n")
    for index, message in enumerate(EXAMPLE_MESSAGES):
        if index > 0:
            print()
        run_message(message)


if __name__ == "__main__":
    main()
