# "કોઈ ધંધો નાનો નથી હોતો" — reel carousel (Gujarati + English)

7 slides, 1080×1440, old grid-paper theme. Built from the visuals of the Bipinbhai Hadvani
reel (on-screen title, FOGG ad clips, office/podium b-roll); the reel has no subtitles and the
audio could not be transcribed here, so slide copy is written around the visuals, not quoted.
Slide 06 numbers (50 પૈસા → ₹10,000 કરોડ) come from the full episode's YouTube description.

- `assets/bipin-photo.webp`, `assets/sagar-photo.webp` — provided photos; `assets/person-*.png` — background-removed cutouts used on the cover; `assets/outro.webp` — outro artwork
- Slides 02–06 are text-only content cards (no photos)
- `out/`, `out-jpg/`, `no-small-business-jpg.zip` — exports

Re-render: `NODE_PATH=$(npm root -g) node render.js`

## Minimal theme
`slides-minimal.html` is the same content in a minimal black/white/red design (flat, no grid,
no doodles or emojis). Render with `NODE_PATH=$(npm root -g) node render.js slides-minimal.html out-minimal`.
Exports: `out-minimal/`, `out-minimal-jpg/`, `no-small-business-minimal-jpg.zip`.

## Essence theme
`slides-essence.html` — light grey grid/circle layout with red pill tags, page dots and arrow button
(inspired by a reference post). Render: `node render.js slides-essence.html out-essence`.
Exports: `out-essence/`, `out-essence-jpg/`, `no-small-business-essence-jpg.zip`.

## Essence theme — red / black / white
`slides-essence-rbw.html` — same layout on pure white with solid red tags/button and black text.
Exports: `out-essence-rbw/`, `out-essence-rbw-jpg/`, `no-small-business-red-black-white-jpg.zip`.

## Poster theme (red / black / white, Hind Vadodara)
`slides-poster.html` — black background, big red slide numbers, white headlines, red bottom band.
Font: Hind Vadodara (Gujarati + Latin). Exports: `out-poster/`, `out-poster-jpg/`, `no-small-business-poster-jpg.zip`.
