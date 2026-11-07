"""Render a 3D blockout of a card's object in Blender, for the image model to restyle.

    blender -b --factory-startup --python scripts/blockout.py -- model.py render.png [soft | check]

"soft" renders a smoother, stylized look: no clear coat, broad highlights, beveled edges in the shading, a larger
light and more fill (experiments/trial2.py). "check" renders nothing and only prints the construction check.

Every run prints a construction check as a line starting with LOOSE: each group of touching hero parts that touches
nothing holding it. With a floor, ledge or setting, every group must reach it; a floating object must be one group.
Two parts touch when their surfaces cross or come within 1% of the hero's height.

A model file sets SCENE and defines build(k), where k holds the helpers below. Parts are the hero unless made
with setting=True. The hero is framed to the real cards' median box, about 80% by 75% of the card.
SCENE: backdrop as hex, azimuth (0 is front-on, positive puts the camera to the right), elevation, lens in mm
and light "left" or "right".
"""

import json
import math
import sys
import types

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Euler, Vector
from mathutils.bvhtree import BVHTree

SIZE = (860, 960)
BOX = (0.80, 0.75)
FINISHES = {"satin": dict(rough=0.45), "matte": dict(rough=0.8), "gloss": dict(rough=0.25, coat=0.6),
            "metal": dict(rough=0.3, metal=1.0), "glass": dict(rough=0.05, glass=1.0), "glow": dict(rough=0.5, glow=4.0)}
SOFT = {"satin": dict(rough=0.6), "matte": dict(rough=0.85), "gloss": dict(rough=0.45),
        "metal": dict(rough=0.5, metal=1.0)}
ROOT = None
LOOK = "plain"


def linear(hex_color):
    rgb = [int(hex_color.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb] + [1.0]


def mat(color, finish="satin"):
    name = f"{color}_{finish}"
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    spec = {**FINISHES[finish], **(SOFT.get(finish, {}) if LOOK == "soft" else {})}
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    shader = m.node_tree.nodes["Principled BSDF"]
    shader.inputs["Base Color"].default_value = linear(color)
    shader.inputs["Roughness"].default_value = spec["rough"]
    shader.inputs["Metallic"].default_value = spec.get("metal", 0.0)
    shader.inputs["Coat Weight"].default_value = spec.get("coat", 0.0)
    shader.inputs["Transmission Weight"].default_value = spec.get("glass", 0.0)
    if "glow" in spec:
        shader.inputs["Emission Color"].default_value = linear(color)
        shader.inputs["Emission Strength"].default_value = spec["glow"]
    if LOOK == "soft" and finish not in ("glow", "glass"):
        bevel = m.node_tree.nodes.new("ShaderNodeBevel")
        bevel.inputs["Radius"].default_value, bevel.samples = 0.02, 8
        m.node_tree.links.new(bevel.outputs["Normal"], shader.inputs["Normal"])
    return m


def _finish(obj, at, rot, m, bevel, setting):
    obj.location = at
    obj.rotation_euler = Euler([math.radians(a) for a in rot])
    if m:
        obj.data.materials.append(m)
    if obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
    if bevel and obj.type == "MESH":
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width, mod.segments, mod.limit_method, mod.harden_normals = bevel, 3, "ANGLE", True
    if not setting:
        obj.parent = ROOT
    return obj


def box(size, at=(0, 0, 0), rot=(0, 0, 0), m=None, bevel=0.01, setting=False):
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.object
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    return _finish(obj, at, rot, m, bevel, setting)


def cyl(r, h, at=(0, 0, 0), rot=(0, 0, 0), m=None, bevel=0.005, setting=False, verts=64):
    """A cylinder along its local z."""
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=verts)
    return _finish(bpy.context.object, at, rot, m, bevel, setting)


def cone(r1, r2, h, at=(0, 0, 0), rot=(0, 0, 0), m=None, bevel=0.005, setting=False, verts=64):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=h, vertices=verts)
    return _finish(bpy.context.object, at, rot, m, bevel, setting)


def sphere(r, at=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0), m=None, setting=False):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=48, ring_count=24)
    obj = bpy.context.object
    obj.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    return _finish(obj, at, rot, m, 0, setting)


