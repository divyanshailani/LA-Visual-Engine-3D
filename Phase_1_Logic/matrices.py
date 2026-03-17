import numpy as np

# ─────────────────────────────────────────────────────────
# All 3x3 Transformation Matrices — True 3D
# Project 02 · Phase 1 Logic · The Architect
# Divyansh Ailani · 2026
# ─────────────────────────────────────────────────────────

# 1. Identity — X, Y, and Z axes untouched
identity = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
], dtype=float)

# 2. Rotate 90° around Z-axis (spinning top)
rotate_z_90 = np.array([
    [0.0, -1.0, 0.0],
    [1.0,  0.0, 0.0],
    [0.0,  0.0, 1.0]
], dtype=float)

# 3. Rotate 90° around X-axis (barrel roll)
rotate_x_90 = np.array([
    [1.0,  0.0,  0.0],
    [0.0,  0.0, -1.0],
    [0.0,  1.0,  0.0]
], dtype=float)

# 4. Uniform Scale 2x (expand the universe in all 3 directions)
scale2x = np.array([
    [2.0, 0.0, 0.0],
    [0.0, 2.0, 0.0],
    [0.0, 0.0, 2.0]
], dtype=float)

# 5. 3D Shear — push the top of the cube sideways along X
shear_x_along_z = np.array([
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
], dtype=float)

# 6. Dimensional Collapse — crush 3D space into a flat 2D plane
# det = 0 — information is destroyed
collapse_z = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0]
], dtype=float)

# ─────────────────────────────────────────────────────────
# Presets Dictionary
# ─────────────────────────────────────────────────────────
presets = {
    "identity":       identity,
    "rotate_z_90":    rotate_z_90,
    "rotate_x_90":    rotate_x_90,
    "scale2x":        scale2x,
    "shear_x_along_z": shear_x_along_z,
    "collapse_z":     collapse_z,
}

def get_preset(name):
    """Returns the 3x3 transformation matrix for a given preset name."""
    if name not in presets:
        raise ValueError(f"Unknown preset '{name}'. Available: {list(presets.keys())}")
    return presets[name]
