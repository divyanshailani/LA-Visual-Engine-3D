import bpy
import sys
import importlib
import os

# ── 1. DIMENSIONAL BRIDGE ────────────────────────────────
path_phase2 = "/Users/divyanshailani/Desktop/project_2_3D/Phase_2 Blender"
path_phase1 = "/Users/divyanshailani/Desktop/project_2_3D/Phase_1 Logic"

if path_phase2 not in sys.path:
    sys.path.append(path_phase2)
if path_phase1 not in sys.path:
    sys.path.append(path_phase1)

# ── 2. IMPORT 3D ENGINE ──────────────────────────────────
from utils import materials, scene_builder, animator
import matrices

importlib.reload(materials)
importlib.reload(scene_builder)
importlib.reload(animator)
importlib.reload(matrices)

# ── 3. MISSION CONTROL ───────────────────────────────────
# Available presets:
# "identity" | "rotate_z_90" | "rotate_x_90" | "scale2x"
# "shear_x_along_z" | "collapse_z"

PRESET_NAME = "rotate_x_90"
FRAME_START = 1
FRAME_END   = 180   # 3 seconds at 60fps
GRID_SIZE   = 2     # Kept small to see the core clearly

print(f"\n🚀 INITIATING 3D SIMULATION: {PRESET_NAME.upper()}")

# ── 4. EXECUTION SEQUENCE ────────────────────────────────
scene_builder.clear_scene()
scene_builder.setup_world_lighting()

target_m = matrices.presets[PRESET_NAME]

# 4 materials — Red î, Cyan ĵ, Magenta k̂, Teal lattice
mat_i, mat_j, mat_k, mat_grid = materials.setup_all_materials()

# 3D Space Lattice (replaces flat 2D grid)
lattice_obj = scene_builder.build_lattice(mat_grid, size=GRID_SIZE)

# The 3 Pillars of 3D Space
i_arrow = scene_builder.build_arrow("i_hat", mat_i, tip_coord=(1.0, 0.0, 0.0))  # Red   X
j_arrow = scene_builder.build_arrow("j_hat", mat_j, tip_coord=(0.0, 1.0, 0.0))  # Cyan  Y
k_arrow = scene_builder.build_arrow("k_hat", mat_k, tip_coord=(0.0, 0.0, 1.0))  # Magenta Z

# Isometric eye
camera = scene_builder.setup_camera()

# Animate all 4 objects
animator.run_director(lattice_obj, target_m, FRAME_START, FRAME_END)
animator.run_director(i_arrow,     target_m, FRAME_START, FRAME_END)
animator.run_director(j_arrow,     target_m, FRAME_START, FRAME_END)
animator.run_director(k_arrow,     target_m, FRAME_START, FRAME_END)

bpy.context.scene.frame_end = FRAME_END + 20
print("🌌 3D SYSTEM ONLINE: Space Lattice Constructed and Keyframed.")

# ── 5. CINEMATOGRAPHER'S EXPORT ──────────────────────────
desktop_path = os.path.join(
    os.path.expanduser("~"), "Desktop", f"Project_02_3D_{PRESET_NAME}.mp4"
)
bpy.context.scene.render.filepath = desktop_path

if hasattr(bpy.context.scene.render.image_settings, 'media_type'):
    bpy.context.scene.render.image_settings.media_type = 'VIDEO'
else:
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'

bpy.context.scene.render.ffmpeg.format = 'MPEG4'
bpy.context.scene.render.ffmpeg.codec  = 'H264'
bpy.context.scene.render.resolution_x  = 1920
bpy.context.scene.render.resolution_y  = 1080
bpy.context.scene.render.fps           = 60

print(f"🎥 EXPORT READY → {desktop_path}")
print("Render → Render Animation  (Ctrl+F12)")
