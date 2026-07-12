# STUDIO 工坊制作间（teal 强调）——雕刻小蓝猫的工作室
# 用法: blender -b -P tools/bake_studio.py -- <输出目录>
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bake_lib as L

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT_DIR = os.path.abspath(argv[0] if argv else '.')

L.reset()

# ── 材质 ────────────────────────────────────────────────
concrete = L.make_mat('concrete', '#6f6a62', 0.9)
wall_teal = L.make_mat('wall_teal', '#31414a', 0.9)
wall_side = L.make_mat('wall_side', '#2e3a42', 0.9)
wood_dark = L.make_mat('wood_dark', '#5f4633', 0.6)
wood_raw = L.make_mat('wood_raw', '#a8845c', 0.7)
metal_dark = L.make_mat('metal_dark', '#23262e', 0.4)
metal_teal = L.make_mat('metal_teal', '#3fa8a0', 0.45)
stone = L.make_mat('stone', '#9aa0a8', 0.85)
neon_teal = L.make_mat('neon_teal', '#0d1418', 0.3, emit='#3fa8a0', emit_strength=6.0)
window_lit = L.make_mat('window_lit', '#fff4e0', 0.3, emit='#ffe9c4', emit_strength=5.0)
paint_red = L.make_mat('paint_red', '#b8432f', 0.6)
paint_amber = L.make_mat('paint_amber', '#e8a33d', 0.6)
paint_blue = L.make_mat('paint_blue', '#3d6db5', 0.6)
bulb_warm = L.make_mat('bulb_warm', '#ffd9a0', 0.3, emit='#ffd9a0', emit_strength=10.0)

# ── 房间壳 + 窗 ─────────────────────────────────────────
L.room_shell(concrete, wall_teal, wall_side, wood_dark)
L.window_on_left(wood_dark, window_lit)

# 后墙 neon 灯条（工坊招牌）
L.box('neon_strip', (3.4, 0.12, 0.16), (0.4, 5.62, 3.3), neon_teal)
L.box('neon_mount', (3.6, 0.08, 0.3), (0.4, 5.74, 3.3), metal_dark)

# ── 中央工作台 + 半成品蓝猫雕像 ─────────────────────────
L.box('bench_top', (3.6, 1.8, 0.14), (0.4, 1.6, 1.0), wood_dark)
for i, (dx, dy) in enumerate([(-1.6, -0.75), (1.6, -0.75), (-1.6, 0.75), (1.6, 0.75)]):
    L.box(f'bench_leg{i}', (0.16, 0.16, 0.95), (0.4 + dx, 1.6 + dy, 0.48), metal_dark)
# 雕像基座 + 半成品猫（石材=还没上色的蓝猫）
L.cyl('statue_base', 0.55, 0.18, (0.4, 1.6, 1.16), wood_raw, verts=16)
L.sphere('statue_body', 0.42, (0.4, 1.6, 1.62), stone, scale=(1.0, 0.85, 1.15))
L.sphere('statue_head', 0.3, (0.4, 1.55, 2.28), stone)
L.cone('statue_ear_l', 0.12, 0.26, (0.2, 1.55, 2.56), stone, verts=10, rot=(0, math.radians(-12), 0))
L.cone('statue_ear_r', 0.12, 0.26, (0.6, 1.55, 2.56), stone, verts=10, rot=(0, math.radians(12), 0))
# 凿子和木槌搁在台面
L.cyl('chisel', 0.035, 0.5, (1.4, 1.2, 1.1), metal_teal, verts=10, rot=(0, math.radians(90), math.radians(20)))
L.cyl('mallet_handle', 0.04, 0.5, (-0.8, 1.1, 1.1), wood_raw, verts=10, rot=(0, math.radians(90), math.radians(-30)))
L.cyl('mallet_head', 0.11, 0.22, (-1.05, 1.22, 1.1), wood_dark, verts=12, rot=(math.radians(90), 0, math.radians(-30)))

# ── 工具墙（后墙挂板）───────────────────────────────────
L.box('pegboard', (3.0, 0.12, 1.6), (-3.4, 5.72, 2.4), wood_raw)
for i, x in enumerate((-4.4, -3.9, -3.4, -2.9)):
    L.cyl(f'tool_handle{i}', 0.04, 0.55, (x, 5.6, 2.45), wood_dark, verts=8, rot=(math.radians(90), 0, 0))
    L.box(f'tool_head{i}', (0.16, 0.08, 0.12), (x, 5.6, 2.75), metal_dark)

# ── 木料堆（右侧）──────────────────────────────────────
for i, (y, z) in enumerate([(3.6, 0.25), (4.1, 0.25), (3.85, 0.68)]):
    L.cyl(f'log{i}', 0.24, 3.0, (3.8, y, z), wood_raw, verts=12, rot=(0, math.radians(90), math.radians(8)))

# ── 货架 + 油漆桶（左后角，开放框架别做实心盒——会把陈设封在里面）──
L.box('shelf_side_l', (0.08, 0.6, 2.4), (-5.5, 4.4, 1.2), metal_dark)
L.box('shelf_side_r', (0.08, 0.6, 2.4), (-3.7, 4.4, 1.2), metal_dark)
L.box('shelf_b1', (1.7, 0.55, 0.06), (-4.6, 4.4, 0.8), wood_dark)
L.box('shelf_b2', (1.7, 0.55, 0.06), (-4.6, 4.4, 1.6), wood_dark)
L.box('shelf_b3', (1.7, 0.55, 0.06), (-4.6, 4.4, 2.35), wood_dark)
for i, (x, mat) in enumerate([(-5.1, paint_red), (-4.6, paint_amber), (-4.1, paint_blue)]):
    L.cyl(f'paint{i}', 0.16, 0.3, (x, 4.4, 0.98), mat, verts=14)
L.cyl('paint_top', 0.16, 0.3, (-4.85, 4.4, 1.78), metal_teal, verts=14)

# ── 刨花桶 + 吊灯 ──────────────────────────────────────
L.cyl('bin', 0.4, 0.7, (2.6, 0.2, 0.35), metal_dark, verts=16)
L.sphere('shavings', 0.34, (2.6, 0.2, 0.72), wood_raw, seg=10, scale=(1, 1, 0.5))
L.cyl('lamp_cord', 0.02, 1.0, (0.4, 1.6, 3.7), metal_dark, verts=8)
L.cone('lamp_shade2', 0.38, 0.4, (0.4, 1.6, 3.1), metal_teal, verts=16, rot=(math.pi, 0, 0))
L.sphere('lamp_bulb2', 0.12, (0.4, 1.6, 2.98), bulb_warm, seg=12)

# ── 灯光（工作台顶补光）────────────────────────────────
L.lights(extra_points=[((0.4, 1.6, 3.4), '#ffcf9e', 110)])

L.finish(OUT_DIR, 'studio')
