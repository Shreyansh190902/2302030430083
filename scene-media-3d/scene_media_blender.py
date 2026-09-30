"""Scene Media – 20 s 3D logo intro for Blender 4.2+ (single file, no other files needed).

HOW TO USE IN THE BLENDER APP
  1. Open Blender, go to the "Scripting" tab (top bar).
  2. Click "New", paste this whole file, then click "Run Script" (▶).
  3. The 3D viewport jumps to the camera view on the finished logo.
     Press Space to play the animation (frame 1 is black on purpose – it fades up).
  4. Render the video: Render menu → Render Animation (frames are saved to the "render" folder).

Timeline @24 fps (480 frames):
  0–3 s    darkness, spotlight clicks on, red light streaks, dust
  3–7.5 s  3D words CREATE. / CAPTURE. / INSPIRE. flip in and fly out
  7.5–10 s the two halves of the S mark slam together – flash, shake, shockwave
  10–12.5  hero shot: mark turns, red rims pulse
  12.5–15  mark moves into place, letters of SCENE MEDIA flip up, red dot pops
  15–19 s  light sweep across logo, tagline rises from the floor
  19–20 s  fade to black
"""
import bpy, bmesh, base64, json, math, os, random, sys, zlib
from mathutils import Vector

# your logo, traced into outlines (compressed JSON)
LOGO_DATA = (
    "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"
)

def _here():
    for d in (os.path.dirname(bpy.data.filepath), os.getcwd()):
        if d and os.path.isdir(d):
            return d
    return ''

HERE = _here()
FPS, END = 24, 480
Z0 = 3.4                                  # height of the logo centre above the floor
ICON_C = Vector((-4.68, 0.0))              # icon centre in traced logo coords
random.seed(7)

def F(sec):
    return int(round(sec * FPS)) + 1

# ---------------------------------------------------------------- reset scene
if bpy.app.background:
    bpy.ops.wm.read_factory_settings(use_empty=True)
else:
    # inside the Blender UI: clear the current scene instead of resetting Blender
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob)
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
        for block in list(coll):
            coll.remove(block)
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
logo = json.loads(zlib.decompress(base64.b64decode(''.join(LOGO_DATA))))

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
def load_font(fname):
    # uses the .ttf if it sits next to your .blend file, otherwise Blender's built-in font
    path = os.path.join(HERE, fname)
    return bpy.data.fonts.load(path) if os.path.exists(path) else bpy.data.fonts.load('<builtin>')

font = load_font('ArchivoBlack.ttf')
font_tag = load_font('Poppins-600.ttf')

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
sc.render.filepath = '//render/'
# open on the finished logo (frame 1 is black on purpose – the intro fades up from darkness)
sc.frame_set(F(17.5))
if not bpy.app.background:
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.shading.type = 'RENDERED'
            area.spaces.active.region_3d.view_perspective = 'CAMERA'
if bpy.app.background and sys.argv[-1].endswith('.blend'):
    bpy.ops.wm.save_as_mainfile(filepath=sys.argv[-1])
    print('saved', sys.argv[-1])
