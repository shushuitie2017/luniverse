# LIFE 生活区（amber 强调）——榻榻米茶间，小蓝猫在猫窝里打盹
# 用法: blender -b -P tools/bake_life.py -- <输出目录>
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bake_lib as L

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT_DIR = os.path.abspath(argv[0] if argv else '.')

L.reset()

# ── 材质 ────────────────────────────────────────────────
tatami = L.make_mat('tatami', '#b3a878', 0.95)
wall_warm = L.make_mat('wall_warm', '#4a4038', 0.9)
wall_side = L.make_mat('wall_side', '#443b34', 0.9)
wood_dark = L.make_mat('wood_dark', '#5f4633', 0.6)
wood_warm = L.make_mat('wood_warm', '#8f6f4e', 0.65)
blanket = L.make_mat('blanket', '#e8a33d', 0.95)
cushion_red = L.make_mat('cushion_red', '#b8432f', 0.9)
cushion_teal = L.make_mat('cushion_teal', '#3fa8a0', 0.9)
ceramic = L.make_mat('ceramic', '#dfe6ee', 0.4)
cat_blue = L.make_mat('cat_blue', '#3d6db5', 0.55)
window_lit = L.make_mat('window_lit', '#fff0d0', 0.3, emit='#ffdba8', emit_strength=5.5)
bulb_warm = L.make_mat('bulb_warm', '#ffd9a0', 0.3, emit='#ffd9a0', emit_strength=9.0)
plant_green = L.make_mat('plant_green', '#4d8a52', 0.8)
pot_clay = L.make_mat('pot_clay', '#a06a45', 0.85)
paper = L.make_mat('paper', '#d8d3c8', 0.9)
art_ink = L.make_mat('art_ink', '#39414e', 0.8)

# ── 房间壳 + 窗 ─────────────────────────────────────────
L.room_shell(tatami, wall_warm, wall_side, wood_dark)
L.window_on_left(wood_dark, window_lit, y=-0.6)

# 挂画（后墙）
L.box('art_frame', (1.6, 0.1, 2.0), (2.6, 5.74, 2.6), wood_dark)
L.box('art_paper', (1.4, 0.06, 1.8), (2.6, 5.7, 2.6), paper)
L.sphere('art_moon', 0.28, (2.9, 5.64, 3.1), art_ink, seg=14, scale=(1, 0.15, 1))
L.box('art_hill', (0.9, 0.05, 0.3), (2.35, 5.66, 2.15), art_ink, rot=(0, math.radians(-6), 0))

# ── 矮桌（被炉风）+ 茶具 ────────────────────────────────
L.box('table_top', (2.4, 1.6, 0.1), (0.2, 1.4, 0.62), wood_warm)
L.box('table_blanket', (2.7, 1.9, 0.3), (0.2, 1.4, 0.42), blanket)
L.box('table_base', (1.6, 1.0, 0.3), (0.2, 1.4, 0.15), wood_dark)
L.cyl('teapot_body', 0.22, 0.26, (-0.3, 1.3, 0.82), ceramic, verts=16)
L.sphere('teapot_lid', 0.1, (-0.3, 1.3, 0.98), ceramic, seg=10)
L.cyl('teapot_spout', 0.04, 0.3, (-0.02, 1.2, 0.85), ceramic, verts=8, rot=(0, math.radians(60), math.radians(-20)))
L.cyl('cup1', 0.09, 0.12, (0.5, 1.1, 0.74), ceramic, verts=12)
L.cyl('cup2', 0.09, 0.12, (0.75, 1.6, 0.74), ceramic, verts=12)

# ── 坐垫两只 ────────────────────────────────────────────
L.cyl('cushion1', 0.5, 0.16, (0.2, -0.2, 0.08), cushion_red, verts=20)
L.cyl('cushion2', 0.5, 0.16, (1.9, 1.6, 0.08), cushion_teal, verts=20)

# ── 猫窝 + 打盹的小蓝猫（右侧）─────────────────────────
L.cyl('bed_outer', 0.85, 0.35, (3.6, 3.2, 0.18), cushion_red, verts=22)
L.cyl('bed_inner', 0.62, 0.3, (3.6, 3.2, 0.26), blanket, verts=20)
L.sphere('cat_sleep_body', 0.45, (3.6, 3.2, 0.55), cat_blue, scale=(1.15, 0.95, 0.55))
L.sphere('cat_sleep_head', 0.26, (3.15, 2.95, 0.55), cat_blue)
L.cone('cat_sleep_ear', 0.1, 0.2, (3.05, 2.85, 0.78), cat_blue, verts=8, rot=(0, math.radians(-15), 0))
L.cyl('cat_sleep_tail', 0.07, 0.9, (4.15, 3.5, 0.42), cat_blue, verts=8, rot=(math.radians(80), 0, math.radians(50)))

# ── 书堆 + 台灯（左后角）───────────────────────────────
for i, (z, mat, rot) in enumerate([(0.09, cushion_teal, 4), (0.27, paper, -7), (0.45, cushion_red, 12)]):
    L.box(f'book{i}', (0.55, 0.75, 0.18), (-4.4, 4.5, z), mat, rot=(0, 0, math.radians(rot)))
L.cyl('floor_lamp_pole', 0.045, 2.1, (-3.4, 4.9, 1.05), wood_dark, verts=10)
L.cone('floor_lamp_shade', 0.4, 0.45, (-3.4, 4.9, 2.25), paper, verts=16, rot=(math.pi, 0, 0))
L.sphere('floor_lamp_bulb', 0.12, (-3.4, 4.9, 2.12), bulb_warm, seg=12)

# ── 绿植 ────────────────────────────────────────────────
L.cyl('pot2', 0.3, 0.5, (4.6, 4.9, 0.25), pot_clay, verts=14)
L.sphere('plant_a', 0.45, (4.6, 4.9, 1.0), plant_green, seg=12, scale=(1, 1, 1.25))
L.sphere('plant_b', 0.3, (4.4, 4.6, 1.35), plant_green, seg=10)

# ── 灯光（更暖的黄昏调 + 桌面补光）─────────────────────
L.lights(sun_color='#ffd9a8', sun_energy=5.0, fill_color='#c9c2ae', fill_energy=430,
         world_color='#332e2a', world_strength=0.9,
         extra_points=[((0.2, 1.4, 3.0), '#ffcf9e', 100), ((3.6, 3.2, 2.2), '#ffd9a0', 60)])

L.finish(OUT_DIR, 'life')
