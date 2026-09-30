"""Scene Media – 20 s 3D logo intro, built procedurally with Blender (bpy 4.2).

Run:  python scene.py <out.blend>
Timeline @24 fps (480 frames):
  0–3 s    darkness, spotlight clicks on, red light streaks fly past, dust
  3–7.5 s  3D words CREATE. / CAPTURE. / INSPIRE. flip in and fly out
  7.5–10 s the two halves of the S mark slam together – flash, shake, shockwave
  10–12.5  hero shot: mark turns, red rims pulse
  12.5–15  mark moves into place, letters of SCENE MEDIA flip up, red dot pops
  15–19 s  light sweep across logo, tagline rises from the floor
  19–20 s  fade to black
"""
import bpy, bmesh, json, math, os, random, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
FPS, END = 24, 480
Z0 = 3.4                                  # height of the logo centre above the floor
ICON_C = Vector((-4.68, 0.0))              # icon centre in traced logo coords
random.seed(7)

def F(sec):
    return int(round(sec * FPS)) + 1

# ---------------------------------------------------------------- reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, END

# ---------------------------------------------------------------- helpers
def kf(owner, path, frame, value, interp='BEZIER', easing='AUTO'):
    setattr(owner, path, value)
    owner.keyframe_insert(path, frame=frame)
    ad = owner.id_data.animation_data if hasattr(owner, 'id_data') else owner.animation_data
    for fc in ad.action.fcurves:
        if fc.data_path.endswith(path):
            for k in fc.keyframe_points:
                if int(round(k.co.x)) == frame:
                    k.interpolation, k.easing = interp, easing

def vis(obj, on_frames):
    """on_frames: (first, last) frame the object renders."""
    a, b = on_frames
    for f, h in ((1, True), (a, False), (b + 1, True)):
        obj.hide_render = h; obj.hide_viewport = h
        obj.keyframe_insert('hide_render', frame=f); obj.keyframe_insert('hide_viewport', frame=f)

def mat_principled(name, color, metal=0.0, rough=0.3, coat=0.0, emit=None, emit_strength=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metal
    p.inputs['Roughness'].default_value = rough
    p.inputs['Coat Weight'].default_value = coat
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1)
        p.inputs['Emission Strength'].default_value = emit_strength
    return m

def mat_emit(name, color, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); o = nt.nodes.new('ShaderNodeOutputMaterial')
    e.inputs['Color'].default_value = (*color, 1); e.inputs['Strength'].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0])
    return m, e.inputs['Strength']

def empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); e.location = loc
    sc.collection.objects.link(e); return e

def curve_from_polys(name, polys, offset, extrude, bevel):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '2D'; cu.fill_mode = 'BOTH'
    cu.extrude, cu.bevel_depth, cu.bevel_resolution, cu.resolution_u = extrude, bevel, 3, 1
    for poly in polys:
        sp = cu.splines.new('POLY'); sp.points.add(len(poly) - 1); sp.use_cyclic_u = True
        for p, (x, y) in zip(sp.points, poly):
            p.co = (x - offset.x, y - offset.y, 0, 1)
    ob = bpy.data.objects.new(name, cu); sc.collection.objects.link(ob)
    ob.rotation_euler.x = math.radians(90)          # stand upright, facing -Y (camera)
    return ob

def to_mesh(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    new = bpy.data.objects.new(ob.name + '_m', me); sc.collection.objects.link(new)
    new.matrix_world = ob.matrix_world.copy()
    bpy.data.objects.remove(ob); return new

# ---------------------------------------------------------------- materials
RED = (0.72, 0.0, 0.0)
m_red = mat_principled('Red', RED, metal=0.2, rough=0.22, coat=1.0, emit=(1, 0.0, 0.0), emit_strength=0.12)
m_white = mat_principled('White', (0.95, 0.95, 0.95), metal=0.0, rough=0.28, coat=0.5)
m_floor = mat_principled('Floor', (0.008, 0.008, 0.008), rough=0.18)
m_streak_r, _ = mat_emit('StreakRed', (1, 0.02, 0.02), 40)
m_streak_w, _ = mat_emit('StreakWhite', (1, 0.9, 0.85), 30)
m_dust, _ = mat_emit('Dust', (1, 0.55, 0.4), 6)
m_tag, _ = mat_emit('Tagline', (1, 1, 1), 2.2)
m_line, line_strength = mat_emit('Underline', (1, 0.02, 0.02), 25)
m_shock, shock_strength = mat_emit('Shock', (1, 0.03, 0.02), 60)

# ---------------------------------------------------------------- world + floor
w = bpy.data.worlds.new('World'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.004, 0.0005, 0.0005, 1); bg.inputs['Strength'].default_value = 1

bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, 0))
floor = bpy.context.object; floor.name = 'Floor'; floor.data.materials.append(m_floor)

