# 烘焙管线共享库（SK-10 的管线本体）
# 场景脚本只负责建模：import bake_lib as L → L.reset() → 建模 → L.finish(out_dir, name)
import bpy
import math
import os

BAKE_SIZE = 2048
SAMPLES = 128

PARTS = []
_scene = None


def reset():
    """清空场景，返回 scene"""
    global PARTS, _scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    PARTS = []
    _scene = bpy.context.scene
    return _scene


def srgb(hexcode):
    h = hexcode.lstrip('#')
    return tuple((int(h[i:i + 2], 16) / 255.0) ** 2.2 for i in (0, 2, 4))


def make_mat(name, color, rough=0.75, emit=None, emit_strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*srgb(color), 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    if emit:
        bsdf.inputs['Emission Color'].default_value = (*srgb(emit), 1.0)
        bsdf.inputs['Emission Strength'].default_value = emit_strength
    return m


def _register(obj, mat):
    obj.data.materials.append(mat)
    PARTS.append(obj)
    return obj


def box(name, size, loc, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    return _register(o, mat)


def cyl(name, r, depth, loc, mat, verts=20, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    return _register(o, mat)


def sphere(name, r, loc, mat, seg=18, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(seg // 2, 6), radius=r, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    return _register(o, mat)


def cone(name, r, depth, loc, mat, verts=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    return _register(o, mat)


def room_shell(floor_mat, wall_back_mat, wall_side_mat, skirt_mat):
    """标准房间壳：12x12 地台 + 后墙(y=5.85) + 左墙(x=-5.85) + 踢脚线。
    与灰盒布局对齐：相机从 +y 侧看进来（three.js 的 +z）。"""
    box('floor', (12, 12, 0.24), (0, 0, -0.12), floor_mat)
    box('wall_back', (12, 0.3, 4.2), (0, 5.85, 2.1), wall_back_mat)
    box('wall_left', (0.3, 12, 4.2), (-5.85, 0, 2.1), wall_side_mat)
    box('skirting_back', (12, 0.34, 0.18), (0, 5.85, 0.09), skirt_mat)
    box('skirting_left', (0.34, 12, 0.18), (-5.85, 0, 0.09), skirt_mat)


def window_on_left(frame_mat, glow_mat, y=-1.2):
    """左墙窗户（发光面 = 主光源之一）"""
    box('window_frame', (0.2, 2.8, 2.2), (-5.78, y, 2.5), frame_mat)
    box('window_glow', (0.1, 2.4, 1.8), (-5.7, y, 2.5), glow_mat)
    box('window_bar_v', (0.24, 0.08, 1.8), (-5.68, y, 2.5), frame_mat)
    box('window_bar_h', (0.24, 2.4, 0.08), (-5.68, y, 2.5), frame_mat)


def lights(sun_color='#ffe0b8', sun_energy=5.5, fill_color='#bcd0ff', fill_energy=460,
           world_color='#2a3040', world_strength=0.85, extra_points=()):
    """M2 定稿的灯光配方；extra_points = [(loc, color, energy), ...] 局部补光"""
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN'))
    sun.data.energy = sun_energy
    sun.data.color = srgb(sun_color)
    sun.data.angle = math.radians(12)
    sun.rotation_euler = (math.radians(58), math.radians(-18), math.radians(-105))
    _scene.collection.objects.link(sun)

    fill = bpy.data.objects.new('fill', bpy.data.lights.new('fill', 'AREA'))
    fill.data.energy = fill_energy
    fill.data.size = 8
    fill.data.color = srgb(fill_color)
    fill.location = (2.0, -1.0, 5.4)
    _scene.collection.objects.link(fill)

    for i, (loc, color, energy) in enumerate(extra_points):
        p = bpy.data.objects.new(f'point{i}', bpy.data.lights.new(f'point{i}', 'POINT'))
        p.data.energy = energy
        p.data.color = srgb(color)
        p.data.shadow_soft_size = 0.6
        p.location = loc
        _scene.collection.objects.link(p)

    world = bpy.data.worlds.new('world')
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (*srgb(world_color), 1.0)
    bg.inputs['Strength'].default_value = world_strength
    _scene.world = world


def finish(out_dir, name, bake_size=BAKE_SIZE, samples=SAMPLES):
    """合并→UV→Cycles 烘焙→换烘焙材质→导出 GLB"""
    os.makedirs(out_dir, exist_ok=True)

    bpy.ops.object.select_all(action='DESELECT')
    for o in PARTS:
        o.select_set(True)
    bpy.context.view_layer.objects.active = PARTS[0]
    bpy.ops.object.join()
    room = bpy.context.object
    room.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(island_margin=0.015)
    bpy.ops.object.mode_set(mode='OBJECT')

    _scene.render.engine = 'CYCLES'
    _scene.cycles.samples = samples
    _scene.cycles.use_denoising = True
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for dt in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
            try:
                prefs.compute_device_type = dt
                prefs.get_devices()
                if [d for d in prefs.devices if d.type != 'CPU']:
                    for d in prefs.devices:
                        d.use = True
                    _scene.cycles.device = 'GPU'
                    print(f'BAKE: using GPU via {dt}')
                    break
            except Exception:
                continue
    except Exception as e:
        print('BAKE: GPU probe failed, CPU fallback:', e)

    bake_img = bpy.data.images.new('bake', bake_size, bake_size, alpha=False)
    for slot in room.material_slots:
        nt = slot.material.node_tree
        node = nt.nodes.new('ShaderNodeTexImage')
        node.image = bake_img
        nt.nodes.active = node

    bpy.ops.object.select_all(action='DESELECT')
    room.select_set(True)
    bpy.context.view_layer.objects.active = room
    print('BAKE: baking COMBINED...')
    bpy.ops.object.bake(type='COMBINED', margin=8, use_clear=True)

    png = os.path.join(out_dir, f'{name}_bake.png')
    bake_img.filepath_raw = png
    bake_img.file_format = 'PNG'
    bake_img.save()
    print('BAKE: saved', png)

    baked_mat = bpy.data.materials.new('baked')
    baked_mat.use_nodes = True
    bsdf = baked_mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Roughness'].default_value = 1.0
    tex = baked_mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image = bake_img
    baked_mat.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    room.data.materials.clear()
    room.data.materials.append(baked_mat)

    glb = os.path.join(out_dir, f'{name}-raw.glb')
    bpy.ops.object.select_all(action='DESELECT')
    room.select_set(True)
    bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', use_selection=True,
                              export_apply=True, export_yup=True)
    print('BAKE: exported', glb)
    print('BAKE: DONE')
