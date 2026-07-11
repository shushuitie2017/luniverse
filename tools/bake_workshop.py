# Blender 4.5 headless：建模 + Cycles 烘焙「蓝猫工坊」房间 → GLB
# 用法: blender -b -P tools/bake_workshop.py -- <输出目录>
# 坐标约定: Blender Z-up，y+ = three.js 的 -z（glTF 导出自动转 Y-up）
# 房间对齐灰盒大厅: 地台 12x12，后墙 y=5.85，左墙 x=-5.85，相机从 +y 侧看进来
import bpy
import math
import sys
import os

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT_DIR = os.path.abspath(argv[0] if argv else '.')
os.makedirs(OUT_DIR, exist_ok=True)

BAKE_SIZE = 2048
SAMPLES = 128

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def srgb(hexcode):
    """sRGB hex → Blender 线性 RGB"""
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


PARTS = []


def register(obj, mat):
    obj.data.materials.append(mat)
    PARTS.append(obj)
    return obj


def box(name, size, loc, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    return register(o, mat)


def cyl(name, r, depth, loc, mat, verts=20, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    return register(o, mat)


def sphere(name, r, loc, mat, seg=18, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    return register(o, mat)


def cone(name, r, depth, loc, mat, verts=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    return register(o, mat)


# ── 材质 ────────────────────────────────────────────────
wood_floor = make_mat('wood_floor', '#8f6f4e', 0.65)
wood_dark = make_mat('wood_dark', '#5f4633', 0.6)
wall_navy = make_mat('wall_navy', '#39414e', 0.9)
wall_side = make_mat('wall_side', '#333a46', 0.9)
rug_red = make_mat('rug_red', '#b8432f', 0.95)
cat_blue = make_mat('cat_blue', '#3d6db5', 0.55)
cat_belly = make_mat('cat_belly', '#dfe6ee', 0.6)
metal_dark = make_mat('metal_dark', '#23262e', 0.4)
screen_teal = make_mat('screen_teal', '#0d1418', 0.3, emit='#3fa8a0', emit_strength=4.0)
bulb_warm = make_mat('bulb_warm', '#ffd9a0', 0.3, emit='#ffd9a0', emit_strength=10.0)
window_lit = make_mat('window_lit', '#fff4e0', 0.3, emit='#ffe9c4', emit_strength=5.0)
plant_green = make_mat('plant_green', '#4d8a52', 0.8)
pot_clay = make_mat('pot_clay', '#a06a45', 0.85)
box_amber = make_mat('box_amber', '#e8a33d', 0.8)
box_teal = make_mat('box_teal', '#3fa8a0', 0.8)
paper = make_mat('paper', '#d8d3c8', 0.9)

# ── 房间壳 ──────────────────────────────────────────────
box('floor', (12, 12, 0.24), (0, 0, -0.12), wood_floor)
box('wall_back', (12, 0.3, 4.2), (0, 5.85, 2.1), wall_navy)
box('wall_left', (0.3, 12, 4.2), (-5.85, 0, 2.1), wall_side)
box('skirting_back', (12, 0.34, 0.18), (0, 5.85, 0.09), wood_dark)
box('skirting_left', (0.34, 12, 0.18), (-5.85, 0, 0.09), wood_dark)

# 左墙窗户（发光面 = 主光源之一）
box('window_frame', (0.2, 2.8, 2.2), (-5.78, -1.2, 2.5), wood_dark)
box('window_glow', (0.1, 2.4, 1.8), (-5.7, -1.2, 2.5), window_lit)
box('window_bar_v', (0.24, 0.08, 1.8), (-5.68, -1.2, 2.5), wood_dark)
box('window_bar_h', (0.24, 2.4, 0.08), (-5.68, -1.2, 2.5), wood_dark)

# ── 工作台（后墙左段）─────────────────────────────────
box('bench_top', (3.4, 1.5, 0.12), (-3.6, 4.6, 0.95), wood_dark)
for i, (dx, dy) in enumerate([(-1.55, -0.6), (1.55, -0.6), (-1.55, 0.6), (1.55, 0.6)]):
    box(f'bench_leg{i}', (0.14, 0.14, 0.9), (-3.6 + dx, 4.6 + dy, 0.45), metal_dark)
# 显示器 + 发光屏幕
box('monitor', (1.1, 0.08, 0.7), (-3.7, 5.0, 1.75), metal_dark, rot=(math.radians(-8), 0, 0))
box('monitor_screen', (0.98, 0.03, 0.58), (-3.7, 4.955, 1.75), screen_teal, rot=(math.radians(-8), 0, 0))
box('monitor_foot', (0.3, 0.25, 0.35), (-3.7, 5.05, 1.18), metal_dark)
# 键盘与散落的纸
box('keyboard', (0.9, 0.32, 0.05), (-3.6, 4.35, 1.04), metal_dark, rot=(0, 0, math.radians(4)))
box('paper1', (0.5, 0.36, 0.02), (-2.5, 4.5, 1.02), paper, rot=(0, 0, math.radians(-12)))

# ── 置物架（后墙右段）─────────────────────────────────
for zi, z in enumerate((1.7, 2.5)):
    box(f'shelf{zi}', (2.8, 0.55, 0.08), (2.8, 5.5, z), wood_dark)
box('shelf_box1', (0.55, 0.45, 0.45), (2.0, 5.5, 2.0), box_amber, rot=(0, 0, math.radians(8)))
box('shelf_box2', (0.5, 0.4, 0.4), (3.1, 5.5, 1.98), box_teal)
box('shelf_box3', (0.45, 0.4, 0.35), (3.7, 5.45, 2.76), rug_red, rot=(0, 0, math.radians(-10)))
sphere('shelf_ball', 0.2, (2.5, 5.5, 2.79), cat_blue, seg=14)

# ── 蓝猫（房间主角，坐在地毯上）───────────────────────
cyl('rug', 2.1, 0.05, (0.6, 0.4, 0.03), rug_red, verts=28)
sphere('cat_body', 0.55, (0.6, 0.6, 0.62), cat_blue, scale=(1.0, 0.85, 1.15))
sphere('cat_belly', 0.42, (0.6, 0.34, 0.5), cat_belly, scale=(0.8, 0.55, 0.9))
sphere('cat_head', 0.4, (0.6, 0.52, 1.5), cat_blue)
cone('cat_ear_l', 0.16, 0.36, (0.34, 0.52, 1.88), cat_blue, verts=10, rot=(0, math.radians(-12), 0))
cone('cat_ear_r', 0.16, 0.36, (0.86, 0.52, 1.88), cat_blue, verts=10, rot=(0, math.radians(12), 0))
sphere('cat_muzzle', 0.16, (0.6, 0.2, 1.4), cat_belly, seg=12, scale=(1.2, 0.7, 0.8))
cyl('cat_tail', 0.09, 1.0, (1.35, 0.95, 0.3), cat_blue, verts=10, rot=(math.radians(70), 0, math.radians(-30)))
sphere('cat_paw_l', 0.16, (0.3, 0.15, 0.12), cat_blue, seg=12)
sphere('cat_paw_r', 0.16, (0.9, 0.15, 0.12), cat_blue, seg=12)

# ── 杂物：木箱堆 / 落地灯 / 盆栽 ──────────────────────
box('crate1', (1.0, 1.0, 1.0), (3.9, 3.2, 0.5), wood_floor, rot=(0, 0, math.radians(12)))
box('crate2', (0.75, 0.75, 0.75), (4.0, 3.1, 1.38), wood_dark, rot=(0, 0, math.radians(-18)))
cyl('lamp_pole', 0.05, 2.3, (4.6, 5.0, 1.15), metal_dark, verts=12)
cone('lamp_shade', 0.42, 0.5, (4.6, 5.0, 2.45), rug_red, verts=16, rot=(math.pi, 0, 0))
sphere('lamp_bulb', 0.13, (4.6, 5.0, 2.3), bulb_warm, seg=12)
cyl('pot', 0.28, 0.45, (-4.7, 3.9, 0.23), pot_clay, verts=14)
sphere('plant1', 0.4, (-4.7, 3.9, 0.85), plant_green, seg=12, scale=(1, 1, 1.3))
sphere('plant2', 0.28, (-4.5, 3.7, 1.2), plant_green, seg=10)

# ── 灯光与世界 ─────────────────────────────────────────
sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN'))
sun.data.energy = 5.5
sun.data.color = srgb('#ffe0b8')
sun.data.angle = math.radians(12)
sun.rotation_euler = (math.radians(58), math.radians(-18), math.radians(-105))
scene.collection.objects.link(sun)

fill = bpy.data.objects.new('fill', bpy.data.lights.new('fill', 'AREA'))
fill.data.energy = 460
fill.data.size = 8
fill.data.color = srgb('#bcd0ff')
fill.location = (2.0, -1.0, 5.4)
scene.collection.objects.link(fill)

# 工作台顶补光（暖），治桌面死黑
desk = bpy.data.objects.new('desk_light', bpy.data.lights.new('desk_light', 'POINT'))
desk.data.energy = 90
desk.data.color = srgb('#ffcf9e')
desk.data.shadow_soft_size = 0.6
desk.location = (-3.6, 4.2, 3.0)
scene.collection.objects.link(desk)

world = bpy.data.worlds.new('world')
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (*srgb('#2a3040'), 1.0)
bg.inputs['Strength'].default_value = 0.85
scene.world = world

# ── 合并 + UV 展开 ─────────────────────────────────────
bpy.ops.object.select_all(action='DESELECT')
for o in PARTS:
    o.select_set(True)
bpy.context.view_layer.objects.active = PARTS[0]
bpy.ops.object.join()
room = bpy.context.object
room.name = 'Workshop'
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(island_margin=0.015)
bpy.ops.object.mode_set(mode='OBJECT')

# ── Cycles 烘焙 ────────────────────────────────────────
scene.render.engine = 'CYCLES'
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for dt in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
        try:
            prefs.compute_device_type = dt
            prefs.get_devices()
            gpus = [d for d in prefs.devices if d.type != 'CPU']
            if gpus:
                for d in prefs.devices:
                    d.use = True
                scene.cycles.device = 'GPU'
                print(f'BAKE: using GPU via {dt}')
                break
        except Exception:
            continue
except Exception as e:
    print('BAKE: GPU probe failed, CPU fallback:', e)

bake_img = bpy.data.images.new('bake', BAKE_SIZE, BAKE_SIZE, alpha=False)
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

bake_png = os.path.join(OUT_DIR, 'workshop_bake.png')
bake_img.filepath_raw = bake_png
bake_img.file_format = 'PNG'
bake_img.save()
print('BAKE: saved', bake_png)

# ── 换成单一烘焙材质，导出 GLB ─────────────────────────
baked_mat = bpy.data.materials.new('baked')
baked_mat.use_nodes = True
bsdf = baked_mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Roughness'].default_value = 1.0
tex = baked_mat.node_tree.nodes.new('ShaderNodeTexImage')
tex.image = bake_img
baked_mat.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
room.data.materials.clear()
room.data.materials.append(baked_mat)

glb_path = os.path.join(OUT_DIR, 'workshop-raw.glb')
bpy.ops.object.select_all(action='DESELECT')
room.select_set(True)
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_yup=True,
)
print('BAKE: exported', glb_path)
print('BAKE: DONE')