# ---------------------------------------------------------------- logo geometry
logo = json.load(open(os.path.join(HERE, 'logo.json')))

# icon -> mesh -> split into top & bottom halves
icon_curve = curve_from_polys('Icon', logo['icon'][0]['polys'], ICON_C, 0.32, 0.035)
icon_curve.rotation_euler.x = 0
icon_mesh = to_mesh(icon_curve)
halves = []
for keep_top in (True, False):
    me = icon_mesh.data.copy()
    bm = bmesh.new(); bm.from_mesh(me)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0), plane_no=(0, 1, 0),
                                 clear_inner=keep_top, clear_outer=not keep_top)
    edges = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
    try:
        bmesh.ops.edgeloop_fill(bm, edges=edges)
    except Exception as ex:
        print('cap fill skipped:', ex)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('IconTop' if keep_top else 'IconBot', me)
    sc.collection.objects.link(ob); ob.data.materials.clear(); ob.data.materials.append(m_red)
    for p in ob.data.polygons: p.use_smooth = False
    halves.append(ob)
bpy.data.objects.remove(icon_mesh)
top, bot = halves

icon_root = empty('IconRoot')
icon_root.rotation_euler.x = math.radians(90)
for h in halves: h.parent = icon_root

# letters (pivot = bottom centre so they flip up like panels)
letters = []
for i, g in enumerate(logo['letters']):
    x0, y0, x1, y1 = g['bbox']
    piv = Vector(((x0 + x1) / 2, y0))
    ob = curve_from_polys(f'L{i}', g['polys'], piv, 0.26, 0.025)
    ob.data.materials.append(m_white)
    ob.location = (piv.x, 0.12, piv.y + Z0)
    letters.append(ob)

dx0, dy0, dx1, dy1 = logo['dot'][0]['bbox']
dpiv = Vector(((dx0 + dx1) / 2, (dy0 + dy1) / 2))
dot = curve_from_polys('Dot', logo['dot'][0]['polys'], dpiv, 0.26, 0.025)
dot.data.materials.append(m_red); dot.location = (dpiv.x, 0.12, dpiv.y + Z0)

# ---------------------------------------------------------------- 3D words
font = bpy.data.fonts.load(os.path.join(HERE, 'ArchivoBlack.ttf'))
font_tag = bpy.data.fonts.load(os.path.join(HERE, 'Poppins-600.ttf'))

def word(text, start, dur):
    cu = bpy.data.curves.new(text, 'FONT'); cu.body = text + '.'
    cu.font = font; cu.size = 2.1; cu.extrude = 0.22; cu.bevel_depth = 0.02
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    cu.materials.append(m_white); cu.materials.append(m_red)
    cu.body_format[len(text)].material_index = 1
    ob = bpy.data.objects.new(text, cu); sc.collection.objects.link(ob)
    a, b = F(start), F(start + dur)
    vis(ob, (a, b))
    kf(ob, 'location', a, (0, 3, Z0), 'BACK', 'EASE_OUT')
    kf(ob, 'rotation_euler', a, (0, 0, math.radians(-10)), 'BACK', 'EASE_OUT')
    kf(ob, 'scale', a, (0.3, 0.3, 0.3), 'BACK', 'EASE_OUT')
    kf(ob, 'location', a + 9, (0, 0, Z0), 'LINEAR')
    kf(ob, 'rotation_euler', a + 9, (math.radians(90), 0, 0), 'LINEAR')
    kf(ob, 'scale', a + 9, (1, 1, 1), 'LINEAR')
    kf(ob, 'location', b - 7, (0, -0.8, Z0), 'EXPO', 'EASE_IN')
    kf(ob, 'rotation_euler', b - 7, (math.radians(90), 0, math.radians(3)), 'EXPO', 'EASE_IN')
    kf(ob, 'scale', b - 7, (1.03, 1.03, 1.03), 'EXPO', 'EASE_IN')
    kf(ob, 'location', b, (0, -9, Z0 + 0.4))
    kf(ob, 'rotation_euler', b, (math.radians(90), 0, math.radians(12)))
    kf(ob, 'scale', b, (1.5, 1.5, 1.5))
    return ob

