"""
Day 84: Image Watermarking Engine
Supports text watermarking, logo overlays, opacity blending, and batch processing.
"""

import os
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont


class WatermarkEngine:
    @staticmethod
    def create_sample_image(filename: str = "sample_photo.png", width: int = 800, height: int = 600) -> str:
        """Generates a pleasant scenic gradient test photo."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, filename)

        img = Image.new("RGB", (width, height), color="#0f172a")
        draw = ImageDraw.Draw(img)

        # Draw a sunset/mountain landscape
        draw.ellipse([width//2 - 100, 80, width//2 + 100, 280], fill="#f59e0b")  # Sun
        draw.polygon([(0, height), (width//3, height//2), (width*2//3, height)], fill="#334155")  # Mountain 1
        draw.polygon([(width//4, height), (width*3//5, height*2//5), (width, height)], fill="#1e293b")  # Mountain 2

        img.save(path)
        return path

    @staticmethod
    def apply_text_watermark(
        image_path: str,
        text: str,
        output_path: str,
        position: str = "bottom-right",
        opacity: float = 0.6,
        font_size: int = 36,
        color: Tuple[int, int, int] = (255, 255, 255)
    ) -> str:
        """
        Applies a transparent text watermark onto an image.
        Position options: 'bottom-right', 'bottom-left', 'top-right', 'top-left', 'center', 'tiled'.
        """
        base_image = Image.open(image_path).convert("RGBA")
        width, height = base_image.size

        # Create transparent overlay
        txt_overlay = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_overlay)

        # Use default font or truetype
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        alpha = int(255 * max(0.0, min(1.0, opacity)))
        rgba_color = (color[0], color[1], color[2], alpha)

        # Calculate bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        padding = 24

        if position == "bottom-right":
            pos = (width - text_w - padding, height - text_h - padding)
            draw.text(pos, text, font=font, fill=rgba_color)
        elif position == "bottom-left":
            pos = (padding, height - text_h - padding)
            draw.text(pos, text, font=font, fill=rgba_color)
        elif position == "top-right":
            pos = (width - text_w - padding, padding)
            draw.text(pos, text, font=font, fill=rgba_color)
        elif position == "top-left":
            pos = (padding, padding)
            draw.text(pos, text, font=font, fill=rgba_color)
        elif position == "center":
            pos = ((width - text_w) // 2, (height - text_h) // 2)
            draw.text(pos, text, font=font, fill=rgba_color)
        elif position == "tiled":
            step_x = text_w + 100
            step_y = text_h + 80
            for x in range(20, width, step_x):
                for y in range(20, height, step_y):
                    draw.text((x, y), text, font=font, fill=rgba_color)

        # Alpha composite overlay onto base image
        watermarked = Image.alpha_composite(base_image, txt_overlay)
        final_img = watermarked.convert("RGB")
        final_img.save(output_path)
        return output_path
