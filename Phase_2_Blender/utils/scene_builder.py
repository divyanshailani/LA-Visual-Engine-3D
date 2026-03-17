import bpy
import math


def clear_scene():
    """Nukes everything and prevents memory leaks."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)
    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam)
    for ng in bpy.data.node_groups:
        if ng.name.startswith("TubeGen_"):
            bpy.data.node_groups.remove(ng)
    print("🧹 3D SCENE BUILDER: Dark Void Cleared.")


def setup_world_lighting():
    """Sets render engine, 60fps, dark void background, switches to RENDERED mode."""
    if (4, 2, 0) <= bpy.app.version < (5, 0, 0):
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    bpy.context.scene.render.fps = 60

    world = bpy.data.worlds.get("World")
    if world and world.use_nodes:
        bg_node = world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs[0].default_value = (0.005, 0.005, 0.01, 1.0)

    try:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.shading.type = 'RENDERED'
                            space.shading.use_scene_lights = True
                            space.shading.use_scene_world = True
        print("✅ Viewport → RENDERED mode activated.")
    except Exception:
        print("⚠️  Press Z → Rendered manually.")


def give_thickness(obj, thickness=0.015):
    """
    Converts 1D math lines into solid 3D tubes via Geometry Nodes.
    Compatible with Shape Key animation — unlike SKIN modifier.
    """
    mod = obj.modifiers.new(name="Neon_Tube", type='NODES')
    tree = bpy.data.node_groups.new(name=f"TubeGen_{obj.name}", type='GeometryNodeTree')
    mod.node_group = tree

    tree.interface.new_socket(name="Geometry", in_out='INPUT',  socket_type='NodeSocketGeometry')
    tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    nodes = tree.nodes
    links = tree.links

    in_node  = nodes.new('NodeGroupInput')
    out_node = nodes.new('NodeGroupOutput')
    m2c      = nodes.new('GeometryNodeMeshToCurve')
    c2m      = nodes.new('GeometryNodeCurveToMesh')
    circle   = nodes.new('GeometryNodeCurvePrimitiveCircle')
    set_mat  = nodes.new('GeometryNodeSetMaterial')

    circle.inputs['Radius'].default_value = thickness
    circle.inputs['Resolution'].default_value = 8

    if obj.data.materials:
        set_mat.inputs['Material'].default_value = obj.data.materials[0]

    links.new(in_node.outputs[0],  m2c.inputs[0])
    links.new(m2c.outputs[0],      c2m.inputs[0])
    links.new(circle.outputs[0],   c2m.inputs[1])
    links.new(c2m.outputs[0],      set_mat.inputs[0])
    links.new(set_mat.outputs[0],  out_node.inputs[0])


def build_lattice(material, size=2, step=1):
    """
    Constructs a 3D Space Lattice — cube grid of edges in X, Y, and Z.
    This is the 3D upgrade from the flat 2D grid in Project 01.
    """
    verts, edges = [], []

    # Lines parallel to X-axis
    for y in range(-size, size + 1, step):
        for z in range(-size, size + 1, step):
            v = len(verts)
            verts += [(-size, y, z), (size, y, z)]
            edges.append((v, v + 1))

    # Lines parallel to Y-axis
    for x in range(-size, size + 1, step):
        for z in range(-size, size + 1, step):
            v = len(verts)
            verts += [(x, -size, z), (x, size, z)]
            edges.append((v, v + 1))

    # Lines parallel to Z-axis (the new depth)
    for x in range(-size, size + 1, step):
        for y in range(-size, size + 1, step):
            v = len(verts)
            verts += [(x, y, -size), (x, y, size)]
            edges.append((v, v + 1))

    mesh = bpy.data.meshes.new("SpaceLattice_Mesh")
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    obj = bpy.data.objects.new("SpaceLattice", mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    give_thickness(obj, thickness=0.01)
    return obj


def build_arrow(name, color_mat, tip_coord):
    """Builds a thick neon basis vector from origin to tip in true 3D."""
    x, y, z = float(tip_coord[0]), float(tip_coord[1]), float(tip_coord[2])

    verts = [(0.0, 0.0, 0.0), (x, y, z)]
    edges = [(0, 1)]

    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(color_mat)
    give_thickness(obj, thickness=0.06)
    return obj


def setup_camera():
    """
    Isometric orthographic camera — perfect diagonal view of 3D space.
    Placed at (10, -10, 10) looking at origin with classic isometric angles.
    """
    cam_data = bpy.data.cameras.new("Main_Cam")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 10.0

    cam_obj = bpy.data.objects.new("Camera", cam_data)
    cam_obj.location = (10.0, -10.0, 10.0)
    cam_obj.rotation_euler = (math.radians(54.736), 0.0, math.radians(45.0))

    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    return cam_obj