word('CREATE', 3.0, 1.5)
word('CAPTURE', 4.5, 1.5)
word('INSPIRE', 6.0, 1.5)

# ---------------------------------------------------------------- tagline + underline
cu = bpy.data.curves.new('Tag', 'FONT'); cu.body = 'EVERY STORY DESERVES A SCENE'
cu.font = font_tag; cu.size = 0.42; cu.space_character = 1.9; cu.extrude = 0.02
cu.align_x = 'CENTER'; cu.materials.append(m_tag)
tag = bpy.data.objects.new('Tagline', cu); sc.collection.objects.link(tag)
tag.rotation_euler.x = math.radians(90)
kf(tag, 'location', 1, (0, -0.6, -0.7), 'CONSTANT')
kf(tag, 'location', F(15.4), (0, -0.6, -0.7), 'BACK', 'EASE_OUT')
kf(tag, 'location', F(16.2), (0, -0.6, 0.42))

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.6, 0.18))
line = bpy.context.object; line.name = 'Underline'; line.data.materials.append(m_line)
kf(line, 'scale', 1, (0, 0.03, 0.03), 'CONSTANT')
kf(line, 'scale', F(15.9), (0, 0.03, 0.03), 'EXPO', 'EASE_OUT')
kf(line, 'scale', F(16.9), (6.2, 0.03, 0.03))

# ---------------------------------------------------------------- icon + logo animation
HERO = Vector((0, 0, Z0))
FINAL = Vector((ICON_C.x, 0.12, ICON_C.y + Z0))
IMPACT = F(8.3)
kf(icon_root, 'location', 1, HERO, 'CONSTANT')
kf(icon_root, 'scale', 1, (1.35, 1.35, 1.35), 'CONSTANT')
kf(icon_root, 'rotation_euler', 1, (math.radians(90), 0, 0), 'CONSTANT')
kf(icon_root, 'rotation_euler', IMPACT + 6, (math.radians(90), 0, 0), 'SINE', 'EASE_IN_OUT')
kf(icon_root, 'rotation_euler', F(11.2), (math.radians(90), 0, math.radians(-28)), 'SINE', 'EASE_IN_OUT')
kf(icon_root, 'rotation_euler', F(12.5), (math.radians(90), 0, math.radians(8)), 'BACK', 'EASE_OUT')
kf(icon_root, 'location', F(12.5), HERO, 'EXPO', 'EASE_IN_OUT')
kf(icon_root, 'scale', F(12.5), (1.35, 1.35, 1.35), 'EXPO', 'EASE_IN_OUT')
kf(icon_root, 'rotation_euler', F(13.5), (math.radians(90), 0, 0))
kf(icon_root, 'location', F(13.5), FINAL)
kf(icon_root, 'scale', F(13.5), (1, 1, 1))

for ob, start in ((top, Vector((-14, 6, 4))), (bot, Vector((14, -2.3, 4)))):
    vis(ob, (F(7.5), END))
    kf(ob, 'location', 1, start, 'CONSTANT')
    kf(ob, 'rotation_euler', 1, (0, 0, math.radians(35 if ob is top else -35)), 'CONSTANT')
    kf(ob, 'location', F(7.5), start, 'EXPO', 'EASE_IN')
    kf(ob, 'rotation_euler', F(7.5), (0, 0, math.radians(35 if ob is top else -35)), 'EXPO', 'EASE_IN')
    kf(ob, 'location', IMPACT, (0, 0, 0))
    kf(ob, 'rotation_euler', IMPACT, (0, 0, 0))

# letters flip up one by one, dot pops last
for i, ob in enumerate(letters):
    s = F(13.3) + i * 2
    kf(ob, 'rotation_euler', 1, (0, 0, 0), 'CONSTANT')
    kf(ob, 'scale', 1, (0, 0, 0), 'CONSTANT')
    kf(ob, 'scale', s, (1, 1, 1), 'CONSTANT')
    kf(ob, 'rotation_euler', s, (0, 0, 0), 'BACK', 'EASE_OUT')
    kf(ob, 'rotation_euler', s + 12, (math.radians(90), 0, 0))
kf(dot, 'scale', 1, (0, 0, 0), 'CONSTANT')
kf(dot, 'scale', F(14.6), (0, 0, 0), 'ELASTIC', 'EASE_OUT')
kf(dot, 'scale', F(15.4), (1, 1, 1))

# shockwave ring
bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.025, major_segments=96, minor_segments=8,
                                 location=(0, 0.3, Z0), rotation=(math.radians(90), 0, 0))
