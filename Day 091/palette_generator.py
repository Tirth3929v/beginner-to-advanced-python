"""
Day 91: K-Means Image Color Palette Extractor
Extracts dominant color clusters from digital images and generates visual palette swatches.
"""

import os
from typing import List, Dict, Tuple
import numpy as np
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans


class ColorPaletteGenerator:
    @staticmethod
    def create_sample_artwork(filename: str = "sample_artwork.png") -> str:
        """Synthesizes a rich colorful artwork with blues, teals, golds, and purples."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, filename)

        img = Image.new("RGB", (400, 400), color="#0f172a")
        draw = ImageDraw.Draw(img)

        # Concentric color rings
        draw.ellipse([50, 50, 350, 350], fill="#0284c7")
        draw.ellipse([90, 90, 310, 310], fill="#38bdf8")
        draw.ellipse([130, 130, 270, 270], fill="#f59e0b")
        draw.ellipse([170, 170, 230, 230], fill="#ec4899")

        img.save(path)
        return path

    @staticmethod
    def extract_palette(image_path: str, num_colors: int = 6) -> List[Dict[str, any]]:
        """
        Extracts dominant color palette using K-Means clustering.
        Returns list of dicts: [{'rgb': (r,g,b), 'hex': '#RRGGBB', 'percent': 35.2}, ...]
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        img = Image.open(image_path).convert("RGB")
        # Resize to thumbnail to accelerate K-Means while maintaining color distribution
        img.thumbnail((150, 150))

        pixels = np.array(img).reshape(-1, 3)

        # Fit KMeans
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=5)
        labels = kmeans.fit_predict(pixels)

        counts = np.bincount(labels)
        total_pixels = len(labels)

        # Order by frequency descending
        sorted_indices = np.argsort(-counts)

        palette = []
        for idx in sorted_indices:
            centroid = kmeans.cluster_centers_[idx].astype(int)
            r, g, b = int(centroid[0]), int(centroid[1]), int(centroid[2])
            hex_code = f"#{r:02x}{g:02x}{b:02x}".upper()
            pct = round((counts[idx] / total_pixels) * 100.0, 1)
            palette.append({
                "rgb": (r, g, b),
                "hex": hex_code,
                "percent": pct
            })

        return palette

    @staticmethod
    def export_palette_swatch(palette: List[Dict[str, any]], output_file: str = "palette_swatch.png") -> str:
        """Generates a high-resolution horizontal color swatch graphic."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, output_file)

        num_c = len(palette)
        swatch_w = 120
        height = 160
        total_w = swatch_w * num_c

        canvas = Image.new("RGB", (total_w, height), color="#ffffff")
        draw = ImageDraw.Draw(canvas)

        for i, item in enumerate(palette):
            x0 = i * swatch_w
            x1 = x0 + swatch_w
            draw.rectangle([x0, 0, x1, 110], fill=item["rgb"])
            # Label area below swatch
            draw.text((x0 + 15, 120), item["hex"], fill="#0f172a")
            draw.text((x0 + 15, 138), f"{item['percent']}%", fill="#64748b")

        canvas.save(path)
        return path
