# Scene Media – 20 Second 3D Logo Intro (Blender)

**Made in:** Blender 4.2 (Cycles renderer), 1280×720, 24 fps, 480 frames
**Look:** dark cinematic studio, glossy mirror floor, brand-red metallic "S" mark, bright white 3D letters, red rim lights and glow.

## Files in this folder
| File | What it is |
|------|------------|
| `scene-media-3d-intro.mp4` | The final rendered 20-second video |
| `scene.blend` | The Blender project – open it in Blender 4.2+ to tweak and re-render (fonts are packed inside) |
| `scene.py` | Script that builds the whole scene from scratch (geometry, materials, lights, camera, animation) |
| `trace.py` + `logo-black.jpg` → `logo.json` | Traces your logo into vector outlines used for the 3D icon, letters and dot |
| `encode.py` | Joins rendered frames into the MP4 |
| `ArchivoBlack.ttf`, `Poppins-600.ttf` | Fonts for the 3D words and tagline |

---

## Shot-by-shot script

| Time | Shot / camera | What happens | Voiceover | Sound |
|------|---------------|--------------|-----------|-------|
| **0:00 – 0:03** | Wide, low angle; the camera glides forward through darkness | Fades up from black. A spotlight **clicks on** with a flicker, lighting a glossy black floor. Red and white **light streaks** zip across the frame. Warm dust floats in the air. | *(none)* | Low drone, light-switch "clunk", whooshes on the streaks |
| **0:03 – 0:04.5** | Front, mid shot | **CREATE.** (white 3D letters, red full stop) flips up off the floor with a bounce, holds, then **flies at the camera**. | "Create." | Bass hit + whoosh |
| **0:04.5 – 0:06** | Same, slow push in | **CAPTURE.** flips up and flies out the same way. | "Capture." | Camera shutter + hit |
| **0:06 – 0:07.5** | Same | **INSPIRE.** flips up and flies out. | "Inspire." | Hit, riser starts |
| **0:07.5 – 0:08.3** | Push in fast | A burst of light streaks. The **two halves of the red S** fly in: top half from the upper left, bottom half from the lower right. | *(none)* | Riser building |
| **0:08.3** | Close-up | **IMPACT** – the halves lock together: bright flash, camera shake, red **shockwave ring** blasts outward, rim lights flare. | *(none)* | Big boom |
| **0:08.5 – 0:12.5** | The camera slowly orbits to the right | Hero shot: the glossy red S turns to show its 3D depth and bevels, with red rim lights pulsing and reflections sliding across it. | *(none)* | Deep sustained hit / music |
| **0:12.5 – 0:14.5** | The camera pulls back to a wide front shot | The S swings back and **moves into its place** in the logo. The letters **S-C-E-N-E  M-E-D-I-A** flip up one after another like panels. | "Scene Media." | Quick ticks on each letter |
| **0:14.6 – 0:15.4** | Wide | The red **dot** pops in with an elastic bounce – full logo complete, reflected in the mirror floor. | *(none)* | "Pop" |
| **0:15 – 0:16.6** | Wide, slow push in | A bright bar of light **sweeps across** the logo from left to right. | *(none)* | Shimmer / "shing" |
| **0:15.4 – 0:19** | Same | The tagline **EVERY STORY DESERVES A SCENE** rises up out of the floor, and a glowing red line draws out beneath it. | "Every story deserves a scene." | Music resolves |
| **0:19 – 0:20** | Same | The spotlight dims and everything fades to black. | *(none)* | Final low hit, then silence |

## Voiceover (about 20 seconds)
> *(0:03)* Create. *(0:04.5)* Capture. *(0:06)* Inspire.
> *(0:13)* Scene Media.
> *(0:15.5)* Every story deserves a scene.

Deep, confident trailer voice. Leave a beat after each of the first three words.

## Music
A cinematic logo reveal or trailer track at 100–120 BPM: quiet build (0–7s), **big impact at 0:08.3**, resolve at 0:15.
Try YouTube Audio Library, Pixabay Music or Epidemic Sound ("cinematic logo reveal", "trailer impact").

---

## Editing it in Blender
1. Open `scene.blend` in **Blender 4.2 or newer**. Press **Space** in the viewport to preview the animation.
2. **Words:** select `CREATE` / `CAPTURE` / `INSPIRE` / `Tagline`, press **Tab** and type new text.
3. **Colours:** the `Red`, `White` and `Floor` materials are in the Shading tab.
4. **Timing:** move keyframes in the Timeline or Dope Sheet (at 24 fps, frame = seconds × 24 + 1).
5. **Render:** Render → Render Animation. For 1080p set Output Properties → Resolution to 1920×1080.
   With a GPU (Cycles → Device: GPU) it renders much faster than the CPU render used here.

**To rebuild from scratch** (e.g. with a new logo): replace `logo-black.jpg` (the logo on a black background), then run
`python trace.py` and then `python scene.py scene.blend` with the `bpy` package (`pip install bpy==4.2.*`).
