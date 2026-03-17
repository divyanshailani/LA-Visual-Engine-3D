import bpy
import numpy as np


def animate_mesh_transformation(obj, target_matrix, frame_start=1, frame_end=180):
    """
    Uses Blender Shape Keys for crash-proof 3D matrix lerp.

    Basis key  = identity (untransformed 3D positions)
    Transformed key = 3x3 matrix applied to every vertex
    Shape key value animates 0.0 → 1.0 = mathematically perfect lerp.
    """
    M = np.array(target_matrix)

    # Basis Shape Key (identity state)
    if not obj.data.shape_keys:
        obj.shape_key_add(name="Basis")

    # Target Shape Key (transformed state)
    sk_target = obj.shape_key_add(name="Transformed")

    # 3D upgrade: extract and transform X, Y, AND Z
    for i, v in enumerate(obj.data.vertices):
        orig_co = np.array([v.co.x, v.co.y, v.co.z])
        new_co  = M @ orig_co                           # 3x3 Matrix @ 3D vector

        sk_target.data[i].co.x = new_co[0]
        sk_target.data[i].co.y = new_co[1]
        sk_target.data[i].co.z = new_co[2]             # Z-axis animated!

    # Animate value 0.0 → 1.0
    sk_target.value = 0.0
    sk_target.keyframe_insert(data_path="value", frame=frame_start)
    sk_target.value = 1.0
    sk_target.keyframe_insert(data_path="value", frame=frame_end)


def set_cinematic_interpolation(obj):
    """
    Smooth Bezier interpolation on Shape Key animation.
    Handles Blender 4.4+ Action Slots and Blender 4.3 classic systems.
    """
    if not obj.data.shape_keys or not obj.data.shape_keys.animation_data:
        return

    action = obj.data.shape_keys.animation_data.action
    if not action:
        return

    # Blender 4.4+ (including 5.0) — Action Slots system
    if hasattr(action, 'layers') and action.layers:
        try:
            for layer in action.layers:
                for strip in layer.strips:
                    if hasattr(strip, 'fcurves'):
                        for fcurve in strip.fcurves:
                            for kp in fcurve.keyframe_points:
                                kp.interpolation = 'BEZIER'
        except Exception:
            pass
    # Blender 4.3 and earlier
    elif hasattr(action, 'fcurves'):
        for fcurve in action.fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'BEZIER'


def run_director(obj, target_matrix, frame_start=1, frame_end=180):
    """Master switch — animates and smooths in one call."""
    animate_mesh_transformation(obj, target_matrix, frame_start, frame_end)
    set_cinematic_interpolation(obj)
    print(f"🎬 ANIMATOR: 3D Shape Key locked for {obj.name} ({frame_start} → {frame_end})")