ring = bpy.context.object; ring.name = 'Shock'; ring.data.materials.append(m_shock)
vis(ring, (IMPACT, IMPACT + 22))
kf(ring, 'scale', IMPACT, (0.6, 0.6, 0.6), 'EXPO', 'EASE_OUT')
kf(ring, 'scale', IMPACT + 22, (14, 14, 14))
kf(shock_strength, 'default_value', IMPACT, 80, 'SINE', 'EASE_IN')
kf(shock_strength, 'default_value', IMPACT + 22, 0)

# ---------------------------------------------------------------- light streaks + dust
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=7, vertices=8, rotation=(0, math.radians(90), 0))
streak_src = bpy.context.object; streak_src.name = 'StreakSrc'
streak_mesh = streak_src.data; bpy.data.objects.remove(streak_src)
def streak(t0, dur, y, z, direction, mat):
    ob = bpy.data.objects.new('Streak', streak_mesh.copy()); sc.collection.objects.link(ob)
    ob.data.materials.append(mat)
    a, b = F(t0), F(t0 + dur)
    vis(ob, (a, b))
    kf(ob, 'location', a, (-30 * direction, y, z), 'LINEAR')
    kf(ob, 'location', b, (30 * direction, y, z))
for i in range(9):
    streak(0.4 + i * 0.28, 0.55, random.uniform(-4, 6), random.uniform(0.5, 7), 1 if i % 2 else -1,
           m_streak_r if i % 3 else m_streak_w)
for i in range(6):
    streak(7.25 + i * 0.07, 0.4, random.uniform(-3, 2), random.uniform(1.5, 6), 1 if i % 2 else -1,
           m_streak_r if i % 2 else m_streak_w)

bpy.ops.mesh.primitive_ico_sphere_add(radius=0.025, subdivisions=1)
dust_src = bpy.context.object; dust_mesh = dust_src.data; bpy.data.objects.remove(dust_src)
dust_mesh.materials.append(m_dust)
for i in range(140):
    ob = bpy.data.objects.new('Dust', dust_mesh); sc.collection.objects.link(ob)
    x, y, z = random.uniform(-16, 16), random.uniform(-10, 14), random.uniform(0.2, 9)
    ob.scale = [random.uniform(0.5, 1.6)] * 3
    kf(ob, 'location', 1, (x, y, z), 'LINEAR')
    kf(ob, 'location', END, (x + random.uniform(-1.5, 1.5), y, z + random.uniform(1.5, 4)))

# ---------------------------------------------------------------- lights
def light(name, kind, loc, energy, color=(1, 1, 1), size=1.0, target=(0, 0, Z0)):
    ld = bpy.data.lights.new(name, kind); ld.energy = energy; ld.color = color
    if kind == 'AREA': ld.size = size
    if kind == 'SPOT': ld.spot_size = math.radians(55); ld.spot_blend = 0.6
    ob = bpy.data.objects.new(name, ld); sc.collection.objects.link(ob); ob.location = loc
    ob.visible_camera = False
    d = Vector(target) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob

key = light('Key', 'AREA', (3, -10, 9), 1500, size=5)
fill = light('Fill', 'AREA', (-7, -9, 3), 350, (0.9, 0.93, 1), size=6)
rim_l = light('RimL', 'AREA', (-9, 9, 10), 2600, (1, 0.03, 0.02), size=4)
rim_r = light('RimR', 'AREA', (9, 9, 10), 2600, (1, 0.03, 0.02), size=4)
spot = light('Spot', 'SPOT', (0, -1, 13), 0, size=0.5, target=(0, 0, 0))
flash = light('Flash', 'POINT', (0, -3, Z0), 0)
sweep = light('Sweep', 'AREA', (-14, -3.5, Z0), 0, size=0.4, target=(0, 0, Z0))
sweep.data.shape = 'RECTANGLE'; sweep.data.size, sweep.data.size_y = 0.3, 9

# spotlight "clicks" on with a flicker
for f, e in ((1, 0), (F(0.5), 0), (F(0.5) + 1, 5000), (F(0.5) + 3, 800), (F(0.5) + 5, 4500), (F(0.5) + 8, 3500)):
    kf(spot.data, 'energy', f, e, 'CONSTANT')
for f, e in ((F(19), 3500), (END, 0)):
    kf(spot.data, 'energy', f, e, 'SINE')