def torus(big, small, at=(0, 0, 0), rot=(0, 0, 0), m=None, setting=False):
    """A ring in its local xy plane."""
    bpy.ops.mesh.primitive_torus_add(major_radius=big, minor_radius=small, major_segments=64, minor_segments=24)
    return _finish(bpy.context.object, at, rot, m, 0, setting)


def tube(points, r, m=None, curved=False, setting=False):
    """A round tube through the points: straight segments, or one smooth curve."""
    curve = bpy.data.curves.new("tube", "CURVE")
    curve.dimensions, curve.bevel_depth, curve.bevel_resolution, curve.use_fill_caps = "3D", r, 6, True
    spline = curve.splines.new("BEZIER" if curved else "POLY")
    if curved:
        spline.bezier_points.add(len(points) - 1)
        for point, co in zip(spline.bezier_points, points):
            point.co, point.handle_left_type, point.handle_right_type = co, "AUTO", "AUTO"
    else:
        spline.points.add(len(points) - 1)
        for point, co in zip(spline.points, points):
            point.co = (*co, 1)
    obj = bpy.data.objects.new("tube", curve)
    bpy.context.collection.objects.link(obj)
    return _finish(obj, (0, 0, 0), (0, 0, 0), m, 0, setting)


def lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=None, setting=False, verts=64):
    """A solid of revolution about the local z: profile is (radius, z) from bottom to top. A radius of 0 closes the end."""
    points = [(r * math.cos(2 * math.pi * i / verts), r * math.sin(2 * math.pi * i / verts), z)
              for r, z in profile for i in range(verts)]
    faces = [(a * verts + i, a * verts + (i + 1) % verts, (a + 1) * verts + (i + 1) % verts, (a + 1) * verts + i)
             for a in range(len(profile) - 1) for i in range(verts)]
    for end in (0, len(profile) - 1):
        if profile[end][0] > 0:
            ring = [end * verts + i for i in range(verts)]
            faces.append(tuple(ring if end else reversed(ring)))
    mesh = bpy.data.meshes.new("lathe")
    mesh.from_pydata(points, [], faces)
    obj = bpy.data.objects.new("lathe", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.remove_doubles(threshold=1e-5)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)
    return _finish(obj, at, rot, m, 0, setting)


def blob(balls, m=None, setting=False):
    """One soft organic form from merged balls: each is (x, y, z, radius) or (x, y, z, radius, (sx, sy, sz)).

    A lone ball shows its radius. Balls that overlap or nearly touch melt together with a soft neck."""
    name = f"blob{len(bpy.data.objects)}"  # metaballs that share a base name melt together
    data = bpy.data.metaballs.new(name)
    data.resolution = data.render_resolution = max(0.003, min(ball[3] for ball in balls) / 6)
    for ball in balls:
        element = data.elements.new(type="ELLIPSOID" if len(ball) > 4 else "BALL")
        element.co, element.radius = ball[:3], ball[3] / 0.575  # the surface sits at 0.575 of a metaball's radius
        if len(ball) > 4:
            element.size_x, element.size_y, element.size_z = ball[4]
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.update()
    for other in bpy.context.selected_objects:
        other.select_set(False)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target="MESH")
    obj = bpy.context.object
    obj.select_set(False)
    return _finish(obj, (0, 0, 0), (0, 0, 0), m, 0, setting)


def warp(part, fn):
    """Move every vertex of a mesh part through fn((x, y, z)) -> (x, y, z), in the part's own coordinates."""
    for vertex in part.data.vertices:
        vertex.co = fn(tuple(vertex.co))
    part.data.update()
    return part


def floor(color, finish="matte", size=40, z=0.0):
    return box((size, size, 0.02), at=(0, 0, z - 0.01), m=mat(color, finish), bevel=0, setting=True)


def turn(x=0, y=0, z=0):
    """Rotate the whole hero, in degrees."""
    ROOT.rotation_euler = Euler([math.radians(a) for a in (x, y, z)])


def unframed(*parts):
    """Hero parts left out of the framing, such as a truss that may run off the card."""
    for part in parts:
        part["unframed"] = True
    return parts


