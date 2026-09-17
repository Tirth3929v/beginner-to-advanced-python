"""
Day 81: International Morse Code Engine & Audio Synthesizer
Bidirectional text translation and standard 800Hz PCM WAV audio generation.
"""

import os
import math
import struct
import wave
import sys
from typing import Tuple

# International Morse Code Specification (ITU-R M.1677-1)
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '@': '.--.-.', '!': '-.-.--', '&': '.-...', "'": '.----.',
    '"': '.-..-.'
}

REVERSE_MORSE_DICT = {code: char for char, code in MORSE_CODE_DICT.items()}


class MorseEngine:
    @staticmethod
    def encode(text: str) -> str:
        """Converts plaintext to Morse Code. Letters separated by space, words by ' / '."""
        words = text.strip().upper().split()
        encoded_words = []
        for word in words:
            encoded_chars = []
            for char in word:
                if char in MORSE_CODE_DICT:
                    encoded_chars.append(MORSE_CODE_DICT[char])
                else:
                    encoded_chars.append(char)
            encoded_words.append(" ".join(encoded_chars))
        return " / ".join(encoded_words)

    @staticmethod
    def decode(morse_code: str) -> str:
        """Converts Morse Code back to uppercase plaintext."""
        words = morse_code.strip().split(" / ")
        decoded_words = []
        for word in words:
            chars = word.strip().split()
            decoded_chars = []
            for c in chars:
                if c in REVERSE_MORSE_DICT:
                    decoded_chars.append(REVERSE_MORSE_DICT[c])
                else:
                    decoded_chars.append(c)
            decoded_words.append("".join(decoded_chars))
        return " ".join(decoded_words)

    @staticmethod
    def synthesize_wav(morse_code: str, output_path: str = "morse_signal.wav", wpm: int = 15) -> str:
        """
        Synthesizes standard 800Hz audio tones and exports as a standalone WAV file.
        WPM calculation uses Paris standard: unit duration = 1200 / wpm (in ms).
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, output_path)

        sample_rate = 44100
        frequency = 800.0  # 800 Hz pitch standard for telegraphy
        dot_duration = 1.2 / wpm  # seconds

        samples = []

        def add_tone(duration: float):
            num_samples = int(sample_rate * duration)
            for i in range(num_samples):
                # Apply envelope fading at edges to eliminate clicking noise
                envelope = 1.0
                fade_len = int(sample_rate * 0.005)
                if i < fade_len:
                    envelope = i / fade_len
                elif i > num_samples - fade_len:
                    envelope = (num_samples - i) / fade_len

                val = envelope * 0.5 * math.sin(2.0 * math.pi * frequency * (i / sample_rate))
                samples.append(int(val * 32767))

        def add_silence(duration: float):
            num_samples = int(sample_rate * duration)
            samples.extend([0] * num_samples)

        for symbol in morse_code:
            if symbol == '.':
                add_tone(dot_duration)
                add_silence(dot_duration)  # intra-char space (1 unit)
            elif symbol == '-':
                add_tone(dot_duration * 3)
                add_silence(dot_duration)  # intra-char space (1 unit)
            elif symbol == ' ':
                add_silence(dot_duration * 2)  # inter-char space total 3 units
            elif symbol == '/':
                add_silence(dot_duration * 4)  # inter-word space total 7 units

        # Pack binary PCM into WAV
        with wave.open(full_path, "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            raw_data = struct.pack(f"<{len(samples)}h", *samples)
            wav_file.writeframes(raw_data)

        return full_path

    @staticmethod
    def play_live_beeps(morse_code: str):
        """Plays real-time audio through system beeper if supported on Windows."""
        if sys.platform == "win32":
            try:
                import winsound
                freq = 800
                dot_ms = 80
                dash_ms = dot_ms * 3
                import time
                for symbol in morse_code:
                    if symbol == '.':
                        winsound.Beep(freq, dot_ms)
                        time.sleep(dot_ms / 1000)
                    elif symbol == '-':
                        winsound.Beep(freq, dash_ms)
                        time.sleep(dot_ms / 1000)
                    elif symbol == ' ':
                        time.sleep((dot_ms * 2) / 1000)
                    elif symbol == '/':
                        time.sleep((dot_ms * 4) / 1000)
            except Exception as e:
                print(f"(Beep notification: {e})")
