# Eye-care Instagram carousel (Gujarati + English)

Topic: *Should you put water directly in your eyes?* — 9 slides, 1080×1440 (3:4), matching the provided cover.

- `assets/cover.webp` — slide 01 (provided cover)
- `slides.html` — slides 02–09 (09 = dark outro: watch full podcast on YouTube) (edit text here)
- `assets/fonts.css`, `assets/fonts/` — bundled Inter, Noto Sans Gujarati, Baloo Bhai 2, Caveat
- `assets/show-logo.jpg`, `assets/show-logo-dark.png` — show logo (light / dark-background versions)
- `assets/outro.jpg` — podcast outro artwork used for slide 09
- `out/01.png … 09.png` — ready-to-post images (PNG)
- `out-jpg/01.jpg … 09.jpg` — same images as JPG

Re-render after editing:

```sh
cd carousel
NODE_PATH=$(npm root -g) node render.js   # needs the `playwright` npm package
```
