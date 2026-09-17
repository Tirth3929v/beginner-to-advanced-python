"""
Day 76: Computation with NumPy & N-Dim Arrays
Interactive Linear Algebra & Image Tensor Studio
"""

import sys
import os
import numpy as np

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from numpy_lab import MatrixLab, ImageTensorLab


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 76: COMPUTATION WITH NUMPY & N-DIMENSIONAL TENSOR ARRAYS")
    print(" 📚 Phase 4: Data Science & Analytics | 100 Days of Code Python Bootcamp")
    print("=" * 76)
    print(" Core NumPy Engineering Concepts:")
    print("  • Tensor Shapes, Dimensions & Slicing: Indexing [H, W, C]")
    print("  • Matrix Broadcasting: Automatic dimension expansion across axis alignments")
    print("  • Linear Algebra: Matrix inversion, eigenvalues, and linear equation solvers")
    print("  • Image Tensor Manipulation: Grayscale transforms, channel isolation, reflections")
    print("=" * 76 + "\n")


def display_broadcasting():
    res = MatrixLab.demonstrate_broadcasting()
    print("\n📐 NUMPY BROADCASTING DEMONSTRATION")
    print("=" * 65)
    print("Original 3x3 Matrix:")
    print(res["matrix"])
    print("\n1D Vector (Shape: (3,)):")
    print(res["vector"])
    print("\n1. Matrix + Vector (Row-wise Broadcast):")
    print(res["row_broadcast"])
    print("\n2. Matrix + Column Vector (Column-wise Broadcast):")
    print(res["col_broadcast"])
    print("\n3. Outer Product (Vector ⊗ Vector):")
    print(res["outer_product"])
    print("=" * 65 + "\n")


def display_linear_algebra():
    print("\n🧮 LINEAR ALGEBRA & EQUATION SYSTEM SOLVER")
    print("=" * 65)
    print("System of Equations:")
    print("  2x + 3y +  z = 1")
    print("  4x +  y - 2z = 2")
    print("  3x + 2y + 3z = 3")

    A = np.array([
        [2, 3, 1],
        [4, 1, -2],
        [3, 2, 3]
    ], dtype=float)
    b = np.array([1, 2, 3], dtype=float)

    solution = MatrixLab.linear_system_solver(A, b)
    props = MatrixLab.matrix_properties(A)

    print(f"\nSolution Vector (x, y, z):")
    print(f"  x = {solution[0]:.4f}")
    print(f"  y = {solution[1]:.4f}")
    print(f"  z = {solution[2]:.4f}")

    print(f"\nMatrix Properties:")
    print(f"  • Determinant: det(A) = {props['determinant']:.4f}")
    print(f"  • Matrix Rank: {props['rank']}")
    print(f"  • Eigenvalues: {np.round(props['eigenvalues'], 4)}")
    print("=" * 65 + "\n")


def run_image_tensor_studio():
    print("\n🎨 IMAGE TENSOR TRANSFORMATION LAB")
    print("=" * 65)
    lab = ImageTensorLab(256, 256)
    print(f"Synthesized RGB image tensor of shape: {lab.image_array.shape}")
    print(f"Data type: {lab.image_array.dtype} | Min: {lab.image_array.min()}, Max: {lab.image_array.max()}")

    # Export transformations
    orig_p = lab.save_array_as_image(lab.image_array, "synthetic_original.png")
    gray_p = lab.save_array_as_image(lab.to_grayscale(), "synthetic_grayscale.png")
    red_p = lab.save_array_as_image(lab.isolate_channel(0), "synthetic_channel_red.png")
    flip_p = lab.save_array_as_image(lab.flip_horizontal(), "synthetic_flipped.png")
    inv_p = lab.save_array_as_image(lab.invert_colors(), "synthetic_inverted.png")

    print("\n✅ Successfully generated and saved 5 transformed image tensors:")
    print(f"  1. Original Canvas:     {os.path.basename(orig_p)}")
    print(f"  2. Grayscale (L):       {os.path.basename(gray_p)}")
    print(f"  3. Isolated Red Channel: {os.path.basename(red_p)}")
    print(f"  4. Horizontal Mirror:   {os.path.basename(flip_p)}")
    print(f"  5. Inverted Colors:     {os.path.basename(inv_p)}")
    print("=" * 65 + "\n")


def run_automated_tests():
    """Verifies matrix math, broadcasting, and image processing tensor transformations."""
    print("\n🔍 Running Day 76 Automated NumPy & Tensor Test Suite...")
    print("-" * 70)
    
    # 1. Broadcasting test
    b_res = MatrixLab.demonstrate_broadcasting()
    assert b_res["row_broadcast"][0, 0] == 11
    assert b_res["row_broadcast"][2, 2] == 93
    print(" [PASS] 1. Matrix broadcasting math verified.")

    # 2. Linear algebra test
    A = np.array([[3, 1], [1, 2]], dtype=float)
    b = np.array([9, 8], dtype=float)
    x = MatrixLab.linear_system_solver(A, b)
    assert np.allclose(A @ x, b)
    print(" [PASS] 2. Linear system solver Ax = b verified.")

    # 3. Determinant & inverse test
    props = MatrixLab.matrix_properties(A)
    assert abs(props["determinant"] - 5.0) < 1e-6
    assert np.allclose(A @ props["inverse"], np.eye(2))
    print(" [PASS] 3. Matrix determinant & identity inversion verified.")

    # 4. Image Tensor generation
    lab = ImageTensorLab(100, 100)
    assert lab.image_array.shape == (100, 100, 3)
    assert lab.image_array.dtype == np.uint8
    print(" [PASS] 4. RGB 3D tensor shape (100, 100, 3) & uint8 encoding verified.")

    # 5. Grayscale & channel isolation
    gray = lab.to_grayscale()
    assert gray.shape == (100, 100)
    red_iso = lab.isolate_channel(0)
    assert red_iso[..., 1].sum() == 0 and red_iso[..., 2].sum() == 0
    print(" [PASS] 5. Luminosity grayscale dot-product and color channel zeroing verified.")

    # 6. Image export pipeline
    out_file = lab.save_array_as_image(gray, "test_gray.png")
    assert os.path.exists(out_file) and os.path.getsize(out_file) > 100
    try:
        os.remove(out_file)
    except Exception:
        pass
    print(" [PASS] 6. Pillow image export from NumPy array verified.")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! NumPy Tensor Lab fully operational.\n")


def main():
    banner()
    while True:
        print("Select a laboratory module:")
        print("  1) 📐 Matrix Broadcasting Rules & Mechanics")
        print("  2) 🧮 Linear Algebra & Equation System Solver (Ax = b)")
        print("  3) 🎨 Image Tensor Manipulation (Grayscale, Slicing & Channel Isolation)")
        print("  4) ✅ Run Automated Verification Suite (6 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            display_broadcasting()
        elif choice == "2":
            display_linear_algebra()
        elif choice == "3":
            run_image_tensor_studio()
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Happy Computing with NumPy! 🧮\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 76 gracefully... Goodbye!\n")
