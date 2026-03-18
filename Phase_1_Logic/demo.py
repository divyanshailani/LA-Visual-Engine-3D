import sys
import numpy as np

from matrices import get_preset, presets


def classify_det(det):
    if np.isclose(det, 0.0):
        return "COLLAPSE - singular transform"
    if det < 0.0:
        return "FLIP - orientation reversed"
    if np.isclose(det, 1.0):
        return "VOLUME PRESERVED"
    return "VOLUME SCALED"


def print_report(name):
    matrix = get_preset(name)
    det = float(np.linalg.det(matrix))

    print("3D TRANSFORMATION REPORT")
    print("=" * 40)
    print(f"Preset: {name}")
    print(f"Available presets: {', '.join(presets.keys())}")
    print("\nMatrix:")
    for row in matrix:
        print(f"[{row[0]:7.2f} {row[1]:7.2f} {row[2]:7.2f}]")
    print(f"\ndet(M) = {det:.4f}")
    print(f"Status: {classify_det(det)}")
    print("=" * 40)


if __name__ == "__main__":
    preset_name = sys.argv[1] if len(sys.argv) > 1 else "rotate_x_90"
    print_report(preset_name)