# rim pulse during hero shot
for ob in (rim_l, rim_r):
    for f, e in ((1, 1200), (F(7.4), 1200), (IMPACT, 6000), (F(10), 2600), (F(11.2), 4200), (F(12.5), 2600)):
        kf(ob.data, 'energy', f, e, 'SINE', 'EASE_IN_OUT')
# impact flash
for f, e in ((1, 0), (IMPACT - 1, 0), (IMPACT, 22000), (IMPACT + 10, 0)):
    kf(flash.data, 'energy', f, e, 'EXPO' if f == IMPACT else 'CONSTANT', 'EASE_OUT')
# light sweep across the finished logo
kf(sweep.data, 'energy', 1, 0, 'CONSTANT'); kf(sweep.data, 'energy', F(15), 9000, 'CONSTANT')
kf(sweep.data, 'energy', F(16.6), 0, 'CONSTANT')
kf(sweep, 'location', F(15), (-14, -3.5, Z0), 'SINE', 'EASE_IN_OUT'); kf(sweep, 'location', F(16.5), (14, -3.5, Z0))

# ---------------------------------------------------------------- camera
target = empty('CamTarget', (0, 0, Z0))
cd = bpy.data.cameras.new('Cam'); cd.lens = 50
cd.dof.use_dof = True; cd.dof.focus_object = target; cd.dof.aperture_fstop = 3.2
cam = bpy.data.objects.new('Cam', cd); sc.collection.objects.link(cam); sc.camera = cam
tc = cam.constraints.new('TRACK_TO'); tc.target = target; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'

cam_keys = [  # (sec, location, target, interp, easing)
    (0.0,  (-6, -34, 1.2), (0, 0, Z0 - 1), 'SINE', 'EASE_OUT'),
    (3.0,  (0, -17, 2.8), (0, 0, Z0), 'SINE', 'EASE_IN_OUT'),
    (7.4,  (0, -14.5, 3.2), (0, 0, Z0), 'EXPO', 'EASE_OUT'),
    (8.3,  (0, -12.5, 3.3), (0, 0, Z0), 'SINE', 'EASE_IN_OUT'),
    (12.4, (4.5, -12, 2.2), (0, 0, Z0), 'EXPO', 'EASE_IN_OUT'),
    (14.2, (0, -27, 3.2), (0, 0, Z0 - 0.45), 'SINE', 'EASE_IN_OUT'),
    (20.0, (0, -24.5, 3.0), (0, 0, Z0 - 0.45), 'SINE', 'EASE_IN_OUT'),
]
for sec, loc, tgt, it, ea in cam_keys:
    kf(cam, 'location', F(sec), loc, it, ea)
    kf(target, 'location', F(sec), tgt, it, ea)

# camera shake on impact
for fc in cam.animation_data.action.fcurves:
    if fc.data_path == 'location' and fc.array_index in (0, 2):
        m = fc.modifiers.new('NOISE'); m.scale = 1.5; m.strength = 0.9; m.phase = fc.array_index * 13
        m.use_restricted_range = True; m.frame_start = IMPACT; m.frame_end = IMPACT + 14; m.blend_out = 10

# ---------------------------------------------------------------- render + colour
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 12
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 3; sc.cycles.transparent_max_bounces = 2
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
sc.view_settings.view_transform = 'Khronos PBR Neutral'; sc.view_settings.look = 'None'
for f, v, it in ((1, -8, 'SINE'), (F(0.6), 0, 'CONSTANT'), (F(19), 0, 'SINE'), (END, -10, 'CONSTANT')):
    kf(sc.view_settings, 'exposure', f, v, it, 'EASE_IN_OUT')

# compositor glow
sc.use_nodes = True
nt = sc.node_tree; nt.nodes.clear()
rl = nt.nodes.new('CompositorNodeRLayers'); comp = nt.nodes.new('CompositorNodeComposite')
glare = nt.nodes.new('CompositorNodeGlare'); glare.glare_type = 'FOG_GLOW'; glare.quality = 'MEDIUM'
glare.threshold = 0.8; glare.size = 8; glare.mix = -0.55
lens = nt.nodes.new('CompositorNodeLensdist'); lens.inputs['Dispersion'].default_value = 0.012; lens.use_fit = True
nt.links.new(rl.outputs['Image'], glare.inputs['Image'])
nt.links.new(glare.outputs['Image'], lens.inputs['Image'])
nt.links.new(lens.outputs['Image'], comp.inputs['Image'])

sc.render.image_settings.file_format = 'PNG'
bpy.ops.wm.save_as_mainfile(filepath=sys.argv[-1])
print('saved', sys.argv[-1])