def hero_points():
    graph = bpy.context.evaluated_depsgraph_get()
    points = []
    for obj in bpy.context.scene.objects:
        if obj.type in {"MESH", "CURVE"} and obj.parent == ROOT and not obj.get("unframed"):
            evaluated = obj.evaluated_get(graph)
            mesh = evaluated.to_mesh()
            points += [evaluated.matrix_world @ v.co for v in mesh.vertices]
            evaluated.to_mesh_clear()
    return points


HELPERS = {"Cube": "box", "Cylinder": "cyl", "Cone": "cone", "Sphere": "sphere", "Torus": "torus", "tube": "tube",
           "lathe": "lathe", "blob": "blob"}  # Blender's object names, as the model file's helpers


def surfaces():
    """Every part as world-space vertices, a BVH tree and a bounding box."""
    graph = bpy.context.evaluated_depsgraph_get()
    parts = []
    for obj in bpy.context.scene.objects:
        if obj.type not in {"MESH", "CURVE"}:
            continue
        evaluated = obj.evaluated_get(graph)
        mesh = evaluated.to_mesh()
        verts = [evaluated.matrix_world @ v.co for v in mesh.vertices]
        polygons = [tuple(p.vertices) for p in mesh.polygons]
        evaluated.to_mesh_clear()
        if not verts or not polygons:
            continue
        low = Vector([min(v[i] for v in verts) for i in range(3)])
        high = Vector([max(v[i] for v in verts) for i in range(3)])
        parts.append({"obj": obj, "hero": obj.parent == ROOT, "verts": verts, "tree": BVHTree.FromPolygons(verts, polygons),
                      "low": low, "high": high})
    return parts


def touching(a, b, tolerance):
    if any(a["low"][i] - tolerance > b["high"][i] or b["low"][i] - tolerance > a["high"][i] for i in range(3)):
        return False
    if a["tree"].overlap(b["tree"]):
        return True
    for first, second in ((a, b), (b, a)):
        step = max(1, len(first["verts"]) // 600)
        for vertex in first["verts"][::step]:
            hit = second["tree"].find_nearest(vertex, tolerance)
            if hit[0] is not None:
                return True
    return False


def loose_parts():
    """Groups of hero parts that touch nothing holding them, as described above."""
    parts = surfaces()
    hero = [p for p in parts if p["hero"]]
    if not hero:
        return []
    height = max(p["high"].z for p in hero) - min(p["low"].z for p in hero)
    tolerance = max(height, 0.01) * 0.01
    group = list(range(len(parts)))

    def root(i):
        while group[i] != i:
            group[i] = group[group[i]]
            i = group[i]
        return i

    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            if (parts[i]["hero"] or parts[j]["hero"]) and root(i) != root(j) and touching(parts[i], parts[j], tolerance):
                group[root(i)] = root(j)
    held = {root(i) for i, p in enumerate(parts) if not p["hero"]}
    if not held:  # a floating object: everything must hang together with its largest group
        sizes = {}
        for i, p in enumerate(parts):
            sizes[root(i)] = sizes.get(root(i), 0) + len(p["verts"])
        held = {max(sizes, key=sizes.get)}
    groups = {}
    for i, p in enumerate(parts):
        if p["hero"] and root(i) not in held:
            groups.setdefault(root(i), []).append(p)
    loose = []
    for members in groups.values():
        low = Vector([min(p["low"][i] for p in members) for i in range(3)])
        high = Vector([max(p["high"][i] for p in members) for i in range(3)])
        kinds = sorted({HELPERS.get(p["obj"].name.split(".")[0].rstrip("0123456789"), "part") for p in members})
        loose.append({"parts": len(members), "kinds": kinds, "at": [round(c, 2) for c in (low + high) / 2],
                      "size": [round(c, 2) for c in high - low]})
    return loose


def frame(camera, scene, azimuth, elevation, points):
    center = sum(points, Vector()) / len(points)
    a, e = math.radians(azimuth), math.radians(elevation)
    direction = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    camera.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()

    def fit(distance):
        camera.location = center + direction * distance
        bpy.context.view_layer.update()
        projected = [world_to_camera_view(scene, camera, p) for p in points]
        xs, ys = [p.x for p in projected], [p.y for p in projected]
        return xs, ys

    low, high = 0.01, 1000.0
    for _ in range(60):
        middle = (low * high) ** 0.5
        xs, ys = fit(middle)
        size = max((max(xs) - min(xs)) / BOX[0], (max(ys) - min(ys)) / BOX[1])
        low, high = (middle, high) if size > 1 else (low, middle)
    longest = max(SIZE)
    for _ in range(3):
        xs, ys = fit(high)
        camera.data.shift_x += ((max(xs) + min(xs)) / 2 - 0.5) * SIZE[0] / longest
        camera.data.shift_y += ((max(ys) + min(ys)) / 2 - 0.5) * SIZE[1] / longest
    return center, high


def stage(scene, spec, center, distance):
    """One soft light from one side and above, a soft fill, and a flat backdrop seen only by the camera."""
    side = -1 if spec.get("light", "left") == "left" else 1
    a = math.radians(spec.get("azimuth", 30) + side * 70)
    direction = Vector((math.sin(a) * 0.6, -math.cos(a) * 0.6, 0.8)).normalized()
    light = bpy.data.lights.new("key", "AREA")
    soft = LOOK == "soft"
    light.size, light.energy = distance * (1.6 if soft else 0.8), 60 * distance ** 2
    key = bpy.data.objects.new("key", light)
    scene.collection.objects.link(key)
    key.location = center + direction * distance * 1.2
    key.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()

    world = bpy.data.worlds.new("world")
    scene.world = world
    world.use_nodes = True
    nodes, links = world.node_tree.nodes, world.node_tree.links
    out = nodes["World Output"]
    fill, seen = nodes.new("ShaderNodeBackground"), nodes.new("ShaderNodeBackground")
    fill.inputs["Color"].default_value = [0.5 + 0.5 * c for c in linear(spec["backdrop"])[:3]] + [1]
    fill.inputs["Strength"].default_value = 0.6 if soft else 0.3
    seen.inputs["Color"].default_value = linear(spec["backdrop"])
    path, mix = nodes.new("ShaderNodeLightPath"), nodes.new("ShaderNodeMixShader")
    links.new(path.outputs["Is Camera Ray"], mix.inputs[0])
    links.new(fill.outputs[0], mix.inputs[1])
    links.new(seen.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], out.inputs["Surface"])


