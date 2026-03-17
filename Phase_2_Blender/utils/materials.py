import bpy

def create_emission_material(name, color_rgba, color_strength=5.0):
    """Creates a glowing neon emission material using Blender shader nodes."""
    if name in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials[name])

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs['Color'].default_value = color_rgba
    node_emission.inputs['Strength'].default_value = color_strength
    node_emission.location = (0, 0)

    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (200, 0)

    links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])
    return mat


def setup_all_materials():
    """3D RGB neon palette — Red X, Cyan Y, Magenta Z, Teal lattice."""
    red_glow     = (1.0, 0.2, 0.2, 1.0)   # î — X-axis
    cyan_glow    = (0.0, 1.0, 0.8, 1.0)   # ĵ — Y-axis
    magenta_glow = (1.0, 0.0, 1.0, 1.0)   # k̂ — Z-axis (the new dimension)
    grid_color   = (0.0, 0.8, 1.0, 1.0)   # Space Lattice

    mat_i_hat = create_emission_material("Mat_i_hat", red_glow,     color_strength=15.0)
    mat_j_hat = create_emission_material("Mat_j_hat", cyan_glow,    color_strength=15.0)
    mat_k_hat = create_emission_material("Mat_k_hat", magenta_glow, color_strength=15.0)
    mat_grid  = create_emission_material("Mat_Grid",  grid_color,   color_strength=8.0)

    print("🎨 3D PAINT SHOP: RGB palette built — Red · Cyan · Magenta · Teal")
    return mat_i_hat, mat_j_hat, mat_k_hat, mat_grid
