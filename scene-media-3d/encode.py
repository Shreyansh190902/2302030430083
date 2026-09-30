"""Join rendered PNG frames into an H.264 MP4 using Blender's built-in FFmpeg.
Run:  python encode.py <frames_dir> <out.mp4>
"""
import bpy, os, sys

frames_dir, out = sys.argv[-2], sys.argv[-1]
files = sorted(f for f in os.listdir(frames_dir) if f.endswith('.png'))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = 24
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
sc.sequence_editor_create()
strip = sc.sequence_editor.sequences.new_image('frames', os.path.join(frames_dir, files[0]), 1, 1)
for f in files[1:]:
    strip.elements.append(f)
sc.frame_start, sc.frame_end = 1, len(files)
sc.view_settings.view_transform = 'Standard'   # frames are already colour-managed
sc.render.image_settings.file_format = 'FFMPEG'
sc.render.ffmpeg.format = 'MPEG4'
sc.render.ffmpeg.codec = 'H264'
sc.render.ffmpeg.constant_rate_factor = 'HIGH'
sc.render.ffmpeg.ffmpeg_preset = 'GOOD'
sc.render.filepath = out
bpy.ops.render.render(animation=True)
print('encoded', len(files), 'frames ->', out)