def render(model, out):
    global ROOT
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    ROOT = bpy.data.objects.new("hero", None)
    scene.collection.objects.link(ROOT)
    namespace = {}
    exec(compile(open(model, encoding="utf-8").read(), model, "exec"), namespace)
    spec = namespace["SCENE"]
    helpers = types.SimpleNamespace(mat=mat, box=box, cyl=cyl, cone=cone, sphere=sphere, torus=torus, tube=tube,
                                    lathe=lathe, blob=blob, warp=warp, floor=floor, turn=turn, unframed=unframed)
    namespace["build"](helpers)
    bpy.context.view_layer.update()
    print("LOOSE: " + json.dumps(loose_parts()), flush=True)
    if LOOK == "check":
        return

    scene.render.resolution_x, scene.render.resolution_y = SIZE
    camera = bpy.data.objects.new("camera", bpy.data.cameras.new("camera"))
    camera.data.lens = spec.get("lens", 50)
    camera.data.sensor_fit = "AUTO"
    scene.collection.objects.link(camera)
    scene.camera = camera
    center, distance = frame(camera, scene, spec.get("azimuth", 30), spec.get("elevation", 12), hero_points())
    camera.data.clip_end = distance * 50
    stage(scene, spec, center, distance)

    # The CPU: a render takes about 10 s, and Cycles on HIP faulted on an integrated GPU and once hung the main GPU
    # under parallel runs (2026-11-07), resetting it and killing every GPU process
    scene.render.engine, scene.cycles.device, scene.cycles.samples = "CYCLES", "CPU", 128
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = "Standard"
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    model_file, out_file, *rest = sys.argv[sys.argv.index("--") + 1:]
    LOOK = rest[0] if rest else "plain"
    render(model_file, out_file)
