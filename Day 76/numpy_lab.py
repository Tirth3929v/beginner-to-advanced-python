"""
Day 76: NumPy N-Dimensional Array Lab & Tensor Processing Engine
Implements array broadcasting, linear algebra, and RGB image tensor operations.
"""

import os
import numpy as np
from PIL import Image


class MatrixLab:
    @staticmethod
    def linear_system_solver(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Solves the system Ax = b using NumPy linear algebra."""
        return np.linalg.solve(A, b)

    @staticmethod
    def matrix_properties(A: np.ndarray) -> dict:
        det = float(np.linalg.det(A))
        inv = np.linalg.inv(A) if abs(det) > 1e-9 else None
        eigenvals, eigenvecs = np.linalg.eig(A)
        return {
            "shape": A.shape,
            "determinant": det,
            "inverse": inv,
            "eigenvalues": eigenvals,
            "rank": int(np.linalg.matrix_rank(A))
        }

    @staticmethod
    def demonstrate_broadcasting() -> dict:
        """Demonstrates NumPy broadcasting mechanics across incompatible dimensions."""
        matrix = np.array([
            [10, 20, 30],
            [40, 50, 60],
            [70, 80, 90]
        ])
        vector = np.array([1, 2, 3])  # Shape (3,) broadcasts to (1, 3) then (3, 3)
        column_vec = np.array([[100], [200], [300]])  # Shape (3, 1)

        return {
            "matrix": matrix,
            "vector": vector,
            "row_broadcast": matrix + vector,
            "col_broadcast": matrix + column_vec,
            "outer_product": np.outer(vector, vector)
        }


class ImageTensorLab:
    def __init__(self, height: int = 256, width: int = 256):
        self.height = height
        self.width = width
        self.image_array = self.generate_synthetic_canvas()

    def generate_synthetic_canvas(self) -> np.ndarray:
        """Generates a vibrant synthetic RGB test canvas using NumPy vectorization."""
        # Create coordinate grids
        x = np.linspace(0, 1, self.width)
        y = np.linspace(0, 1, self.height)
        xx, yy = np.meshgrid(x, y)

        # Red channel: radial gradient from center
        r = np.clip(np.sqrt((xx - 0.5)**2 + (yy - 0.5)**2) * 2, 0, 1)
        r_channel = (r * 255).astype(np.uint8)

        # Green channel: horizontal sine wave
        g_channel = (np.sin(xx * 4 * np.pi) * 0.5 + 0.5) * 255
        g_channel = g_channel.astype(np.uint8)

        # Blue channel: vertical gradient
        b_channel = (yy * 255).astype(np.uint8)

        # Stack into (Height, Width, 3) RGB Tensor
        rgb_tensor = np.stack([r_channel, g_channel, b_channel], axis=-1)
        return rgb_tensor

    def to_grayscale(self, img: np.ndarray = None) -> np.ndarray:
        """Converts RGB tensor (H, W, 3) to 2D Grayscale using luminosity weights."""
        target = self.image_array if img is None else img
        weights = np.array([0.2989, 0.5870, 0.1140])
        gray = np.dot(target[..., :3], weights)
        return np.clip(gray, 0, 255).astype(np.uint8)

    def isolate_channel(self, channel_idx: int) -> np.ndarray:
        """Isolates a single color channel: 0=Red, 1=Green, 2=Blue."""
        isolated = np.zeros_like(self.image_array)
        isolated[..., channel_idx] = self.image_array[..., channel_idx]
        return isolated

    def flip_horizontal(self) -> np.ndarray:
        """Reverses columns via slice notation [:, ::-1]."""
        return self.image_array[:, ::-1, :]

    def flip_vertical(self) -> np.ndarray:
        """Reverses rows via slice notation [::-1, :]."""
        return self.image_array[::-1, :, :]

    def invert_colors(self) -> np.ndarray:
        """Inverts 8-bit color space: 255 - tensor."""
        return 255 - self.image_array

    def save_array_as_image(self, arr: np.ndarray, filename: str) -> str:
        """Saves a 2D or 3D NumPy array as a PNG image using Pillow."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, filename)
        mode = "L" if arr.ndim == 2 else "RGB"
        img = Image.fromarray(arr, mode=mode)
        img.save(full_path)
        return full_path
