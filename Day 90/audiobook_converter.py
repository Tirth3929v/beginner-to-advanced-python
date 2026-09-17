"""
Day 90: Convert PDF to Audiobook Engine
Extracts text from PDF documents using pypdf and synthesizes spoken MP3 audio via gTTS.
"""

import os
import re
from typing import Tuple, Dict
import pypdf
from gtts import gTTS


class AudiobookConverter:
    @staticmethod
    def extract_text(pdf_path: str) -> Tuple[str, int]:
        """Extracts text content across all pages in a PDF document."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        reader = pypdf.PdfReader(pdf_path)
        total_pages = len(reader.pages)

        extracted_chunks = []
        for i, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            if txt.strip():
                extracted_chunks.append(txt.strip())

        full_text = "\n\n".join(extracted_chunks)
        # Normalize whitespace
        cleaned_text = re.sub(r"[ \t]+", " ", full_text)
        return cleaned_text, total_pages

    @staticmethod
    def get_text_metrics(text: str) -> Dict[str, any]:
        words = text.split()
        word_count = len(words)
        # Average reading speed: 150 words per minute
        est_minutes = round(word_count / 150.0, 1)
        return {
            "char_count": len(text),
            "word_count": word_count,
            "estimated_audio_minutes": est_minutes
        }

    @staticmethod
    def convert_to_mp3(text: str, output_path: str, lang: str = "en", slow: bool = False) -> str:
        """Synthesizes text into spoken MP3 audio."""
        if not text.strip():
            raise ValueError("Cannot synthesize audio from empty text.")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_file = os.path.join(base_dir, output_path) if not os.path.isabs(output_path) else output_path

        # Truncate for demonstration if excessively long
        synthesis_text = text if len(text) < 5000 else text[:5000] + " ... End of preview chapter."

        tts = gTTS(text=synthesis_text, lang=lang, slow=slow)
        tts.save(target_file)
        return target_file
