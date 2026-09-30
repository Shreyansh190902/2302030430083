import json, numpy as np, potrace
from PIL import Image
img = np.asarray(Image.open('logo-black.jpg').convert('RGB')).astype(int)
R,G,B = img[...,0], img[...,1], img[...,2]
masks = {'red': (R > 120) & (G < 90) & (B < 90), 'white': (R > 128) & (G > 128) & (B > 128)}
cx, cy, S = 1000, 1000, 100.0   # centre + scale: 100 px -> 1 Blender unit

P = lambda p: np.array([p.x, p.y], float)

def bez(p0, p1, p2, p3, n=10):
    t = np.linspace(0, 1, n + 1)[1:, None]
    return ((1-t)**3)*p0 + 3*((1-t)**2)*t*p1 + 3*(1-t)*t*t*p2 + t**3*p3

def trace(mask):
    plist = potrace.Bitmap(~mask).trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=0.2)
    polys = []
    for c in plist:
        pts = []; cur = P(c.start_point)
        for s in c.segments:
            if s.is_corner:
                pts += [P(s.c), P(s.end_point)]
            else:
                pts += list(bez(cur, P(s.c1), P(s.c2), P(s.end_point)))
            cur = P(s.end_point)
        a = np.array(pts)
        a = np.c_[(a[:, 0] - cx) / S, -(a[:, 1] - cy) / S]
        polys.append(a)
    return polys

def group(polys):
    # an outline whose bbox sits inside another outline's bbox is a hole of it
    bb = [(p[:,0].min(), p[:,1].min(), p[:,0].max(), p[:,1].max()) for p in polys]
    area = [(b[2]-b[0])*(b[3]-b[1]) for b in bb]
    groups = {}
    for i, b in enumerate(bb):
        parents = [j for j, o in enumerate(bb) if j != i and area[j] > area[i] and o[0] <= b[0] and o[1] <= b[1] and o[2] >= b[2] and o[3] >= b[3]]
        if parents: groups.setdefault(min(parents, key=lambda j: area[j]), []).append(i)
        else: groups.setdefault(i, [])
    out = []
    for o, holes in groups.items():
        out.append({'bbox': bb[o], 'polys': [polys[o].tolist()] + [polys[h].tolist() for h in holes]})
    return out

red = group(trace(masks['red'])); white = group(trace(masks['white']))
icon = [g for g in red if g['bbox'][2] < -2]      # icon is on the left
dot  = [g for g in red if g['bbox'][2] >= -2]
# letters: two rows, sorted by row (top first) then x
white.sort(key=lambda g: (-round(g['bbox'][3]), g['bbox'][0]))
json.dump({'icon': icon, 'dot': dot, 'letters': white}, open('logo.json', 'w'))
print('icon parts', len(icon), 'dot', len(dot), 'letters', len(white))
for g in icon + dot + white: print([round(v, 2) for v in g['bbox']], 'holes', len(g['polys']) - 1)
